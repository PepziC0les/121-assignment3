import os


def buildDocCount():
    dirs = os.listdir(os.getcwd() + "/TEMP")
    path=  os.path.join(os.getcwd(), "TEMP")
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
    os.rmdir(os.getcwd() + "/TEMP")


def buildIndex():
    pass

'''
def buildDocCount():
    count = 0
    dirs = os.listdir(os.getcwd() + "/TEMP")
    path=  os.path.join(os.getcwd(), "TEMP")
    finalDict = dict()
    #buffer1 = ""
    for i in dirs:
        finalDict.update(mitigateDict(i, path, count))
        count += 1
    with open("wordDocFreq.txt", "w") as file:
        for i,j in sorted(finalDict.items()):
            file.write(f"{i}:{j}|")
    os.rmdir(os.getcwd() + "/TEMP")


def mitigateDict(i, path, count):
    partialDict = dict()
    for k in os.listdir(os.path.join(path,i)):
        with open(os.path.join(path,i,k), "r", buffering=1) as file2:
            items = file2.read().strip("|").split("|")
            for j in items:
                try:
                    if j in finalDict:
                        partialDict[j] += 1
                    else:
                        partialDict[j] = 1
                except:
                    pass 
        os.remove(os.path.join(path,i,k))
    os.rmdir(os.path.join(path,i))
    print(partialDict)
    return partialDict
    #with open(os.path.join(path, f"temp_dict{count}.txt"), "w") as file:
        #for i,j in sorted(paritalDict.items()):
            #file.write(f"{i}:{j}|")
    
'''
'''
            while True:
                try:
                    c = file2.read(1)
                    if not c:
                        break
                    if c == "|":
                        if buffer1 in finalDict:
                            finalDict[buffer1] += 1
                        else:
                            finalDict[buffer1] = 1
                        print(buffer1, finalDict[buffer1])
                        buffer1 = ""
                    else:
                        buffer1 += c
                except:
                    pass
            '''
    
'''
with open(path + i, "r", buffering=1) as file2:
            items = file2.read().strip("|").split("|")
            for j in items:
                try:
                    if j in finalDict:
                        finalDict[j] += 1
                    else:
                        finalDict[j] = 1
                except:
                    pass
    os.remove(path + i)
    pass

'''    
    
    
    
    
    
    
    
    
    
    
    