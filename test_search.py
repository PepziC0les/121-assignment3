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
        # gets pages for words that aren't stop words
        for word in self._components:
            # picks the json file to look into
            if word[0] in "abcdefghijklmnopqrstuvwxyz":
                temp_path = os.path.join(path, word[0] + ".json")
            else:
                temp_path = os.path.join(path, "misc.json")
            # Starts going through json file looking for word and respective ids
            with open(temp_path, "r") as file:
                temp = file.read(bufferSize)
                termValue = temp
                start = time.time()
                # gives the code .05 sec to look through the json
                while time.time() - start < .05:
                    temp = file.read(bufferSize)
                    # if the word is in the termValue keep appending if it isn't replace what is in it
                    if word in termValue.split("\""):
                        termValue += temp
                    else:
                        termValue = temp

                    # find the spot of the word and ending ]]
                    wordPos = termValue.find("\"" + word + "\"")
                    endPos = termValue.find("]]")
                    # remove extra characters behind if the ending is before the word
                    if endPos < wordPos:
                        termValue = termValue[wordPos:]
                    # if the word and ending exists break
                    if wordPos != -1 and wordPos < endPos:
                        break
                # formats the result into a json 
                termValue = "{" + termValue[:termValue.find("]]")+2] + "}"
                data = json.loads(termValue)

                # adds the url and its tfidf value to pages, throws exception if the word doesn't match what came out of the json
                try:
                    for val in data[word]:
                        if val[0] in self._pages:
                            self._pages[val[0]].append(val[1])
                        else:
                            self._pages[val[0]] = [val[1],]
                except:
                    print("Sorry, results for your search can not be found in our database")
                    return
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
                    while time.time() - start < .05:
                        temp = file.read(bufferSize)
                        if word in termValue.split("\""):
                            termValue += temp
                        else:
                            termValue = temp

                        wordPos = termValue.find("\"" + word + "\"")
                        endPos = termValue.find("]]")
                        if endPos < wordPos:
                            termValue = termValue[wordPos:]
                        if wordPos != -1 and wordPos < endPos:
                            break
                    termValue = "{" + termValue[:termValue.find("]]")+2] + "}"
                    data = json.loads(termValue)

                    try:
                        for val in data[word]:
                            if val[0] in self._backupPages:
                                self._backupPages[val[0]].append(val[1])
                            else:
                                self._backupPages[val[0]] = [val[1],]
                    except:
                        print("Sorry, results for your search can not be found in our database")
                        return
        # takes only pages with all existing words
        self._pages = {url:tfidf for url, tfidf in self._pages.items() if len(tfidf) == len(self._components)}
        self._backupPages = {url:tfidf for url, tfidf in self._backupPages.items() if len(tfidf) == len(self._stopWords)}

        # query frequency
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
        
        # if there aren't enough results, add to the number of results with the backup pages
        if not done:
            qf = [self._original.count(word)/len(self._original) for word in self._original]

            for url in sorted(self._backupPages, key= lambda x: sum(self._backupPages[x]), reverse=True)[:50]:
                cosine_sim = dot(qf, self._backupPages[url]) / (norm(qf) * norm(self._backupPages[url]))
                if len(results) < 10 or cosine_sim > results[-1][1]:
                    if len(results) == 10:
                        results.pop()
                    results.append((url, cosine_sim))
                    results = sorted(results, key=lambda x: x[1], reverse=True)

        return results
                    
            