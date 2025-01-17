
@staticmethod
class Point:
    def __init__(self, x:float, y:float):
        self.__x = x
        self.__y = y
        
    def X(self):
        return self.__x
    def Y(self):
        return self.__y
    def translate(self, other):
        self.__x += other.__x
        self.__y += other.__y
    

class Orientation:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle