from deeppavlov import build_model
import nltk.data
from nltk.tokenize import word_tokenize


def _deprecated_process_output(out, begin_idx):
    ret = [] # [(token, idx)]
    tags = out[1][0]
    for i in range(len(tags)):
        t = tags[i]
        if t == 'O':
            continue
        else:
            tag_name = t[2:] #B-, I-
        ret.append((out[0][0][i], tag_name, i+begin_idx))
    return ret


def process_output(out):
    ret = [] # [(token, idx)]
    tags = out[1][0]
    tokens = out[0][0]
    for i in range(len(tags)):
        ret.append((tokens[i], tags[i]))
    return ret

"""
def handle_file(filepath):
    sentences = split_file_text_into_sentences(filepath)
    idx = 0
    seq_length = 128
    ret = []
    while idx < len(tokens):
        begin_idx = idx
        end_idx = min(len(tokens), begin_idx + seq_length)
        inp = tokens[begin_idx:end_idx]
        out = ner_model(inp)
        ret.extend(process_output(out, begin_idx))
        idx = end_idx
    return ret
"""


class Ner:
    def __init__(self, dp_ner_config_path):
        self.ner_model = build_model(dp_ner_config_path)
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def handle_file(self, filepath):
        sentences = self.split_file_text_into_sentences(filepath)
        ret = []  # [[original words], [NER tags]]
        for sentence in sentences:
            tokens = self.split_sentence_into_tokens(sentence)
            inp = ' '.join(tokens)
            try:
                out = self.ner_model([inp])
                ret.extend(process_output(out))
            except BaseException as e:
                # for debug purposes
                print('WARN: exception=', e)
                out = []
                for tok in tokens:
                    out.append((tok, 'O'))
                ret.extend(out)
        return ret

    def split_file_text_into_sentences(self, filepath):
        with open(filepath) as fp:
            data = fp.read()
        sentences = self.tokenizer.tokenize(data)
        return sentences

    def split_sentence_into_tokens(self, sentence):
        tokens = word_tokenize(sentence)
        return tokens