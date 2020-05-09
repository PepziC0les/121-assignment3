import os
import json
import time
import csv 
from extract_content_ver2 import ContentExtractor
from buildDocCount import *
import shutil


fileCount = 0
dirCount = 0
wordDocFreq = dict()


def convert_wordDocFreq():
    global wordDocFre
    if os.path.isfile("wordDocFreq.txt"):
        with open("wordDocFreq.txt", "r") as db:
            content = db.read()
            content = content.split("|")
            for count in range(len(content)):
                val = content[count].rsplit(":", 1)
                try:
                    dict_word_freq[val[0]] = val[1]
                except:
                    pass



def getJSONFiles(path: str):
    print("CURRENT PATH IS: ", path)
    list_paths = os.listdir(path=path)
    global fileCount
    global dirCount
    global wordDocFreq
    
    while len(list_paths) > 0:
            
        if(".json" in list_paths[-1]):
            with open(list_paths[-1]) as file:
                data = file.read()
                obj = json.loads(data)
                url = obj["url"]
                webHTML = obj["content"]
                content = ContentExtractor(url=url, jsonLine = webHTML, globalDict=wordDocFreq)
                content.extract_content()
                content.write_to_file(numFiles=fileCount, numDir=dirCount, mode="index")
                    
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




def main():
    #if os.path.isfile(os.getcwd() + "/wordDocFreq.txt"):
    #    os.remove(os.getcwd() + "/wordDocFreq.txt")
    convert_wordDocFreq()
    #for i in ["ANALYST", "DEV"]: # 
    for i in ["SAMPLE"]:
    #for i in ["SAMPLE2"]:
        print(f"Working on {i}")
        if not os.path.isdir(os.getcwd() + "/TEMP"):
            os.mkdir(os.getcwd() + "/TEMP")
        start = time.time()
        getJSONFiles(os.path.join(os.getcwd(), i))
        end = time.time()
        print(end-start, i)
    buildIndex("final_index.json")
    #buildDocCount()
    
    
    
    
    
if __name__ == "__main__":
    main()
    
    
    