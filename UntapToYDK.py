import requests as rq
import unidecode
import time
import json
import tkinter as tk

from tkinter import filedialog
cardDict = {}
ydkDict = {}
types = ["Fusion Monster","XYZ Monster","Synchro Monster"]
def browseFiles():
    fileName = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    parseFile(fileName)

def parseFile(fileName):
    file = open(fileName, "r")

    for line in file:
        line = unidecode.unidecode(line)
        paranthIndex = line.find('(')
        copies = line[0]
        if(paranthIndex > -1):
            #print(paranthIndex)
            nameEndIndex = paranthIndex - 1
            cardName = line[2:nameEndIndex]
            cardDict[cardName] = copies
            #print(cardDict)
        else:
            print(line)
    GrabIdFromDataBase()


def GrabIdFromDataBase():
    totalRequests = 0
    dataBaseUrl = "https://db.ygoprodeck.com/api/v7/cardinfo.php?fname="
    for key in cardDict:
        if(totalRequests < 19):
            result = rq.get(dataBaseUrl+key)
            jsonResult = json.loads(result.text)

            cardID = jsonResult["data"][0]["id"]
            cardType = jsonResult["data"][0]["type"]
            print(cardID)
            print(cardType)
            ydkDict[cardID] = [cardType, cardDict[key]]

            totalRequests = totalRequests + 1
        else:
            totalRequests = 0
            time.sleep(2)
    createYDKFile()

def createYDKFile():
    ydkFile = open("NewYDK.txt", "x")
    ydkFile.write("#created by UntapToYDK\n")
    ydkFile.write("#main\n")
    addToExtra = []
    for key in ydkDict:
        copies = int(ydkDict[key][1])
        if(ydkDict[key][0] not in types):
            while(copies > 0):
                ydkFile.write(str(key)+'\n')
                copies = copies - 1
            print(str(key))
        else:
            while(copies > 0):
                addToExtra.append(key)
                copies = copies - 1

    ydkFile.write("#extra\n")
    for id in addToExtra:
        ydkFile.write(str(id)+'\n')
        print(str(id))
    ydkFile.write("!side\n")


window = tk.Tk()

window.title("Convert Shitty Untap txt to YDK")


fileExplorerLabel = tk.Label(window, text="Select the txt file Downloaded from Untap", width = 100, height = 4)


openFileButton = tk.Button(window, text = "Browse Files", command = browseFiles)

fileExplorerLabel.grid(column = 0, row = 0)

openFileButton.grid(column = 0, row = 1)


# Let the window wait for any events
window.mainloop()
