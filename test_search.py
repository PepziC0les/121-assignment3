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
    



    def new_getPages(self, bufferSize = 65534):
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
                        termValue = termValue[termValue.index(word) - 1:]
                termValue = "{" + termValue[:termValue.find("]]")+2] + "}"
                #with open("test.txt", "w") as file:
                 #   file.write (termValue)
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
                            termValue = termValue[termValue.index(word) - 1:]
                    termValue = "{" + termValue[:termValue.find("]]")+2] + "}"

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

        for url in sorted(self._pages, key= lambda x: sum(self._pages[x]), reverse=True)[:50]:
            cosine_sim = dot(qf, self._pages[url]) / (norm(qf) * norm(self._pages[url]))
            if len(results) < 10 or cosine_sim > results[-1][1]:
                if len(results) == 10:
                    results.pop()
                    done = True
                results.append((url, cosine_sim))
                results = sorted(results, key=lambda x: x[1], reverse=True)
            if url in self._backupPages:
                self._backupPages[url].append(val)
        
        if not done:
            qf = [self._original.count(word)/len(self._original) for word in self._original]

            for url in sorted(self._backupPages, key= lambda x: sum(self._backupPages[x]), reverse=True)[:50]:
                cosine_sim = dot(qf, self._backupPages[url]) / (norm(qf) * norm(self._backupPages[url]))
                if cosine_sim > results[-1][1] or len(results) < 10:
                    if len(results) == 10:
                        results.pop()
                    results.append((url, cosine_sim))
                    results = sorted(results, key=lambda x: x[1], reverse=True)

        return results
                    
            