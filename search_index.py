from sklearn.metrics.pairwise import cosine_similarity as csim
import ijson
import json
import os
import time
import itertools

class Search():
    
    def __init__(self, query:str):
       self._components = query.lower().split()
       self._pages = dict(itertools.zip_longest(*[iter(self._components)] * 2, fillvalue=set()))
       self.path = os.getcwd()
    
    def __repr__(self):
        return str(self._index[self._pages[0]])
    
    
    '''
    def search_index_txt(self):
        path = os.path.join(self.path, "PTR","TXT")
        for i in self._indexes:
            with open(os.path.join(path, (i + ".txt")), "r") as file:
                pass
    '''
   
    def search_index_json(self):
        path = os.path.join(self.path, "PTR","JSON")
        ptr = []
        
        start = time.time()
        for i in self._components:
            with open(os.path.join(path, (i[0] + ".json")), "r") as file:
                item = json.loads(file.read())
                ptr.append((i, item[i]))
        end = time.time()
        print(end-start)
        return ptr
    
    
    def get_pages(self):
        with open("final_index.json", "r") as file:
            for i in self.search_index_json():
                file.seek(i[1]-1)
                prevValue = ""
                for prefix, the_type, value in ijson.parse(file):
                    if prefix == '' and the_type == 'map_key':
                        break
                    if prefix == "in.item.url":
                        prevValue = value
                        self._pages[i[0]][value] = 0
                    if prefix == "in.item.tfidf":
                        self._pages[i[0]][prevValue] = value
        print(self._pages)