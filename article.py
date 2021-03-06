import re
from datetime import datetime

import nltk

import pos_tag


class Article:
    def __init__(self, id, data):
        self.id = id
        self.title = data['title']
        self.content = data['content']
        self.imageUrl = data['imageUrl']
        self.readMoreUrl = data['readMoreUrl']
        self.timestamp = data['timestamp']  # getTimestamp(data['date'], data['time'])
        self.tokens, self.trees = process(data['content'])

    def toJSON(self):
        obj = dict()
        obj['id'] = self.id
        obj['title'] = self.title
        obj['content'] = self.content
        obj['imageUrl'] = self.imageUrl
        obj['readMoreUrl'] = self.readMoreUrl
        obj['timestamp'] = self.timestamp
        obj['trees'] = [str(x) for x in self.trees]
        obj['tokens'] = self.tokens

        return obj


def process(text):
    tokens = pos_tag.posTag(text)
    trees = []
    sentences = [x.strip() for x in text.split(".") if len(x.strip()) > 4]
    for sentence in sentences:
        trees.append(chunk(pos_tag.removeWordsWithTags(pos_tag.posTag(sentence))))
    return tokens, trees


def getTimestamp(date, time):
    date = re.split(r'[\s,]', date)
    del date[-1]

    time = re.split(r'[\s:]', time)
    if time[-1] == 'pm':
        time[0] = str(int(time[0]) + 11)
    del time[-1]

    return int(datetime(int(date[2]), 2, int(date[0]), int(time[0]), int(time[1])).timestamp())


def chunk(tokens, grammar=None):
    if grammar is None:
        # VVVV:RB MD VB - Check if this is required in the future
        grammar = ('''
                    NNNP: {<NNP>+}
                    NNNN: {<DT>?<RB>*<JJ>*<NN.?>+}
                    VVVV: {<RB>*<VB.?>+}
                    NVN: {<.*N><VS><N.*>}
                    NVIN: {<.*N><VVVV><IN><N.*>}
                    NIN: {<.*N><IN><N.*>}
                    ''')
    chunkParser = nltk.RegexpParser(grammar)
    return chunkParser.parse(tokens)

