#write in files with a format, for saveable progress
import os

def delete_until(string: str, substring: str):
    list = string.split(substring)
    new = ""
    for i in list:
        if i == list[-1]:
            break
        new = new + i + substring
    return new

class File:
    def __init__(self):
        pack = delete_until(__file__, '\\')
        self.__file_path = pack
        self.__file_name = ""
        
    def make(self, file_name: str):
        self.__file_name = file_name
        file = os.path.join(self.__file_path, self.__file_name)
        if os.path.exists(file):
            return
        open(file, 'w').close()
        return self

    def delete_file_text(self):
        file = os.path.join(self.__file_path, self.__file_name)
        with open(file, 'w') as f:
            f.write("")
        return self
            
    def append(self, text: list[str]):
        file = os.path.join(self.__file_path, self.__file_name)
        with open(file, 'a') as f:
            for i in text:
                f.write(i)
                if not i == text[-1]:
                    f.write("\n")
        return self

    def write(self, text: list[str]):
        self.delete_file_text()
        self.append(text)
        return self
    
    def read(self):
        file = os.path.join(self.__file_path, self.__file_name)
        with open(file, 'r') as f:
            return f.read()
        
class Folder:
    def __init__(self, folder_name: str):
        pack = delete_until(__file__, '\\')
        
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
    
class Map:
    def __init__(self, *chars: tuple[object, object]):
        self.chars = chars
        
    def add(self, *chars: tuple[object, object]):
        self.chars = self.chars + chars
        
    def get(self, input: object):
        for i in self.chars:
            if i[0] == input:
                return i[1]
        return None
    
    def get_char(self, input: object):
        for i in self.chars:
            if i[1] == input:
                return i[0]
        return None