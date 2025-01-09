#write in files with a format, for saveable progress
import os

def deleteUntil(string: str, substring: str):
    lista = string.split(substring)
    new = ""
    for i in lista:
        if i == lista[-1]:
            break
        new = new + i + substring
    return new

class File:
    def __init__(self, filename: str):
        pack = deleteUntil(__file__, '\\')
        
        self.filename = filename
        self.filepath =  pack + filename
        
    def withPath(self,directory):
        self.filepath = directory + self.filename
        return self
    
    def make(self):
        self.filename += '.txt'
        self.filepath += '.txt'
        self.file_descriptor = os.open(self.filepath, os.O_CREAT)
        os.close(self.file_descriptor)
        return self

    def write(self, text: list[str]):
        os.open(self.filepath, os.O_RDWR)
        for txt in text:
            line = str.encode(txt + "\n")
            
            os.write(self.file_descriptor, line)
            
    def close(self):
        os.close(self.file_descriptor)
        return self
        
class Folder:
    def __init__(self, foldername: str):
        pack = deleteUntil(__file__, '\\')
        
        self.foldername = foldername
        self.path = pack
        
    def make(self):
        file = os.path.join(self.path, self.foldername)
        if os.path.exists(file):
            return
        os.mkdir(file)
        return self
    
    def withPath(self, path):
        self.path = path
        return self