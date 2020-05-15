import re
import json
import ijson
import time
import os

def produce_indexes():
    count = 0
    alphaMapped = {'a': dict(),
                   'b': dict(),
                   'c': dict(),
                   'd': dict(),
                   'e': dict(),
                   'f': dict(),
                   'g': dict(),
                   'h': dict(),
                   'i': dict(),
                   'j': dict(),
                   'k': dict(),
                   'l': dict(),
                   'm': dict(),
                   'n': dict(),
                   'o': dict(),
                   'p': dict(),
                   'q': dict(),
                   'r': dict(),
                   's': dict(),
                   't': dict(),
                   'u': dict(),
                   'v': dict(),
                   'w': dict(),
                   'x': dict(),
                   'y': dict(),
                   'z': dict(),}
    
    print("Begin creating dictionary")
    file2 = open("final_index2.json", "r")
    index = 0
    with open("final_index.json", "r") as file:    
        start = time.time()
        #start2 = time.time()
        beforeStart = 0
        startPos = 0
        endPos = 0
        for prefix, the_type, value in ijson.parse(file):
            #end2 = 0
            if prefix == '' and the_type == 'map_key' and value[0].isalpha():
                
                if file.tell() != endPos:
                    endPos = file.tell()
                else:
                    startPos = beforeStart
                    file2.seek(startPos)
                
                
                
                if(file2.tell() > startPos):
                    file2.seek(startPos)
                blockSize = endPos - startPos
                #if(blockSize > 10^3):
                #    numBlocks = blockSize/(10^3)
                #    remainder = blockSize % (numBlocks*10^3)
                block = file2.read(blockSize)
                    
                try:
                    index = startPos + block.index(f'"{value}')
                    alphaMapped[value[0]][value] = index+1
                    beforeStart = startPos
                    startPos = endPos
                    #end2 = time.time()
                    #print(value, end2-start2)
                except:
                    pass
                #start2=time.time()
        
        
        end=time.time()
        print("Index dict of ptrs finished, begin writing to files. Time taken:", end-start)
    file2.close()
    
    
    
    start = time.time()
    path = os.path.join(os.getcwd(), "PTR")
    os.mkdir(path)
    os.mkdir(os.path.join(path , "JSON"))
    os.mkdir(os.path.join(path , "TXT"))
    for i in "abcdefghijklmnopqrstuvwxyz":
        with open(path + "/JSON/" + i + ".json", "w") as file:
            json.dump(alphaMapped[i], file, ensure_ascii=False)
        with open(path + "/TXT/" + i + ".txt", "w") as file:
            for j in alphaMapped[i]:
                file.write(j +"<=>" + str(alphaMapped[i][j]) + '\n')
    end = time.time()
    print("Writing indexes finished. Time taken: ", end-start)
    
    
def find_key_position(file, value, startPos, endPos):
    #print(value, file.tell(), startPos, endPos)
    pass
        
        
        
    
if __name__ == "__main__":
    
    if os.path.isdir(os.getcwd() + "/PTR/JSON"):
        files = os.listdir(os.getcwd() + "/PTR/JSON")
        for i in files:
            os.remove(os.path.join(os.getcwd(), "PTR", "JSON", i))
        os.rmdir(os.getcwd() + "/PTR/JSON")
    if os.path.isdir(os.getcwd() + "/PTR/TXT"):
        files = os.listdir(os.getcwd() + "/PTR/TXT")
        for i in files:
            os.remove(os.path.join(os.getcwd(), "PTR", "TXT", i))
        os.rmdir(os.getcwd() + "/PTR/TXT")
        os.rmdir(os.getcwd() + "/PTR")
    
    
    
    produce_indexes()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    