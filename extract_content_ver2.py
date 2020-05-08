import re
import csv
import nltk
import os
from bs4 import BeautifulSoup
from math import log10
from buildDocCount import buildDocCount


class ContentExtractor:
    def __init__(self, url=None, jsonLine="", globalDict=dict()):
        self.jsonLine = jsonLine
        self.globalDict = globalDict
        self.url = url
        self.wordFrequency = dict()
        self.numOfTerms = 0
        


    def extract_content(self):
        content = BeautifulSoup(self.jsonLine, "lxml")
        tokens = nltk.tokenize.word_tokenize(content.get_text())
        self.compute_frequency(tokens)
    
    
    
    def compute_frequency(self, tokens:list):
        for word in tokens:
            if len(word) >= 2 and word.isalnum():
                self.numOfTerms += 1
                word = word.lower()
                if word in self.wordFrequency:
                    self.wordFrequency[word] += 1
                
                else:
                    self.wordFrequency[word] = 1
                
    
    def write_to_file(self, numFiles, numDir,mode="wfd"):
        path = os.getcwd() + f'/TEMP/DIR{numDir}'
        if mode == "wfd": #Default, must change specification. This portion deals with helping make the wordDocFreq.txt which is used to calculate idf. Only need to call this when wordDocFreq.txt is missing.
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + f'/file{numFiles}.txt', mode="w") as file:
                for i in sorted(self.wordFrequency.keys()):
                    try:
                        file.write(f"{i}|")          
                    except:
                        pass
        else:
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + f'/file{numFiles}.txt', mode="w") as file:
                for i,j in self.wordFrequency.items():
                    value = self.calculate_tfidf(t=j, 
                                            numOfDwithT= self.wordFrequency[j], 
                                            numOfTerms=self.numOfTerms, 
                                            numOfD=57381)
                        
                    pair = (self.url, value)
                    item = [pair]
                    try:
                        file.write(f"{i}|")          
                    except:
                        pass
            
    


                        
    
    def get_wordFrequencies(self):
        return self.wordFrequency
    
    
    
    #Cannot use until total number of documents have been counted for, as well as all words.
    def calculate_tfidf(self, t, numOfDwithT, numOfTerms, numOfD=57381):
        numOfTerms = self.numOfTerms
        if(numOfDwithT == 0):
            numOfDwithT = 1
        tf = t/numOfDwithT
        idf = log10(numOfD/numOfDwithT)
        return tf * idf

    def convert_wordDocFreq(self):
        dict_word_freq = {}
        if os.path.isfile("wordDocFreq.txt"):
            with open("wordDocFreq.txt", "r") as db:
                content = db.read()
                content = content.split("|")
                for count in range(len(content)):
                    val = content[count].rsplit(":", 1)
                    try:
                        dict_word_freq[val[0]] = val[1]
                    except:
                        # prints any errors
                        print(content[count])
                        print(val)
                        #break
            
            print(dict_word_freq)

if __name__ == "__main__":
    content = ContentExtractor()#"https://www.nltk.org/")
    #content.extract_content()
    print(content.convert_wordDocFreq())
    
    
    
    
    
    
    
    
    
    
    
    