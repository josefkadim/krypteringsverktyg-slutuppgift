import os
import argparse

from cryptography.fernet import Fernet 

def pathExists(fileName: str) -> bool:
    isPath = True
    if not os.path.isfile(fileName):
        isPath = False 
        print("[-] File does not exist . . .")
    return isPath

def generateSymetricKeyAsFile(fileName: str) -> None:
    key: Fernet = Fernet.generate_key()
    with open(fileName, "wb+") as fileHandle:
        fileHandle.write(key)

def getKeyFromFile(fileName: str) -> Fernet:
    if not pathExists(fileName): 
        return None
    
    with open(fileName, "rb") as fileHandle:
        return Fernet(fileHandle.read())

def encryptFileUsingKey(key: Fernet, fileName: str) -> None:
    if not pathExists(fileName): 
        return
    
    lines: list = open(fileName, "rb").readlines()
    with open(fileName, "wb+") as fileHandle:
        for line in lines:
            fileHandle.write(key.encrypt(line))
def decryptFileUsingKey(key: Fernet, fileName: str) -> None:
    if not pathExists(fileName):
        return None
    
    lines: list = open(fileName, "rb").readlines()
    with open(fileName, "wb+") as fileHandle:
        for line in lines:
            fileHandle.write(key.decrypt(line))

def initArgparse() -> dict:
    argparsee = argparse.ArgumentParser()
    argparsee.add_argument("-f", "--file", required=True, help="File to target")
    argparsee.add_argument("--symetric-key", required=False, action="store_true", help="Generate a symetric key")
    argparsee.add_argument("--using-key", required=False, help="Use key for target file")
    argparsee.add_argument("-e", "--encrypt", required=False, action="store_true", help="Encrypt target file")
    argparsee.add_argument("-d", "--decrypt", required=False, action="store_true", help="Decrypt target file")
    args = vars(argparsee.parse_args())
    return args

def main():
    args: dict = initArgparse()
    if (args["symetric_key"]):
        generateSymetricKeyAsFile(args["file"])
    elif (args["using_key"]):
        key: Fernet = getKeyFromFile(args["using_key"])
        if (args["encrypt"]):
            encryptFileUsingKey(key, args["file"])
        elif (args["decrypt"]):
            decryptFileUsingKey(key, args["file"])

if __name__ == "__main__":
    main()


