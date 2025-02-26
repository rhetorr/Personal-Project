import random
import pygame
from util.mathextra.Location import Angle, Orientation, Point
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class FuelCell():
    def __init__(self, window:pygame.Surface, size: Point, res_scalar: Point):
        self.size = size.times(res_scalar)
        self.__window__ = window
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self.tank = self.i_h.resize(self.i_h.get("fuel.png"), self.size)
        self.__tank_angle__ = Angle.in_degrees(0)
        self.rect = self.tank.get_rect()
        
        self.pos: Orientation = Orientation.init(size.negate().minus(Point.fill(100)), Angle.in_degrees(0))
        self.fuel = float(random.randint(10, 50))
        self.spawned = False
    def render(self):
        self.tank = self.i_h.rotate(self.tank, self.pos.angle.minus(self.__tank_angle__))
        self.__tank_angle__ = self.pos.angle
        self.rect = self.__window__.blit(self.tank, self.pos.get_point().tuple())
    def spawn(self, xpos: float):
        self.pos = Orientation.init(Point(xpos, -self.size.y), self.pos.angle)
        self.spawned = True
        return self
    def move_y(self, amount: float):
        self.pos.y += amount
        return self
    def face(self, angle: Angle):
        self.pos.angle = angle
        return self
    
    def collided(self, other: pygame.Rect)->bool:
        return self.rect.colliderect(other)
    
    def reset(self):
        self.tank = self.i_h.resize(self.i_h.get("fuel.png"), self.size)
        self.__tank_angle__ = Angle.in_degrees(0)
        self.rect = self.tank.get_rect()
        
        self.pos: Orientation = Orientation.init(self.size.negate().minus(Point.fill(100)), Angle.in_degrees(0))
        self.fuel = float(random.randint(10, 50))
        self.spawned = False
        return self