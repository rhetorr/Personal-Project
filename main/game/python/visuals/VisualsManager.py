import pygame


from GameState import GameState
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class VisualsManager:
    def __init__(self, resolution: tuple, caption: str, icon_filename: str):
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self.WIN = pygame.display.set_mode(resolution, vsync=1) #creating window
        pygame.display.set_caption(caption)
        pygame.display.set_icon(self.i_h.get(icon_filename))
        self.bg = self.i_h.get("white.jpg")
        
    def render(self, surface, coords):
        return self.WIN.blit(surface, coords)
    
    def background(self):
        self.WIN.fill("white")
        self.render(self.bg, (0,0))
    
    def graphics(self, state: GameState):
        self.background()
        # match state:
        #     case _:
        #         self.WIN.fill("white")
        