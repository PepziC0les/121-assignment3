import re
#from nltk.tokenize import ToktokTokenizer
import shelve
import csv
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize, pos_tag
import requests #Requests optional, content already in JSON files.
from bs4 import BeautifulSoup
from math import log10


class ContentExtractor:
    def __init__(self, url=None, path=None, jsonLine="", writeLoc=None):
        self.jsonLine = jsonLine
        self.writeLoc = writeLoc
        self.url = url
        self.file = path
        self.wordFrequency = dict()
        self.tfIdMappings = dict()
        self.contentBlocks = []
        self.mostFrequentWord = ("", 0)
        self.numOfTerms = 0
        


    def extract_content(self):
        #page = requests.get(self.url)    
        tokenized = RegexpTokenizer(r"\w+")    
        #self.jsonLine = ""
        #with open(self.jsonFile, "r") as file:
        #    data = file.read()
        #    obj = json.loads(data)
        #    jsonLine = obj["content"]
        content = BeautifulSoup(self.jsonLine, features="lxml")
        
        for i in content.find_all(['a', 'p', 'tb', 'body', re.compile('^h[1-6]$'), ]):
            line = i.get_text(strip=True)
            for sent in sent_tokenize(line):
                tokens = pos_tag(tokenized.tokenize(sent))
                if len(tokens) != 0:
                    self.contentBlocks.extend(tokens)
                    self.compute_frequency(tokens)
    
    
    
    def compute_frequency(self, tokens:list):
        for word in tokens:
            self.numOfTerms += 1
            word = word[0].lower()
            if len(word) >= 2:
                with shelve.open("WORDDB", "w") as db:
                    if word in self.wordFrequency:
                        self.wordFrequency[word] += 1
                
                    else:
                        self.wordFrequency[word] = 1
                
                    if self.wordFrequency[word] > self.mostFrequentWord[1]:
                        self.mostFrequentWord = (word, self.wordFrequency[word])
    
                    if word in db:
                        db[word] += 1
                    else:
                        db[word] = 1

        
        

    def write_to_file(self, url, tfidf, term):
        with open('document_idrtf.csv', mode="w", newline='') as file:
            document = csv.writer(file, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
            document.writerow([url, term, tfidf])
    
    
    def map_tfidf_term(self):
        mappings = []
        for i,j in self.tfIdMappings.items():
            mappings.append(i, self.calculate_tfidf(t=i, ))
    
    #Cannot use until total number of documents have been counted for, as well as all words.
    def calculate_tfidf(t, numOfDwithT, numOfTerms=self.numOfTerms, numOfD=57381):
        numOfDinA = 1988
        numOfDinD = 55393
        tf = t/numOfDwithT
        idf = math.log10(numOfD, numOfDwithT)
        return tf * idf


if __name__ == "__main__":
    content = ContentExtractor("https://www.nltk.org/")
    content.extract_content()
    print(content.mostFrequentWord)
    
    
    
    
    
    
    
    
    
    
    
    