from sklearn.metrics.pairwise import cosine_similarity as csim
import scipy.spatial.distance
import ijson
import json
import os
import time
import itertools
from numpy import dot
from numpy.linalg import norm

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
                    #print(j)
                    if j['url'] not in self._pages:
                        self._pages[j['url']] = [j['tfidf']]
                        self._numPages += 1
                    else:
                        self._pages[j['url']].append(j['tfidf'])
                #print(self._pages)
        self._pages = {url:tfidf for url, tfidf in self._pages.items() if len(tfidf) == len(self._components)}
        qf = [self._components.count(word)/len(self._components) for word in self._components]
        results = list()
        print("qf: ", qf)
        for url, val in self._pages.items():
            print(val)
            # qf is the list of the query frequency
            # val is the tfidf of a url
            # the scipy thing is something I saw online and by subtracting 1 from the distance u get the similarity apparently
            # the second one is more like the formula with the dot product over the normalization
            
            #cosine_sim = 1 - scipy.spatial.distance.cosine(qf, val)
            cosine_sim = dot(qf, val) / (norm(qf) * norm(val))
            #if results[-1][1] < cosine_sim:
            #    results.pop()
            
            #if len(results) > 10:
            #    pass
            #else:
            #    results.append()
            results.append((url, cosine_sim))
        #vals = {url : (sum(tfidf)/len(tfidf)) for url, tfidf in self._pages.items()}
        sorted_vals = sorted(results, key=lambda x: x[1], reverse=True)
        #print(results)
        #print(sorted_vals)
        print("\nHere are the top 5 relevant websites!")
        for count, i in enumerate(sorted_vals[:5]):
            print(f"{count+1}: ", i)
        print()
        return sorted_vals[:5]    