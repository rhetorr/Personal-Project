import pygame
import VisualsUtil

class Sprite(pygame.rect):
    def __init__(self, size: tuple):
        self.size = size
    def from_image(self, dims, name):
        pygame.transform.scale(pygame.image.load(VisualsUtil._ASSETS_PATH+name), dims)
        return self