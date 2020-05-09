import os
import json


def buildDocCount():
    path = os.path.join(os.getcwd(), "TEMP")
    dirs = os.listdir(path)
    finalDict = dict()
    #buffer1 = ""
    for i in dirs:
        for k in os.listdir(os.path.join(path,i)):
            with open(os.path.join(path,i,k), "r", buffering=1) as file2:
                items = file2.read().strip("|").split("|")
                for j in items:
                    try:
                        if j in finalDict:
                            finalDict[j] += 1
                        else:
                            finalDict[j] = 1
                    except:
                        pass 
            os.remove(os.path.join(path,i,k))
        os.rmdir(os.path.join(path,i))
    with open("wordDocFreq.txt", "w") as file:
        for i,j in sorted(finalDict.items()):
            file.write(f"{i}:{j}|")
    os.rmdir(path)

    
def buildIndex(finalIndexFd:str):
    path = os.path.join(os.getcwd(), "TEMP")
    dirs = os.listdir(path)
    index = dict()
    for url_data_fd in dirs:
        with open(url_data_fd) as url_file:
            json_data = json.loads(url_file)
            for word in json_data:
                if word in index:
                    index[word].extend(json_data[word])
                else:
                    index[word] = json_data[word]
        os.remove(url_data_fd)
    
    with open(finalIndexFd, "w") as index_file:
          index_file.write(json.dumps(index))
        
    os.rmdir(path)
        
    
    

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