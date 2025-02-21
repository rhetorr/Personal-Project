import pygame
from GameStates import GameStates
from visuals.Button import Button
from player.Rocket import Rocket
from util.mathextra.Location import Point
from util.TextHelpers import TextHelpers
from .Sprite import Sprite
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class VisualsManager:
    def __init__(self, resolution: tuple, caption: str, icon_filename: str):
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self._window_ = pygame.display.set_mode((resolution[0], resolution[1]), vsync=1) #creating window
        pygame.display.set_caption(caption)
        self.icon = Sprite(self._window_, Point.fill(100), GameStates.MENU).from_image(icon_filename)
        pygame.display.set_icon(self.icon.sprite)
        self.font = TextHelpers(self._window_, "arial", 20)
        
        self.back_button = Button(self._window_, Point(0, 0), Point(250, 75), "Back", 30, bg_hover="red")
        
        self.icon_menu = Sprite(self._window_, Point.fill(225), GameStates.MENU).from_image(icon_filename)
        self.play_button = Button(self._window_, Point(0, 0), Point(250, 75), "Play", 30, "sky blue", "blue")
        self.settings_button = Button(self._window_, Point(0, 0), Point(250, 75), "Settings", 30)
        self.quit_button = Button(self._window_, Point(0, 0), Point(250, 75), "Quit", 30, bg_hover="red")
        
    def render(self, surface, coords):
        return self._window_.blit(surface, coords)
    
    def draw_testlines(self):
        pygame.draw.line(self._window_, "black", (self._window_.get_width()/2, 0), (self._window_.get_width()/2, self._window_.get_height()))
        pygame.draw.line(self._window_, "black", (0, self._window_.get_height()/2), (self._window_.get_width(), self._window_.get_height()/2))
    
    def graphics(self, state: GameStates, player: Rocket):
        self._window_.fill("white")
        player.hide()
        self.play_button.hide()
        match state:
            case GameStates.LAUNCHING:
                self.font.full_render("LOADING...", "black", Point._key())
            case GameStates.MENU:
                self.icon_menu.at(Point(self._window_.get_width()/2-self.icon_menu.size.x/2, 0)).show().render()
                self.play_button.at(Point(self._window_.get_width()/2-self.play_button.size.x/2, self._window_.get_height()/2-self.play_button.size.y/2 - 100)).show().render()
                self.settings_button.at(Point(self._window_.get_width()/2-self.settings_button.size.x/2, self._window_.get_height()/2)).show().render()
                self.quit_button.at(Point(self._window_.get_width()/2-self.quit_button.size.x/2, self._window_.get_height()/2-self.quit_button.size.y/2 + 200)).show().render()
            case GameStates.SETTINGS:
                self.back_button.at(Point(0,0)).show().render()
                self.font.full_render("Settings", "black", Point._key())
            case GameStates.STARTING | GameStates.PLAYING | GameStates.LOST:
                player.show().render()
                self.font.full_render("wip", "black", Point._key())
            case GameStates.QUITTING:
                self.font.full_render("QUITTING...", "black", Point._key())
        pygame.display.update()
        