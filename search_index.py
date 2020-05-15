from sklearn.metrics.pairwise import cosine_similarity as csim
import ijson
import json
import os
import time

class Search():
    
    def __init__(self, query:str):
       self._components = query.lower().split()
       self._pages = []
       self.path = os.getcwd()
    
    def __repr__(self):
        return str(self._index[self._pages[0]])
    
    
    '''
    def search_index_txt(self):
        path = os.path.join(self.path, "PTR","TXT")
        for i in self._indexes:
            with open(os.path.join(path, (i + ".txt"))) as file:
                pass
    '''
   
    def search_index_json(self):
        path = os.path.join(self.path, "PTR","JSON")
        ptr = []
        
        start = time.time()
        for i in self._components:
            with open(os.path.join(path, (i[0] + ".json"))) as file:
                item = json.loads(file.read())
                ptr.append(item[i])
        end = time.time()
        print(end-start)
        return ptr