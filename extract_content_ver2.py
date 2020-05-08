import re
import csv
import nltk
import os
from bs4 import BeautifulSoup
from math import log10
from buildDocCount import buildDocCount


class ContentExtractor:
    def __init__(self, url=None, path=None, jsonLine="", writeLoc=None):
        self.jsonLine = jsonLine
        self.writeLoc = writeLoc
        self.url = url
        self.wordFrequency = dict()
        self.numOfTerms = 0
        


    def extract_content(self):
        content = BeautifulSoup(self.jsonLine, "lxml")
        tokens = nltk.tokenize.word_tokenize(content.get_text())
        self.compute_frequency(tokens)
    
    
    
    def compute_frequency(self, tokens:list):
        for word in tokens:
            if len(word) >= 2:
                self.numOfTerms += 1
                word = word.lower()
                if word in self.wordFrequency:
                    self.wordFrequency[word] += 1
                
                else:
                    self.wordFrequency[word] = 1
                
    
    def write_to_file(self, numFiles, numDir,mode="wfd"):
        if mode == "wfd":
            path = os.getcwd() + f'/TEMP/DIR{numDir}'
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + f'/file{numFiles}.txt', mode="w") as file:
                for i in sorted(self.wordFrequency.keys()):
                    try:
                        file.write(f"{i}|")          
                    except:
                        pass
    
    def map_tfidf_term(self):
        with shelve.open("inverted_index_db", writeback=True) as db1:
            with shelve.open("WordDocFreq") as db2:
                for i,j in self.wordFrequency.items():
                    value = self.calculate_tfidf(t=j, 
                                                 numOfDwithT=db2[i], 
                                                 numOfTerms=self.numOfTerms, 
                                                 numOfD=57381)
                        
                    pair = (self.url, value)
                    item = [pair]
                    try:
                        db1[i] = db1[i] + item
                    except:
                        db1[i] = item
                  
                        
    
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


if __name__ == "__main__":
    content = ContentExtractor("https://www.nltk.org/")
    content.extract_content()
    print(content.mostFrequentWord)
    
    
    
    
    
    
    
    
    
    
    
    