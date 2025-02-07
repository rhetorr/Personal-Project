import pygame
import VisualsUtil
from main.game.python.util import RectHelpers

class Sprite(pygame.rect):
    def __init__(self, size: tuple):
        self.size = size
        self.sprite = pygame.surface.Surface(size)
    def from_image(self, name):
        self.sprite = pygame.transform.scale(pygame.image.load(VisualsUtil._ASSETS_PATH+name), self.size)
        return self
    def from_rect(self, rect_helper: RectHelpers):
        return self