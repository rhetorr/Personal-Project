import pygame
from GameStates import GameStates
from util.RectHelpers import RectHelpers
from util.MouseUtil import Mouse, ClickType
from visuals.Button import Button
from player.Rocket import Rocket
from util.mathextra.Location import Angle, Point
from util.TextHelpers import TextHelpers
from .Sprite import Sprite
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers
import Settings
from screeninfo import get_monitors

class VisualsManager:
    def __init__(self, resolution, caption: str, icon_filename: str, mouse: Mouse):
        self.config_settings = Settings.get_config_dict()
        
        self.full_res = (get_monitors()[self.config_settings["main_monitor"]].width,get_monitors()[self.config_settings["main_monitor"]].height)
        self.def_res = resolution
        self.used_res = self.full_res if self.config_settings["fullscreen"] else resolution
        
        self.res_scalar = Point(self.used_res[0]/self.def_res[0], self.used_res[1]/self.def_res[1])
        
        self.mouse = mouse
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self._window_ = pygame.display.set_mode(self.used_res, vsync=1) #creating window
        pygame.display.set_caption(caption)
        self.icon = Sprite(self._window_, self.res_scalar.times(Point.fill(100))).with_image(icon_filename)
        pygame.display.set_icon(self.icon.sprite)
        
        self.space_bg = Sprite(self._window_, Point(self._window_.get_width(), self._window_.get_height())).with_image("stars.jpg", rotation=Angle.in_degrees(90))
        
        self.font = TextHelpers(self._window_, "arial", round(20*self.res_scalar.x))
        self.settings_font = TextHelpers(self._window_, "times new roman", round(40*self.res_scalar.x))
        
        self.back_button = Button(self._window_, Point.fill(0), self.res_scalar.times(Point.fill(75)), "<", round(30*self.res_scalar.x), bg_hover="red")
        
        self.icon_menu = Sprite(self._window_, self.res_scalar.times(Point.fill(225))).with_image(icon_filename)
        self.play_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Play", round(30*self.res_scalar.x), "sky blue", "blue")
        self.settings_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Settings", round(30*self.res_scalar.x))
        self.quit_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Quit", round(30*self.res_scalar.x), bg_hover="red")
        
        self.settings_panel = RectHelpers(Point(100, 0).times(self.res_scalar), Point(self._window_.get_width(), self._window_.get_height()).minus(Point(200, 0).times(self.res_scalar)))
        self.txt_fullscreen = self.settings_font.make_text("Fullscreen", "black")
        self.fullscreen_button = Button(self._window_, Point.fill(0), Point.fill(75).times(self.res_scalar), "", round(30*self.res_scalar.x), bg_hover="gray")
        
    def render(self, surface, coords):
        return self._window_.blit(surface, coords)
    
    def draw_testlines(self):
        pygame.draw.line(self._window_, "black", (self._window_.get_width()/2, 0), (self._window_.get_width()/2, self._window_.get_height()))
        pygame.draw.line(self._window_, "black", (0, self._window_.get_height()/2), (self._window_.get_width(), self._window_.get_height()/2))
    
    def graphics(self, state: GameStates, player: Rocket, timer):
        self._window_.fill("white")
        
        self.icon_menu.hide()
        self.play_button.hide()
        self.settings_button.hide()
        self.quit_button.hide()
        
        self.back_button.hide()
        self.fullscreen_button.hide()
        
        self.space_bg.hide()
        
        match state:
            case GameStates.LAUNCHING:
                self.font.full_render("LOADING...", "black", Point._key())
            case GameStates.MENU:
                self.icon_menu.at(Point(self._window_.get_width()/2-self.icon_menu.size.x/2, 0)).show().render()
                self.play_button.at(Point(self._window_.get_width()/2-self.play_button.size.x/2, self._window_.get_height()/2-self.play_button.size.y/2).minus(Point(0, 100).times(self.res_scalar))).show().render(self.mouse)
                self.settings_button.at(Point(self._window_.get_width()/2-self.settings_button.size.x/2, self._window_.get_height()/2)).show().render(self.mouse)
                self.quit_button.at(Point(self._window_.get_width()/2-self.quit_button.size.x/2, self._window_.get_height()/2-self.quit_button.size.y/2).plus(Point(0,200).times(self.res_scalar))).show().render(self.mouse)
            case GameStates.SETTINGS:
                self.settings_panel.render(self._window_, "gray")
                self.back_button.at(Point(15,15).times(self.res_scalar)).show().render(self.mouse)
                
                self.settings_font.render(self.txt_fullscreen, Point(125, 25).times(self.res_scalar))
                if self.config_settings["fullscreen"]:
                    self.fullscreen_button.with_image("checkmark.png")
                else:
                    self.fullscreen_button.with_text("")
                self.fullscreen_button.at(Point(self.txt_fullscreen.get_width()/2-self.fullscreen_button.size.x/2,self.txt_fullscreen.get_height()).plus(Point(125,25).times(self.res_scalar))).show().render(self.mouse)
                
            case GameStates.STARTING | GameStates.PLAYING | GameStates.LOST:
                self.space_bg.show().at(Point.fill(0)).render()
                player.render()
                t = self.font.make_text(str(timer), "black")
                self.font.render(t, Point(0, self._window_.get_height()-t.get_height()))
            case GameStates.QUITTING:
                self.font.full_render("QUITTING...", "black", Point._key())
        pygame.display.update()
        