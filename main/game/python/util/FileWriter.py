#write in files with a format, for saveable progress
import os

def __delete_until(string: str, substring: str):
    list = string.split(substring)
    new = ""
    for i in list:
        if i == list[-1]:
            break
        new = new + i + substring
    return new

class File:
    def __init__(self, file_name: str):
        pack = __delete_until(__file__, '\\')
        
        self.file_name = file_name
        self.__file_path =  pack + file_name
        
    def withPath(self,directory):
        self.__file_path = directory + self.file_name
        return self
    
    def make(self):
        self.file_name += '.txt'
        self.__file_path += '.txt'
        self.__file_descriptor = os.open(self.__file_path, os.O_CREAT)
        os.close(self.__file_descriptor)
        return self

    def write(self, text: list[str]):
        os.open(self.__file_path, os.O_RDWR)
        for txt in text:
            line = str.encode(txt + "\n")
            
            os.write(self.__file_descriptor, line)
            
    def close(self):
        os.close(self.__file_descriptor)
        return self
        
class Folder:
    def __init__(self, folder_name: str):
        pack = __delete_until(__file__, '\\')
        
        self.folder_name = folder_name
        self.__folder_path = pack
        
    def make(self):
        file = os.path.join(self.__folder_path, self.folder_name)
        if os.path.exists(file):
            return
        os.mkdir(file)
        return self
    
    def withPath(self, path):
        self.__folder_path = path
        return self