from sklearn.metrics.pairwise import cosine_similarity as csim
import ijson
import json
import os
import time
import itertools

class Search():
    
    def __init__(self, query:str):
       self._components = query.lower().split()
       self._pages = dict(itertools.zip_longest(*[iter(self._components)] * 2, fillvalue=list))
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
        
        for i in self._components:
            with open(os.path.join(path, (i[0] + ".json")), "r") as file:
                item = json.loads(file.read())
                ptr.append((i, item[i]))
        return ptr
    
    
    def get_pages(self, bufferSize = 65534):
        termPos = self.search_index_json()
        start = time.time()
        
        with open("final_index.json", "r", buffering=1) as file:
            items = []
            termValue = ""
            for i in termPos:
                file.seek(i[1]-1)
                temp = file.read(bufferSize)
                termValue = temp
                
                while "]" not in temp:
                    temp = file.read(bufferSize)
                    termValue += temp
    
                termValue = "{" + termValue[:termValue.index("]")+1] + "}"
                jsonForm = json.loads(termValue)
                
                for j in jsonForm[i[0]]:
                    items.append((j["url"], j["tfidf"]))
                
                self._pages[i[0]] = sorted(items)

        #print(self._pages)
        end = time.time()
        print(end-start)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        