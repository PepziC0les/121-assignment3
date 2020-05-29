import ijson
import json
import os
import time
import itertools
from numpy import dot
from numpy.linalg import norm

class Search():
    
    def __init__(self, query:str):
        self._original = query.lower().split()
        self._components = list()
        self._stopWords = list()
        with open("stopWords.txt", "r") as file:
            data = file.read()
            end = time.time()
            for word in self._original:
                if word in data:
                    self._stopWords.append(word)
                else:
                    self._components.append(word)
        self._pages = dict()
        self._backupPages = dict()
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
    
    
    def get_pages(self, bufferSize = 85534):
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
        #print("qf: ", qf)
        for url, val in self._pages.items():
            print(val)
            #print(val)
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
    



    def new_getPages(self, bufferSize = 85534):
        path = os.path.join(os.getcwd(),"PTR", "JSON")
        for word in self._components:
            if word[0] in "abcdefghijklmnopqrstuvwxyz":
                temp_path = os.path.join(path, word[0] + ".json")
            else:
                temp_path = os.path.join(path, "misc.json")
            with open(temp_path, "r") as file:
                temp = file.read(bufferSize)
                termValue = temp
                start = time.time()
                while time.time() - start < .02:
                    temp = file.read(bufferSize)
                    
                    if word in termValue:
                        termValue += temp
                    else:
                        termValue = temp
                    if termValue.find("]]") < termValue.find(word):
                        termValue = termValue[termValue.index(word):]
                termValue = "{\"" + termValue[:termValue.find("]]")+2] + "}"
                data = json.loads(termValue)

                for val in data[word]:
                    if val[0] in self._pages:
                        self._pages[val[0]].append(val[1])
                    else:
                        self._pages[val[0]] = [val[1],]
        if len(self._pages) < 10:
            for word in self._stopWords:
                if word[0] in "abcdefghijklmnopqrstuvwxyz":
                    temp_path = os.path.join(path, word[0] + ".json")
                else:
                    temp_path = os.path.join(path, "misc.json")
                start2 = time.time()
                with open(temp_path, "r") as file:
                    temp = file.read(bufferSize)
                    termValue = temp
                    start = time.time()
                    while time.time() - start < .02:
                        temp = file.read(bufferSize)
                        
                        if word in termValue:
                            termValue += temp
                        else:
                            termValue = temp

                    termValue = "{\"" + termValue[:termValue.find("]]")+2] + "}"

                    data = json.loads(termValue)

                    for val in data[word]:
                        if val[0] in self._pages:
                            self._backupPages[val[0]].append(val[1])
                        else:
                            self._backupPages[val[0]] = [val[1],]
        self._pages = {url:tfidf for url, tfidf in self._pages.items() if len(tfidf) == len(self._components)}
        self._backupPages = {url:tfidf for url, tfidf in self._backupPages.items() if len(tfidf) == len(self._stopWords)}

        qf = [self._components.count(word)/len(self._components) for word in self._components]
        results = list()
        done = False

        for url, val in self._pages.items():
            cosine_sim = dot(qf, val) / (norm(qf) * norm(val))
            if len(results) < 10 or cosine_sim > results[-1][1]:
                if len(results) == 10:
                    results.pop()
                    done = True
                results.append((url, cosine_sim))
                #results = sorted(results, key=lambda x: x[1], reverse=True)
            #if url in self._backupPages:
            #    self._backupPages[url].append(val)
        
        if not done:
            print("here")
            qf = [self._original.count(word)/len(self._original) for word in self._original]

            for url, val in self._backupPages.items():
                cosine_sim = dot(qf, val) / (norm(qf) * norm(val))
                if cosine_sim > results[-1][1] or len(results) < 10:
                    if len(results) == 10:
                        results.pop()
                    results.append((url, cosine_sim))
                    results = sorted(results, key=lambda x: x[1], reverse=True)

        
        return results
                    
            