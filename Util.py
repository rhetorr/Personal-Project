import time
import enum
import Constants
import os
from FileWriter import File
from FileWriter import Folder

@enum.unique
class Directions(enum.Enum):
    NORTH = "NORTH"
    NORTHEAST = "NORTHEAST"
    EAST = "EAST"
    SOUTHEAST = "SOUTHEAST"
    SOUTH = "SOUTH"
    SOUTHWEST = "SOUTHWEST"
    WEST = "WEST"
    NORTHWEST = "NORTHWEST"
    CENTER = "CENTER"

class TileImages:
    def directioned(self, generic_name, direction: Directions):
        return generic_name + "_" + direction.value + ".png"
    
    def grass(self, direction: Directions):
        return "assets/tiles/grasses/" + self.directioned("GRASS", direction)
    

class Tile:
    def __init__(self):
        self.walkable = True
        self.name = '-'
        
    def walk(self, walkable: bool):
        self.walkable = walkable
        return self
    
    def withName(self, name:str):
        self.name = name
        return self
    
@enum.unique
class Tiles(enum.Enum):
    null = Tile().walk(True).withName('-')
    grass = Tile().walk(True).withName('^')
    wood = Tile().walk(True).withName('=')
    water_deep = Tile().walk(False).withName('_')
    water_shallow = Tile().walk(True).withName('m')
    floor = Tile().walk(True).withName('f')
    

class Stopwatch:
    def __init__(self):
        self.start_timestamp = time.time()
        self.running = False
        self.end_timestamp = time.time()
    
    def reset(self):
        self.running = True
        self.start_timestamp = time.time()
        self.end_timestamp = time.time()
        return self
    
    def end(self):
        self.end_timestamp = time.time()
        self.running = False
        return self
    
    def get(self):
        self.end_timestamp = time.time()
        return self.end_timestamp - self.start_timestamp
    
    def elapsed(self, seconds):
        return (self.get() >= seconds)
    
class Frame():
    def __init__(self):
        self.size = 12
        self.grid = [[Tiles.null]*self.size] * self.size
        
    def fill(self, type: Tiles):
        self.grid = [[type]*self.size] * self.size
        return self
    
    def insert(self, x,y, type: Tiles):
        self.grid[x][y] = type
        return self
        
    def accept(self, grid):
        self.grid = grid
        return self
    
    def format(self):
        listed = [['-']*self.size]*self.size
        formatted = []
        for i in range(self.size):
            for j in range(self.size):
                listed[i][j] = self.grid[i][j].value.name
        for i in listed:
            formatted.append(string_list_join(i))
        return formatted
    
class World():
    def __init__(self, name: str):
        self.size = 10
        self.name = name
        self.chunks = [[Frame().fill(Tiles.null)]*self.size]*self.size
        Folder(self.name).withPath('worlds').make()
    
    def fill(self, type: Tiles):
        self.chunks = [[Frame().fill(type)]*(self.size)]*(self.size)
        return self
    
    def accept(self, new):
        self.chunks = new
        return self
    
    def save(self):
        writer = File('chunks').withPath(Constants._WORLDS_PATH+self.name+'/').make()
        
        writer.write([self.name,'/'])
        for i in self.chunks:
            for j in i:
                line = j.format()
                line.append('/')
                writer.write(line)
        writer.close()
        return self
    
def string_list_join(list: list[str])->str:
    newstring = ''
    for i in range(len(list)):
        newstring += list[i]
    return newstring

def get_worlds():
    return os.listdir('worlds')