from __future__ import division
import math
import nltk
import numpy as np
from dev_config import ALPHA, BETA, GAMMA

class Corpora:
    def __init__(self, query, corpora, relevantDocIds):
        self.corpora        = corpora
        self.docCount       = len(corpora)
        self.relevantDocIds = relevantDocIds
        self.query          = query
        # computing results at init
        self.documents      = self._parseDocuments(corpora)
        self.bagOfWords     = self._constructVocab()
        self.docFreqs       = self._getDocFreqs()

    def __repr__(self):
        return "Corpora with %d documents, %d words" % \
                (self.docCount, len(self.bagOfWords))

    def _parseDocuments(self, corpora):
        return [nltk.Text([w.lower() for w in nltk.word_tokenize(doc)]) \
                for doc in corpora]

    def _constructVocab(self):
        words = set()
        for d in self.documents:
            words.update([w for w in d if w.isalpha()])
        return words

    def _getDocFreqs(self):
        return { word: sum([1 for doc in self.documents if word in set(doc)]) \
                for word in self.bagOfWords }

    def tfidf(self, term, doc):
        tf = doc.count(term)
        df = self.docFreqs[term]
        idf = math.log(self.docCount / df) if df else 0
        return tf * idf

    # returns a vectorized representation of a document
    def vectorize(self, doc):
        return np.array([self.tfidf(word, doc) for word in sorted(self.bagOfWords)])

    # returns a array of document vectors of all docs in the corpora
    def getVectorizedCorpora(self):
        return [self.vectorize(doc) for doc in self.documents]

    def _getQueryVector(self):
        doc = [w.lower() for w in nltk.word_tokenize(self.query)]
        return self.vectorize(doc)

    def getUpdatedQuery(self):
        relevantDocSum, irrelevantDocSum = 0.0, 0.0
        selectedIds = self.relevantDocIds
        docVectors = self.getVectorizedCorpora()
        relevantCount = len(self.relevantDocIds)
        irrelevantCount = self.docCount - relevantCount

        # get the query vector
        queryVector = self._getQueryVector()

        # find the sums
        for (index, vector) in enumerate(docVectors):
            if index in selectedIds:
                relevantDocSum += vector
            else:
                irrelevantDocSum += vector

        # apply the formula
        vector = (ALPHA * queryVector) + (BETA / relevantCount * relevantDocSum) - \
            (GAMMA / irrelevantCount * irrelevantDocSum)

        topIndices = vector.argsort()[-5:]
        wordList = sorted(self.bagOfWords)

        for i in topIndices:
            print wordList[i],
