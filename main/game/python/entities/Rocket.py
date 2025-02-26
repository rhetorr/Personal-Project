import pygame
from util.mathextra.Location import Angle, Orientation, Point
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class Rocket():
    def __init__(self, window:pygame.Surface, size: Point, res_scalar: Point, fuel_usage: float):
        self.size = size.times(res_scalar)
        self.__window__ = window
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self.rocket = self.i_h.resize(self.i_h.get("rocket.png"), self.size)
        self.__rocket_angle__ = Angle.in_degrees(0)
        
        self.pos: Orientation = Orientation.init(size.negate().minus(Point.fill(100)), Angle.in_degrees(0))
        self.fuel = 100
        self.fuel_usage = fuel_usage 
    def render(self):
        self.rocket = self.i_h.rotate(self.rocket, self.pos.angle.minus(self.__rocket_angle__))
        self.__rocket_angle__ = self.pos.angle
        self.__window__.blit(self.rocket, self.pos.get_point().tuple())
    def at(self, pos: Point):
        self.pos = Orientation.init(pos, self.pos.angle)
        return self
    def move_x(self, amount: float):
        self.pos.x += amount
        return self
    def move_y(self, amount: float):
        self.pos.y += amount
        return self
    def move(self, amount: Point):
        self.pos = self.pos.translate_by(amount)
        return self
    def face(self, angle: Angle):
        self.pos.angle = angle
        return self
    def fuel_up(self, amount: float):
        self.fuel += amount