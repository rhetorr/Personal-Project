
import pygame


class Window(pygame.Surface):
    def __init__(self, width:int,height:int):
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.surface_value = pygame.display.set_mode((width, height), vsync=1)
    
    def set_icon(self, icon: pygame.Surface):
        pygame.display.set_icon(icon)
    def set_caption(self, caption: str):
        pygame.display.set_caption(caption)