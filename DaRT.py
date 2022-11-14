import tkinter as tk
import os, sys, hashlib
from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from zipfile import ZipFile
import os.path
import time

def dropFunction(event):
   #Parse list of files (might be more than one)
   ######## Does not currently handle spaces in the filepath or filename
   dropList = event.data.split(' ')
   
   for filePath in dropList:
       if os.path.isfile(filePath):
           if filePath.split(os.sep)[-1].endswith('.dart'):
               assemble(filePath)
           else:
               disassemble(filePath)
       else:
           print('Error: Path may contain spaces')
   
def disassemble(filePath):
   print("Disassemble File: " + filePath)
   
   file = open(filePath, "rb")
   numberOfDivisions = int(piecesText.get())

   allBytes = file.read()

   result = [allBytes[i::numberOfDivisions] for i in range(numberOfDivisions)]

   #Output Split Files
   partialFileList = []
   for i in range(len(result)):
       partialFilename = filePath + '_partial_' + str(i)
       fileOutput = open(partialFilename, 'wb')
       fileOutput.write(result[i])
       fileOutput.close()
       partialFileList.append(partialFilename)
    
       metaFilename = filePath + '_hashes.txt'
       metaOutput = open(metaFilename, 'a')
       metaOutput.write(partialFilename.split(os.sep)[-1] + ": " + hashlib.md5(result[i]).hexdigest() + "\n") 
       metaOutput.close()
    
       with ZipFile(filePath + '.dart',"w") as newzip:
           for partial in partialFileList:
               while not os.path.exists(partial):
                   time.sleep(1)
               newzip.write(partial.split(os.sep)[-1]) #Splitings prevents nested folder structure in zip
           newzip.write(metaFilename.split(os.sep)[-1])

   #Cleanup Tempfiles        
   for part in partialFileList:
       os.remove(part)
   os.remove(metaFilename)
   
   print('Disassembly Complete')
   #--------------------------------------------------------------
   
def assemble(filePath):
   print("Reconstruct File: " + filePath)
   
   #Unzip Files
   with ZipFile(filePath, 'r') as inputZip:
       inputZip.extractall('.')

   baseFilename = filePath.split('.dart')[0]

   #Read In Files
   count = 0
   result = []
   partialFileList = []
   metaFilename = baseFilename + '_hashes.txt'
   while True:
       try:
           partialFilename = baseFilename + '_partial_' + str(count)
           file = open(partialFilename, "rb")
           allBytes = list(file.read())
           result.append(allBytes)
           partialFileList.append(partialFilename)
           file.close()
           count = count + 1
       except:
           break
        
   #Cleanup Tempfiles        
   for part in partialFileList:
       os.remove(part)
   os.remove(metaFilename)

   #Join Files
   finalResult = []
   count = 0
   while True:
       try:
           for i in range(len(result)):
               finalResult.append(result[i][count])
           count = count + 1
       except:
           break

   #Output Joined Files
   fileOutput = open(baseFilename, 'wb')
   fileOutput.write(bytes(finalResult))
   fileOutput.close()
   
   print('Reconstruction Complete')
   #--------------------------------------------------------------

def fileSelectButton():
   selectedFilepath = filedialog.askopenfilename(initialdir = '.' ,title = "Select File...")
   if selectedFilepath:
       if selectedFilepath.split(os.sep)[-1].endswith('.dart'):
           assemble(selectedFilepath)
       else:
           disassemble(selectedFilepath)

def create_circle(x, y, r, canvasName, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color)

root = TkinterDnD.Tk()

root.title("DaRT")
root.geometry("200x225")
root.resizable(0, 0)

myCanvas = Canvas(root)
myCanvas.pack()

create_circle(100, 100, 80, myCanvas, 'black')
create_circle(100, 100, 75, myCanvas, 'red')
create_circle(100, 100, 60, myCanvas, 'white')
create_circle(100, 100, 45, myCanvas, 'red')
create_circle(100, 100, 30, myCanvas, 'white')
create_circle(100, 100, 15, myCanvas, 'red')

buttonText = StringVar()
buttonText.set('Drop Files Here...')
fileSelectButton = Button(root, textvariable=buttonText, borderwidth=0, command=fileSelectButton)
fileSelectButton.place(x=40,y=196)

piecesText = StringVar()
piecesEntry = Entry(root,width=2,textvariable=piecesText, borderwidth=0)
piecesEntry.place(x=5,y=200)
piecesText.set('4')

myCanvas.drop_target_register(DND_FILES)
myCanvas.dnd_bind('<<Drop>>', dropFunction)

root.mainloop()
