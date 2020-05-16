import os
import json


def buildDocCount():
    path = os.path.join(os.getcwd(), "TEMP")
    #print(path)
    dirs = os.listdir(path)
    #print(dirs)
    finalDict = dict()
    #buffer1 = ""
    for i in dirs:
        #print(i)
        #for k in os.listdir(os.path.join(path,i)):
        with open(os.path.join(path,i), "r", buffering=1) as file2:
            items = file2.read().strip("|").split("|")
            for j in items:
                try:
                    if j in finalDict:
                        finalDict[j] += 1
                    else:
                        finalDict[j] = 1
                except:
                    pass 
        os.remove(os.path.join(path,i))
        #os.rmdir(os.path.join(path,i))
    with open("wordDocFreq.txt", "w") as file:
        for i,j in sorted(finalDict.items()):
            file.write(f"{i}:{j}|")
    os.rmdir(path)

    
def buildIndex(finalIndexFd:str):
    path = os.path.join(os.getcwd(), "TEMP")
    dirs = os.listdir(path)
    index = dict()
    for url_data_fd in dirs:
        with open(os.path.join(path, url_data_fd)) as url_file:
            data = url_file.read()
            json_data = json.loads(data)
            for word in json_data:
                if word in index:
                    index[word].extend(json_data[word])
                else:
                    index[word] = json_data[word]
        os.remove(os.path.join(path, url_data_fd))
    
    with open(finalIndexFd, "w") as index_file:
          index_file.write(json.dumps(index))
        
    os.rmdir(path)

def buildDocIDs():
    path = os.path.join(os.getcwd(), "docID_to_url.txt")
    out_path = os.path.join(os.getcwd(), "docID_url.json")
    with open(path) as input:
        with open(out_path, "w") as docIDs:
            docID_dict = dict()
            values = input.read().split("||")
            for val in values[:-1]:
                id, url = val.split("=>")
                docID_dict[id] = url
            json.dump(docID_dict, docIDs, ensure_ascii=False)
    os.remove(path)
            
    
    

# def buildIndex(tempJsonFd:str, newTempDict:dict) -> dict:
#     """
#     @parameter - tempJsonFd: a buffer
#     @parameter - newTempDict: 
#     """
#     with open('tempJsonFd', 'rw', buffering=1) as json_file:
#         jsonBuf = json.loads(json_file)
#         json_file.seek(0)
#         json_file.truncate()
#         for word in newTempDict:
#             if word in jsonBuf:
#                 jsonBuf[word].extend(newTempDict[word])
#             else
#                 jsonBuf[word] = newTempDict[word]
#         json.dumps(jsonBuf)
    
#     return dict()