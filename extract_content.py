import re
#from nltk.tokenize import ToktokTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize, pos_tag
import requests
from bs4 import BeautifulSoup
from math import log10


class ContentExtractor:
    def __init__(self, url):
        self.url = url
        self.wordFrequency = dict()
        self.tfIdMappings = dict()
        self.contentBlocks = []
        self.mostFrequentWord = ("", 0)
        self.size = 0
        

    def extract_content(self):
        page = requests.get(self.url)    
        tokenized = RegexpTokenizer(r"\w+")
        content = BeautifulSoup(page.content, features="lxml")
    
        for i in content.find_all(['a', 'p', 'tb', 'body', re.compile('^h[1-6]$'), ]):
            line = i.get_text(strip=True)
            for sent in sent_tokenize(line):
                tokens = pos_tag(tokenized.tokenize(sent))
                if len(tokens) != 0:
                    self.contentBlocks.extend(tokens)
                    self.compute_frequency(tokens)
                    
    
    
    
    def compute_frequency(self, tokens:list):
        for word in tokens:
            self.size += 1
            word = word[0].lower()
            if len(word) >= 2:
                if word in self.wordFrequency:
                    self.wordFrequency[word] += 1
                else:
                    self.wordFrequency[word] = 1
                
                #print(self.wordFrequency[word], self.mostFrequentWord[1])
                if self.wordFrequency[word] > self.mostFrequentWord[1]:
                    self.mostFrequentWord = (word, self.wordFrequency[word])
    
    
    def tf_idf_score(self, word):
        tf = log10(1 + self.wordFrequency[word])
        #idf = log10(self.size/)


content = ContentExtractor("https://www.nltk.org/")
content.extract_content()
print(content.mostFrequentWord)