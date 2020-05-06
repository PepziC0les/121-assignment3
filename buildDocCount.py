import shelve

def buildDocCount(wordFrequency):
    with shelve.open("WordDocFreq") as db:
        for word in wordFrequency:
            if word not in db:
                db[word] = 1
            else:
                db[word] += 1


if __name__ == "__main__":
    buildDocCount({"New York City":8550405, "Los Angeles":3971883, "Toronto":2731571, "Chicago":2720546, "Houston":2296224, "Montreal":1704694, "Calgary":1239220, "Vancouver":631486, "Boston":667137})
    buildDocCount({"red" : "rot", "green" : "grün", "blue" : "blau", "yellow":"gelb", "New York City": 1})
    buildDocCount({"A" : ".-", 
                    "B" : "-...", 
                    "C" : "-.-.", 
                    "D" : "-..", 
                    "E" : ".", 
                    "F" : "..-.", 
                    "G" : "--.", 
                    "H" : "....", 
                    "I" : "..", 
                    "J" : ".---", 
                    "K" : "-.-", 
                    "L" : ".-..", 
                    "M" : "--", 
                    "N" : "-.", 
                    "O" : "---", 
                    "P" : ".--.", 
                    "Q" : "--.-", 
                    "R" : ".-.", 
                    "S" : "...", 
                    "T" : "-", 
                    "U" : "..-", 
                    "V" : "...-", 
                    "W" : ".--", 
                    "X" : "-..-", 
                    "Y" : "-.--", 
                    "Z" : "--..", 
                    "0" : "-----", 
                    "1" : ".----", 
                    "2" : "..---", 
                    "3" : "...--", 
                    "4" : "....-", 
                    "5" : ".....", 
                    "6" : "-....", 
                    "7" : "--...", 
                    "8" : "---..", 
                    "9" : "----.", 
                    "." : ".-.-.-", 
                    "," : "--..--"})
   
    with shelve.open("WordDocFreq") as db:
        for i in db:
            print(f"{i} : {db[i]}")