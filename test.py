import os
import json
import time
import csv 
from extract_content import ContentExtractor

def getJSONFiles(path: str):
    list_paths = os.listdir(path=path)
    # Goes until the list is empty
    with open('document_idrtf.csv', mode="w", newline='') as file2:
        document = csv.writer(file2, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        while len(list_paths) > 0:
            
            # Checks to see if the next file is json
            if(".json" in list_paths[-1]):
                # Loads the json and prints the url
                with open(list_paths[-1]) as file:
                    data = file.read()
                    obj = json.loads(data)
                    #print()
                    url = obj["url"]
                    webHTML = obj["content"]
                    content = ContentExtractor(jsonLine = webHTML)
                    content.extract_content()
                    
                    document.writerow([url, term, tfidf])
                    list_paths.pop()
            else:
                # Builds the new path using the next directory in the url
                new_path = os.path.join(path, list_paths[-1])
                #print(new_path)
                # Loads the directories and builds the path to that directory
                new_list = []
                for val in os.listdir(path=new_path):
                    new_list.append(os.path.join(new_path, val))
                # deletes the last value then add to the start of the list
                list_paths.pop()
                list_paths += new_list 




if __name__ == "__main__":
    #for i in ["ANALYST", "DEV"]:
    for i in ["SAMPLE"]:
        start = time.time()
        getJSONFiles(os.path.join(os.getcwd(), i))
        end = time.time()
        print(end-start, i, "Brandon")