import os, sys, hashlib
from zipfile import ZipFile
import os.path
import time
import argparse
   
def disassemble(filePath, num):
    print("Disassemble File: " + filePath)
    
    file = open(filePath, "rb")
    numberOfDivisions = num

    allBytes = file.read()

    result = [allBytes[i::numberOfDivisions] for i in range(numberOfDivisions)]

    #Output Split Files
    partialFileList = []
    metaContents = ""
    metaFilename = filePath + '_hashes.txt'
    with ZipFile(filePath + '.dart',"w") as newzip:
        for index, i in enumerate(result):
            partialFilename = filePath + '_partial_' + str(index)
            with newzip.open(os.path.basename(partialFilename), 'w') as f:
                f.write(i)
            metaContents += os.path.basename(partialFilename) + ": " + hashlib.md5(i).hexdigest() + "\n"
            
            
        with newzip.open(os.path.basename(metaFilename), 'w') as metaOutput:
            metaOutput.write(metaContents.encode()) 
        
        print('Disassembly Complete')
   #--------------------------------------------------------------
   
def assemble(filePath):
   print("Reconstruct File: " + filePath)

   outputbaseFilename = filePath.replace('.dart', '')

   with ZipFile(filePath, 'r') as inputZip:
        files = inputZip.namelist()
        result = []
        partialFileList = []
        for file in files:
            if '_hashes.txt' in file:
                baseFilename = file.replace('_hashes.txt', '')
        
        for count in range(0, len(list(filter(lambda x: baseFilename + '_partial_' in x, files)))):
                partialFilename = baseFilename + '_partial_' + str(count)
                
                with inputZip.open(partialFilename, "r") as f:
                    allBytes = list(f.read())
                result.append(allBytes)

        #Join Files
        finalResult = []
        for x in range(len(result[0])):
            for i in result:
                if len(i) > x:
                    finalResult.append(i[x])

        #Output Joined Files
        with open(outputbaseFilename, 'wb') as f:
            f.write(bytes(finalResult))
        
        print('Reconstruction Complete')
   #--------------------------------------------------------------


def run_dart(args):
    if args.command == 'disassemble':
        if os.path.isdir(args.file_path):
            for path in os.listdir(args.file_path):
                disassemble(os.path.join(args.file_path, path), args.num_parts)
        else:
            disassemble(args.file_path, args.num_parts)
    elif args.command == 'assemble':
        if os.path.isdir(args.file_path):
            for path in os.listdir(args.file_path):
                assemble(os.path.join(args.file_path, path))
        else:
            assemble(args.file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['disassemble', 'assemble'])
    parser.add_argument('file_path')
    parser.add_argument('--num_parts', type=int, default=4)

    args = parser.parse_args()
    run_dart(args)