import os, io, json, requests
from config import ConfigProcessor
from amqp_processor import AmqpProcessor
from pgdb import PostgreSqlDatabase
from ner import Ner


# temp storage path (it maybe the local dir or some another)
STORAGE_PATH = None
DOCKER_ENV = "DOCKER_ENV"


def create_callback(ner_model, pgdb):
    def callback(channel, method, properties, body):
        in_msg_dict = json.loads(body.decode())
        print('msg_dict =', in_msg_dict)
        doc_id = in_msg_dict['doc_id']
        link = in_msg_dict['link']

        # 1. Download image to local storage
        filename = link.split('/')[-1]
        local_img_path = os.path.join(STORAGE_PATH, filename)
        with open(local_img_path, 'wb') as handle:
            response = requests.get(link, stream=True)

            if not response.ok:
                print('NOT RESPONSE OK! Failed to download image by link=', link)
                # channel.basic_ack(delivery_tag=method.delivery_tag)
                raise RuntimeError('Failed to download image by link=', link)
                return

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

        # 2.
        ner_outputs = ner_model.handle_file(os.path.join(STORAGE_PATH, filename))

        # 3. Save to db
        word_ids = pgdb.write_words(doc_id, ner_outputs)
        pgdb.write_tags(doc_id, ner_outputs, word_ids)

        # 4. Deliver message ack
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print('Processed doc_id={}'.format(doc_id))
    return callback


def main():
    # for docker docker.json
    if DOCKER_ENV in os.environ:
        cfg_path = './config/docker.json'
    else:
        cfg_path = './config/dev.json'
    # 1.
    config_processor = ConfigProcessor(cfg_path)
    cfg = config_processor.get_configs()
    print(cfg)

    global STORAGE_PATH
    STORAGE_PATH = cfg['local_storage_path']

    # 2. Ner
    ner_model = Ner('./ml/devlabs_ner_ontonotes_bert.json')
    #ret = ner_model.handle_file('/home/neurus/Projects/rvision-hackathon-2021-q1/converted/2020/11-2020-Chaes-e-commerce-malware-research.pdf.txt')
    #print(ret)

    # 3. RabbitMq
    amqp_processor = AmqpProcessor(cfg['rabbit_mq'])

    # 4. DB
    pgdb = PostgreSqlDatabase(cfg)

    # 5. Start to listen incoming messages
    try:
        channel = amqp_processor.establish_connection(create_callback(ner_model, pgdb))
        channel.start_consuming()
    except:
        pgdb.close()
        amqp_processor.close_connection()
        # re-raise the last exception (maybe useful for Docker container!)
        #TODO
        #raise


if __name__ == '__main__':
    main()
    print('Exit...')