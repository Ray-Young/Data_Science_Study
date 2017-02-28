from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import JSONProtocol
from itertools import combinations
from sklearn.metrics import jaccard_similarity_score

import re

WORD_RE = re.compile(r"[\w']+")

class Jaccard(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    
    def map_user_business(self,_,review):
        yield(review['user_id'],review['business_id'])
        
    def reduce_user_business(self,user,business):
        yield(user,list(set(business)))
    
    def map_user_businesslist(self,user,businesslist):
        yield (None, (user,businesslist))
        
    def reduce_similarity(self,_,users):
        for user1,user2 in combinations(users,2):
            #print("user1: ",user1,user1[1])
            #print("user2: ",user2,user2[1])
            #J_similarity = jaccard_similarity_score(user1[1],user2[1])
            #print(set(user1[1]).intersection(user2[1]))
            J_similarity = len(set(user1[1]).intersection(user2[1]))/len(set(user1[1]+user2[1]))
            if J_similarity >= 0.5:
                yield((user1[0],user2[0]),J_similarity)
                
    def steps(self):
        return [MRStep(mapper = self.map_user_business,
                      reducer = self.reduce_user_business),
               MRStep(mapper = self.map_user_businesslist,
                     reducer = self.reduce_similarity)]

if __name__ == '__main__':
    Jaccard.run();
