import os
import json
import time
import csv 
from test3 import ContentExtractor
from buildDocCount import buildDocCount
import shutil


fileCount = 0
dirCount = 0

def getJSONFiles(path: str):
    print("CURRENT PATH IS: ", path)
    list_paths = os.listdir(path=path)
    global fileCount
    global dirCount
    with open('document_idrtf.csv', mode="w", newline='') as file2:
        while len(list_paths) > 0:
            
            if(".json" in list_paths[-1]):
                with open(list_paths[-1]) as file:
                    data = file.read()
                    obj = json.loads(data)
                    url = obj["url"]
                    webHTML = obj["content"]
                    content = ContentExtractor(url=url, jsonLine = webHTML)
                    content.extract_content()
                    content.write_to_file(numFiles=fileCount, numDir=dirCount)
                    
                    #content.map_tfidf_term() #Used to make inverted index. Do not use with buildDocCount. buildDocCount must be ran first.
                    
                    #buildDocCount(content.get_wordFrequencies()) #Used to build doc counts. Do not use with map_tfidf. 
                    
                    list_paths.pop()
                
            else:
                new_path = os.path.join(path, list_paths[-1])
                new_list = []
                for val in os.listdir(path=new_path):
                    new_list.append(os.path.join(new_path, val))
                list_paths.pop()
                list_paths += new_list 
                
            fileCount += 1
            if fileCount % 4 == 0:
                dirCount += 1

    
    #shutil.rmtree(os.getcwd() + "/TEMP")
    
if __name__ == "__main__":
    #if os.path.isfile(os.getcwd() + "/wordDocFreq.txt"):
    #    os.remove(os.getcwd() + "/wordDocFreq.txt")
    for i in ["ANALYST", "DEV"]: # 
    #for i in ["SAMPLE"]:
    #for i in ["SAMPLE2"]:
        print(f"Working on {i}")
        if not os.path.isdir(os.getcwd() + "/TEMP"):
            os.mkdir(os.getcwd() + "/TEMP")
        start = time.time()
        getJSONFiles(os.path.join(os.getcwd(), i))
        end = time.time()
        print(end-start, i)
    
    #buildDocCount()
    
    
    