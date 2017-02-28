from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import JSONProtocol
from itertools import combinations

import re
import json

regex = re.compile(r"[\w']+")

class ParseTask2(MRJob):
    
    def get_words(self, _, review):
        data = json.loads(review)
        for word in regex.findall(data["text"]):
            yield(word.lower(),data['review_id'])
       
    def calculate_words(self, word, review_id):
        dic = {}
        if word in dic:
            dic[word].append(review_id)
        else:
            dic[word] = []
            dic[word].append(review_id)
        
        x=0;
        tmp = []
        for i in dic[word][0]:
            x+=1
            tmp.append(i)
        if(x==1):
            x=0
            yield tmp[0],1
      
    def max_distinct(self,review_id,count):
        yield None,(sum(count),review_id)
    
    def max_review(self,_,review_count_pairs):
        print("Max number of review words:")
        yield max(review_count_pairs)
            
    def steps(self):
        return [MRStep(mapper = self.get_words,combiner=self.calculate_words,reducer = self.max_distinct), MRStep(reducer = self.max_review)]

if __name__ == '__main__':
    ParseTask2.run();
