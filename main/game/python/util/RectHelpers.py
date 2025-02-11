import pygame
class RectHelpers():
    def __init__(self, x, y, width, height):
        self.__rect_value__ = pygame.Rect(x, y, width, height)
    def render(self, win: pygame.Surface, color: pygame.Color):
        pygame.draw.rect(win, color, self.__rect_value__)
    def get_rect(self):
        return self.__rect_value__