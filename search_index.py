from sklearn.metrics.pairwise import cosine_similarity as csim
import ijson
import json
import os
import time
import itertools

class Search():
    
    def __init__(self, query:str):
       self._components = query.lower().split()
       self._pages = dict()
       self.path = os.getcwd()
       self._numPages = 0

   
    def search_index_json(self):
        '''
        Returns a list of tuples
        Each tuple consists of a search term and the byte offset in final_index.json
        '''
        path = os.path.join(self.path, "PTR", "JSON")
        ptr = []
        
        for i in self._components:
            with open(os.path.join(path, (i[0] + ".json")), "r", buffering=1) as file:
                item = json.loads(file.read())
                ptr.append((i, item[i]))
        return ptr
    
    
    def get_pages(self, bufferSize = 65534):
        with open("final_index.json", "r", buffering=1) as file:
            termValue = ""
            for i in self.search_index_json():
                file.seek(i[1]-1)
                temp = file.read(bufferSize)
                termValue = temp
                
                while "]" not in temp:
                    temp = file.read(bufferSize)
                    termValue += temp
    
                termValue = "{" + termValue[:termValue.index("]")+1] + "}"
                jsonForm = json.loads(termValue)
                
                for j in jsonForm[i[0]]:
                    if j['url'] not in self._pages:
                        self._pages[j['url']] = [j['tfidf']]
                        self._numPages += 1
                    else:
                        self._pages[j['url']].append(j['tfidf'])
        
        highest = max(len(j) for j in self._pages.values())
        topResults = [i for i in self._pages.values if i == highest]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        