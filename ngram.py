from math import log10

class Ngram(object):
    def __init__(self, path, sep=' '):
        self.ngrams = {}
        with open(path, 'r') as f:
            for line in f:
                ngram, count = line.strip().split(sep)
                self.ngrams[ngram] = int(count)

        self.len_of_ngram = len(ngram)  # bi-gram, tri-gram etc.
        self.num_of_ngrams = sum(self.ngrams.values())

        # calculate probabilities for known n-grams
        for ngram in list(self.ngrams.keys()):
            count = self.ngrams[ngram]
            if count > 0:
                self.ngrams[ngram] = log10(float(count) / self.num_of_ngrams)

        # Log probability floor for unknown n-grams
        self.floor = log10(0.01 / self.num_of_ngrams)

    def score(self, message):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(message) - self.len_of_ngram + 1):
            ngram = message[i:i + self.len_of_ngram]
            if ngram in self.ngrams:
                score += ngrams(ngram)
            else:
                score += self.floor

        return score
