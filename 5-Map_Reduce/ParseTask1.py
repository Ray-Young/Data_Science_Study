from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import JSONProtocol
from itertools import combinations

import re
import json

Regex = re.compile(r"[\w']+")

class ParseTask1(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def get_words(self, _, review):
        for word in Regex.findall(review['text']):
            yield (word.lower(), 1)

    def calculate_words(self, word, counts):
        yield (word, sum(counts))

    def steps(self):
        return [MRStep(mapper = self.get_words,
                       reducer = self.calculate_words)]

if __name__ == '__main__':
    ParseTask1.run();
