import requests as rq
import unidecode
import time
import json
import tkinter as tk
import concurrent.futures as cf
from tkinter import filedialog



def browseFiles():
    fileName = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"),("all files","*.*")))
    fileNameLabel = tk.Label(window, text="File selected: " + fileName, width = 100, height = 4)
    fileNameLabel.grid(column = 0, row = 2)

    transformFileButton = tk.Button(window, text = "Load data from Untap File and YGOPRO database", command = lambda: parseFile(fileName))
    transformFileButton.grid(column = 0, row = 3)
    window.event_generate("<<OnBroweComplete>>")

def parseFile(fileName):
    progressLabel.grid(column = 0, row = 4)
    with open(fileName, "r") as file:
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
    window.event_generate("<<OnParseComplete>>")
    #GrabIdFromDataBase()

def GrabIdFromDataBase(key):
    dataBaseUrl = "https://db.ygoprodeck.com/api/v7/cardinfo.php?fname="
    result = rq.get(dataBaseUrl+key)
    try:
        jsonResult = json.loads(result.text)
        cardID = jsonResult["data"][0]["id"]
        cardType = jsonResult["data"][0]["type"]
    except:
        print("An error occurred")
        errorWindow = tk.Tk()
        errorWindow.title("Error!!")
        errorMsg = tk.Label(errorWindow, text="An error occurred. It was probably a response from YGOPRO blocking your IP for making too many requests. If you have a VPN fire it up otherwise wait around for an hour and re-run?", width= 100, height=25)
        errorMsg.pack()

    print(cardID)
    #print(cardType)
    ydkDict[cardID] = [cardType, cardDict[key]]
    window.event_generate("<<OnDataGrabComplete>>")



def createYDKFile(nameForFile):
    ydkFile = open(nameForFile+".txt", "x")
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
    ydkFile.close()
    allDone = tk.Label(window, text="ALL OPERATIONS COMPLETE", width = 100, height = 4)
    allDone.grid(column = 0, row = 7)

def do_browse_complete(some):
    print("Browse complete")

def do_parse_complete(some):
    print("Parse complete")
    print("Doing a threading")

    with cf.ThreadPoolExecutor(max_workers=2) as executor:
        futuresFromDatabase = {executor.submit(GrabIdFromDataBase, key): key for key in list(cardDict.keys())}

    progressLabel.config(text="Download from YGOPRO database Complete")
    fileNameInput = tk.Label(window, text="Enter File Name: ", width = 100, height = 4)
    fileNameInput.grid(column = 0, row = 5)

    nameForYDKFile = tk.Entry(window)
    nameForYDKFile.grid(column = 1, row = 5)

    generateFileButton = tk.Button(window, text = "Generate YDK File", command = lambda: createYDKFile(str(nameForYDKFile.get())))
    generateFileButton.grid(column = 0, row = 6)

def OnDataGrabComplete(data):
    print("Grabbed One")
    progress = ""
    for i in databaseProgress:
        progress = progress + "#"
    progressLabel.config(text=progress)

def main():
    global cardDict
    cardDict = {}
    global ydkDict
    ydkDict = {}
    global types
    types = ["Fusion Monster","XYZ Monster","Synchro Monster"]
    global window
    window = tk.Tk()

    window.title("Convert Shitty Untap txt to YDK")
    window.bind("<<OnBrowseComplete>>", do_browse_complete)
    window.bind("<<OnParseComplete>>", do_parse_complete)
    window.bind("<<OnDataGrabComplete>>", OnDataGrabComplete)

    global progressLabel
    progressLabel = tk.Label(window, text="Please Wait...Making calls to YGOPRO database", width = 100, height = 4)
    fileExplorerLabel = tk.Label(window, text="Select the txt file Downloaded from Untap", width = 100, height = 4)

    openFileButton = tk.Button(window, text = "Browse Files", command = browseFiles)


    fileExplorerLabel.grid(column = 0, row = 0)

    openFileButton.grid(column = 0, row = 1)


    # Let the window wait for any events
    window.mainloop()



if __name__ == "__main__":

    main()
