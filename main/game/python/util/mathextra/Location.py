import math

class Point:
    def __init__(self, x:float, y:float):
        self.__x = x
        self.__y = y
        
    def X(self):
        return self.__x
    def Y(self):
        return self.__y
    def plus(self, other):
        self.__x += other.__x
        self.__y += other.__y
        return self
        
class Angle:
    def __init__(self):
        self.rad = 0.0
        self.deg = 0.0
        self.rot = 0.0
        
    def inRadians(self, rad: float):
        self.rad = rad
        self.deg = math.degrees(rad)
        self.rot = rad/(math.pi*2.0)
        
    def inDegrees(self, deg: float):
        self.deg = deg
        self.rad = math.radians(deg)
        self.rot = deg/360.0
        
    def inRotations(self, rot: float):
        self.rot = rot
        self.deg = rot*360.0
        self.rad = rot*(math.pi*2.0)
        
    def plus(self, other):
        self.rad += other.rad
        self.deg += other.deg
        self.rot += other.rot
        return self
    
    def cos(self):
        return math.cos(self.rad)
    def sin(self):
        return math.sin(self.rad)
    def tan(self):
        return math.tan(self.rad)
    
    def acos(self):
        return math.acos(self.rad)
    def asin(self):
        return math.asin(self.rad)
    def atan(self):
        return math.atan(self.rad)
    

class Orientation:
    def __init__(self, x: float, y: float, angle: Angle):
        self.x = x
        self.y = y
        self.angle = angle
    def __init__(self, coords: Point, angle: Angle):
        self.x = coords.X()
        self.y = coords.Y()
        self.angle = angle
    
    def get_point(self) -> Point:
        return Point(self.x, self.y)
    def get_angle(self) -> Angle:
        return self.angle
    
    def translate_by(self, new: Point):
        Point(self.x, self.y).plus(new)
        return self
    def rotate_by(self, new: Angle):
        self.angle.plus(new)
        return self
    def plus(self, other):
        self.translate_by(other.get_point())
        self.rotate_by(other.get_angle())
        return self