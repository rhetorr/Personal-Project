import pygame
class RectHelpers:
    
    def __init__(self, size: tuple):
        self.__size__=size
        self.__coords__= (-100,-100)
        self._rect_ = pygame.Rect(self.__coords__[0], self.__coords__[1], size[0], size[1])
        self.__color__ = "red"
    def render(self, win):
        self._rect_ = pygame.draw.rect(win, self.__color__, self._rect_)
        return self
    def with_color(self, color):
        self.__color__ = color
        return self
    def at(self, x, y):
        self.__coords__ = (x,y)
        self._rect_ = pygame.Rect(self.__coords__[0], self.__coords__[1], self.__size__[0], self.__size__[1])
        return self
    def with_size(self, width, height):
        self.__size__ = (width, height)
        self._rect_ = pygame.Rect(self.__coords__[0], self.__coords__[1], self.__size__[0], self.__size__[1])
        return self
