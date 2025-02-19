import pygame

from visuals.Window import Window
from util.mathextra.Location import Point
class RectHelpers():
    def __init__(self, pos: Point, size: Point):
        self.pos = pos
        self.size = size
        self.__rect_value__ = pygame.Rect(pos.x, pos.y, size.x, size.y)
    def render(self, win: Window, color: pygame.Color):
        pygame.draw.rect(win, color, self.__rect_value__)
    def get_rect(self):
        return self.__rect_value__
    def at(self, pos: Point):
        self.pos = pos
        self.__rect_value__.x = pos.x
        self.__rect_value__.y = pos.y
        return self