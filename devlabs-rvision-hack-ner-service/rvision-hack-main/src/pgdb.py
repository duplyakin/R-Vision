import psycopg2

# for performance reasons
attr_to_pg_id = {
    "CVE": 1,
    "CWE": 2,
    "SOFTWARE": 3,
    "MALWARE": 4,
    "COURSE_OF_ACTION": 5,
    "INTRUSION_SET": 6,
    "THREAT_ACTOR": 7,
    "TOOL": 8,
    "ATTACK_PATTERN": 9,
    "INDUSTRY": 10,
    "MITRE_ATTACK": 11,
    "CAMPAIGN": 12,
    "ORG": 13,
    "COUNTRY": 14,
    "CITY": 15,
    "GEOLOCATION": 16,
    "TIMESTAMP": 17,
    "IOC": 18,
    "TECHNIQUE": 19
}

def _prepare_words(doc_id, ner_outputs):
    res = []
    for ner_output in ner_outputs:
        word, label = ner_output
        res.append((word, 2, doc_id))
    return res


def _prepare_tags(doc_id, ner_outputs, word_ids):
    grouped_label = dict()
    for i in range(len(ner_outputs)):
        word, label = ner_outputs[i]
        word_id = word_ids[i]
        if label == 'O':
            continue
        label = label[2:]
        if label not in attr_to_pg_id:
            continue
        if label not in grouped_label:
            grouped_label[label] = []
        grouped_label[label].append(word_id)
    ret = []
    for label, word_ids_list in grouped_label.items():
        ret.append((word_ids_list, attr_to_pg_id[label], 1, doc_id))
    return ret


class PostgreSqlDatabase:

    def __init__(self, config):
        self.connection_string = config["database_url"]
        self.connection = self.get_connection()

    def get_connection(self):
        pg_conn = psycopg2.connect(self.connection_string)
        pg_conn.autocommit = False
        return pg_conn

    def close(self):
        self.connection.close()

    def insert_first_row(self, row):
        pg_cursor = self.connection.cursor()
        pg_cursor.execute("""
                    INSERT INTO document_ocr(ocr_text, status, document_id, is_active, created_at)
                    VALUES (%s,%s,%s, True, now()) RETURNING id;""",
                              row
        )
        id = pg_cursor.fetchone()
        id = id[0]
        self.connection.commit()
        pg_cursor.close()
        return id

    def write_words(self, doc_id, ner_outputs):
        word_rows = _prepare_words(doc_id, ner_outputs)
        if len(word_rows) == 0:
            return []
        next_id = self.insert_first_row(word_rows[0])
        pg_cursor = self.connection.cursor()

        pg_cursor.executemany("""
            INSERT INTO document_ocr(ocr_text, status, document_id, is_active, created_at)
            VALUES (%s,%s,%s, True, now())""",
            word_rows[1:]
        )
        #pg_cursor.executemany("""
        #    INSERT INTO document_ocr(ocr_text, status, document_id, is_active, created_at)
        #    VALUES (%s,%s,%s, True, now())
        #    RETURNING id""",
        #                      word_rows
        #                      )
        #returned_ids = pg_cursor.fetchall()

        ids = [next_id + i for i in range(len(ner_outputs))]
        self.connection.commit()
        pg_cursor.close()
        return ids

    def write_tags(self, doc_id, ner_outputs, word_ids):
        tag_rows = _prepare_tags(doc_id, ner_outputs, word_ids)
        if len(tag_rows) == 0:
            return
        pg_cursor = self.connection.cursor()
        pg_cursor.executemany("""
            INSERT INTO document_nlp(ocr_word_ids, attribute_id, status, document_id, is_active, created_at)
            VALUES (%s, %s, %s, %s, True, now())""",
            tag_rows
        )
        self.connection.commit()
        pg_cursor.close()


if __name__ == '__main__':
    from config import ConfigProcessor
    config_processor = ConfigProcessor('./config/dev.json')
    cfg = config_processor.get_configs()
    print(cfg)
    pgdb = PostgreSqlDatabase(cfg)
    doc_id = 2
    ner_outputs = [('Puppeteer', 'B-MALWARE'), ('library', 'I-MALWARE'),
                   ('for', 'O'), ('further', 'O'), ('attacks', 'O'), ('in', 'O'), ('other', 'O'), ('major', 'O'), ('financial', 'O'), ('institutions', 'O')]
    word_ids = pgdb.write_words(doc_id, ner_outputs)
    print(word_ids)
    pgdb.write_tags(doc_id, ner_outputs, word_ids)