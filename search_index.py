from sklearn.metrics.pairwise import cosine_similarity as csim
import pandas as pd
import json


class Search():
    
    def __init__(self, query:str, data):
       self.components = query.split()
       self._index = json.loads(data)
       self.pages = []
       
    
    def __repr__(self):
        #return str(self.components)
        return str(self._index[self.pages[0]])
    
    def search_index(self):
        pass