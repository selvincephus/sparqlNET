###################################################################################################
#  Written by Selvin Cephus Jayakumar
###################################################################################################
import unicodedata
import re

import torch


class SparqlPostprocessing:
    # Legacy code. Is not used currently but could be a useful class for future work
    def __init__(self):
        pass

    def sparqilise(self, query):
        query = query.replace("starturl", " <")
        query = query.replace("endurl", "> ")
        query = query.replace("openbrace", " (")
        query = query.replace("closebrace", ") ")

        if re.search("dbpedia resource", query):
            query = query.replace("dbpedia resource", "http://dbpedia.org/resource/")

        if re.search("dbpedia ontology", query):
            query = query.replace("dbpedia ontology", "http://dbpedia.org/ontology/")

        if re.search("rdfsyntaxnstype", query):
            query = query.replace("rdfsyntaxnstype", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

        if re.search("dbpedia property", query):
            query = query.replace("dbpedia property", "http://dbpedia.org/property/")

        return query


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {"humidity":2,"solve":3,"alarm":4,"features":5,"LAA":6,"CDA":7,"counters":8, "value":9, "package":10}
        self.word2count = {}
        self.index2word = {0:"SOS",1:"EOS",2:"humidity",3:"solve",4:"alarm",5:"features",6:"LAA",7:"CDA",8:"counters",9:"value",10:"package"}

        self.n_words = len(self.word2index)  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


class DataPrep:
    def __init__(self, lang1, lang2, reverse, device):
        self.SOS_token = 0
        self.EOS_token = 1
        self.lang1 = lang1
        self.lang2 = lang2
        self.reverse = reverse
        self.device = device

    # Turn a Unicode string to plain ASCII, thanks to
    # http://stackoverflow.com/a/518232/2809427
    def unicodeToAscii(s):
        # print(s)
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def normalizeString(self, s):
        # s = unicodeToAscii(s.lower().strip())
        s = re.sub(r"([.!?])", r" \1", s)
        # s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
        return s

    def readLangs(self):
        # print("Reading lines...")
        # Read the file and split into lines

        data = open('data/%s-%s.txt' % (self.lang1, self.lang2), encoding="utf8"). \
            read().strip().split('\n')

        # Split every line into pairs and normalize
        pairs = [[self.normalizeString(s) for s in l.split(',')] for l in data]

        # Reverse pairs, make Lang instances
        if self.reverse:
            pairs = [list(reversed(p)) for p in pairs]
            input_lang = Lang(self.lang2)
            output_lang = Lang(self.lang1)
        else:
            input_lang = Lang(self.lang1)
            output_lang = Lang(self.lang2)

        return input_lang, output_lang, pairs

    def prepareData(self):
        input_lang, output_lang, pairs = self.readLangs()
        # print("Read %s train sentence pairs" % len(pairs))
        # print("Trimmed to %s train sentence pairs" % len(pairs))
        # print("Counting words...")
        for pair in pairs:
            if len(pair) == 2:
                input_lang.addSentence(pair[0])
                output_lang.addSentence(pair[1])
        # print("Counted words in train set:")
        # print(input_lang.name, input_lang.n_words)
        # print(output_lang.name, output_lang.n_words)
        return input_lang, output_lang, pairs

    def normalizeString(self, s):
        # s = unicodeToAscii(s.lower().strip())
        s = re.sub(r"([.!?])", r" \1", s)
        # s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
        return s

    def indexesFromSentence(self, lang, sentence):
        indexes = []
        # return [lang.word2index[word] for word in sentence.split(' ')]
        words = sentence.split(' ')
        words = list(filter(None, words))  # filter out null characters in sentences. Causes key error if not done.
        for word in words:
            word_index = lang.word2index[word]
            indexes.append(word_index)
        return indexes

    def tensorFromSentence(self, lang, sentence):
        indexes = self.indexesFromSentence(lang, sentence)
        indexes.append(self.EOS_token)
        return torch.tensor(indexes, dtype=torch.long, device=self.device).view(-1, 1)

    def tensorsFromPair(self, pair):
        input_tensor = self.tensorFromSentence(self.input_lang, pair[0])
        target_tensor = self.tensorFromSentence(self.output_lang, pair[1])
        return input_tensor, target_tensor


