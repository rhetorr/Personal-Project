import pygame
from GameStates import GameStates
from util.RectHelpers import RectHelpers
from util.MouseUtil import Mouse, ClickType
from visuals.Button import Button
from player.Rocket import Rocket
from util.mathextra.Location import Point
from util.TextHelpers import TextHelpers
from .Sprite import Sprite
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class VisualsManager:
    def __init__(self, resolution: tuple, caption: str, icon_filename: str, mouse: Mouse):
        self.mouse = mouse
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self._window_ = pygame.display.set_mode((resolution[0], resolution[1]), vsync=1) #creating window
        pygame.display.set_caption(caption)
        self.icon = Sprite(self._window_, Point.fill(100)).with_image(icon_filename)
        pygame.display.set_icon(self.icon.sprite)
        
        self.config_settings = {
            "fullscreen": False
        }
        
        self.font = TextHelpers(self._window_, "arial", 20)
        self.settings_font = TextHelpers(self._window_, "times new roman", 40)
        
        self.back_button = Button(self._window_, Point.fill(0), Point.fill(75), "<", 30, bg_hover="red")
        
        self.icon_menu = Sprite(self._window_, Point.fill(225)).with_image(icon_filename)
        self.play_button = Button(self._window_, Point.fill(0), Point(250, 75), "Play", 30, "sky blue", "blue")
        self.settings_button = Button(self._window_, Point.fill(0), Point(250, 75), "Settings", 30)
        self.quit_button = Button(self._window_, Point.fill(0), Point(250, 75), "Quit", 30, bg_hover="red")
        
        self.settings_panel = RectHelpers(Point(100, 0), Point(self._window_.get_width()-200, self._window_.get_height()))
        self.txt_fullscreen = self.settings_font.make_text("Fullscreen", "black")
        self.fullscreen_button = Button(self._window_, Point.fill(0), Point.fill(75), "", 30, bg_hover="gray")
        
    def render(self, surface, coords):
        return self._window_.blit(surface, coords)
    
    def draw_testlines(self):
        pygame.draw.line(self._window_, "black", (self._window_.get_width()/2, 0), (self._window_.get_width()/2, self._window_.get_height()))
        pygame.draw.line(self._window_, "black", (0, self._window_.get_height()/2), (self._window_.get_width(), self._window_.get_height()/2))
    
    def graphics(self, state: GameStates, player: Rocket):
        self._window_.fill("white")
        
        self.icon_menu.hide()
        self.play_button.hide()
        self.settings_button.hide()
        self.quit_button.hide()
        
        self.back_button.hide()
        self.fullscreen_button.hide()
        
        player.hide()
        match state:
            case GameStates.LAUNCHING:
                self.font.full_render("LOADING...", "black", Point._key())
            case GameStates.MENU:
                self.icon_menu.at(Point(self._window_.get_width()/2-self.icon_menu.size.x/2, 0)).show().render()
                self.play_button.at(Point(self._window_.get_width()/2-self.play_button.size.x/2, self._window_.get_height()/2-self.play_button.size.y/2 - 100)).show().render(self.mouse)
                self.settings_button.at(Point(self._window_.get_width()/2-self.settings_button.size.x/2, self._window_.get_height()/2)).show().render(self.mouse)
                self.quit_button.at(Point(self._window_.get_width()/2-self.quit_button.size.x/2, self._window_.get_height()/2-self.quit_button.size.y/2 + 200)).show().render(self.mouse)
            case GameStates.SETTINGS:
                self.settings_panel.render(self._window_, "gray")
                self.back_button.at(Point(15,15)).show().render(self.mouse)
                
                self.settings_font.render(self.txt_fullscreen, Point(125, 25))
                if self.config_settings["fullscreen"]:
                    self.fullscreen_button.with_image("checkmark.png")
                else:
                    self.fullscreen_button.with_text("")
                self.fullscreen_button.at(Point(125+self.txt_fullscreen.get_width()/2-self.fullscreen_button.size.x/2, 25+self.txt_fullscreen.get_height())).show().render(self.mouse)
                
            case GameStates.STARTING | GameStates.PLAYING | GameStates.LOST:
                player.show().render()
                self.font.full_render("wip", "black", Point._key())
            case GameStates.QUITTING:
                self.font.full_render("QUITTING...", "black", Point._key())
        pygame.display.update()
        