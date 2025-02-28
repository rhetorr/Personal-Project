import pygame
from GameStates import GameStates
from util.mathextra.Location import Angle, Point
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers

class Sprite(RectHelpers):
    def __init__(self, window:pygame.Surface, size: Point):
        super().__init__(size.negate().minus(Point.fill(100)), size)
        super().__delattr__("__rect_value__")
        self.sprite = pygame.surface.Surface(size.tuple())
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        self.__window__ = window
        self.size.with_mid(Point(self.__window__.get_width(), self.__window__.get_height()))
    def with_image(self, name, rotation: Angle = Angle.in_degrees(0)):
        raw = self.i_h.get(name)
        self.sprite = self.i_h.resize(self.i_h.rotate(raw, rotation), self.size)
        return self
    def render(self):
        self.__window__.blit(self.sprite, self.pos.tuple())
    def at(self, pos: Point):
        self.pos = pos
        return self
    def move_y(self, amount: float):
        self.at(self.pos.plus(Point(0, amount)))
        return self