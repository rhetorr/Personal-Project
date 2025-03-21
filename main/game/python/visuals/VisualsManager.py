import pygame
from GameStates import GameStates
from entities.FuelCell import FuelCell
from entities.Asteroid import Asteroid
from util.RectHelpers import RectHelpers
from util.MouseUtil import Mouse, ClickType
from visuals.Button import Button
from entities.Rocket import Rocket
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
        self.window_size = self._window_.get_size()
        self.window_width = self.window_size[0]
        self.window_height = self.window_size[1]
        pygame.display.set_caption(caption)
        self.icon = Sprite(self._window_, self.res_scalar.times(Point.fill(100))).with_image("rocket.png")
        pygame.display.set_icon(self.icon.sprite)
        
        
        self.font = TextHelpers(self._window_, "arial", round(20*self.res_scalar.x))
        self.settings_font = TextHelpers(self._window_, "times new roman", round(40*self.res_scalar.x))
        
        self.back_button = Button(self._window_, Point.fill(0), self.res_scalar.times(Point.fill(75)), "<", round(30*self.res_scalar.x), bg_hover="orange")
        
        self.icon_menu = Sprite(self._window_, self.res_scalar.times(Point(325, 400))).with_image(icon_filename)
        self.play_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Play", round(30*self.res_scalar.x))
        self.settings_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Settings", round(30*self.res_scalar.x), bg_hover="orange")
        self.quit_button = Button(self._window_, Point.fill(0), Point(250, 75).times(self.res_scalar), "Quit", round(30*self.res_scalar.x), bg_hover="red")
        
        self.settings_panel = RectHelpers(Point(100, 0).times(self.res_scalar), Point(self.window_width, self.window_height).minus(Point(200, 0).times(self.res_scalar)))
        self.txt_fullscreen = self.settings_font.make_text("Fullscreen", "white")
        self.fullscreen_button = Button(self._window_, Point.fill(0), Point.fill(75).times(self.res_scalar), "", round(30*self.res_scalar.x), bg_color= pygame.Color(0, 150, 0).grayscale(), bg_hover="gray")
        
        self.menu_button = Button(self._window_, Point.fill(0), Point(125, 75).times(self.res_scalar), "Menu", round(50*self.res_scalar.x), bg_hover="orange")
        
        self.bg_vel = round(300 * self.res_scalar.y) # px/s
        self.space_bg_1 = Sprite(self._window_, Point(self.window_width, self.window_height)).with_image("stars.jpg", rotation=Angle.in_degrees(90))
        self.space_bg_2 = Sprite(self._window_, Point(self.window_width, self.window_height)).with_image("stars.jpg", rotation=Angle.in_degrees(90))
        
    def render(self, surface, coords):
        return self._window_.blit(surface, coords)
    
    def draw_testlines(self):
        pygame.draw.line(self._window_, "black", (self.window_width/2, 0), (self.window_width/2, self.window_height))
        pygame.draw.line(self._window_, "black", (0, self.window_height/2), (self.window_width, self.window_height/2))
    
    def graphics(self, state: GameStates, player: Rocket, fuel: FuelCell, asteroid_1: Asteroid, asteroid_2: Asteroid, asteroid_3: Asteroid, asteroid_4: Asteroid, asteroid_5: Asteroid, timer, score):
        
        window_width_half = self.window_width/2
        window_height_half = self.window_height/2
        window_size_point: Point = Point.from_tuple(self.window_size)
        match state:
            case GameStates.LAUNCHING:
                self._window_.fill("black")
                self.font.full_render("LOADING...", "white", Point._key())
            case GameStates.MENU:
                self._window_.fill('black')
                self.icon_menu.at(Point(window_width_half-self.icon_menu.size.x/2, 0)).render()
                self.play_button.at(Point(window_width_half-self.play_button.size.x/2, window_height_half-self.play_button.size.y/2).minus(Point(0, 100).times(self.res_scalar))).render(self.mouse)
                self.settings_button.at(Point(window_width_half-self.settings_button.size.x/2, window_height_half)).render(self.mouse)
                self.quit_button.at(Point(window_width_half-self.quit_button.size.x/2, window_height_half-self.quit_button.size.y/2).plus(Point(0,200).times(self.res_scalar))).render(self.mouse)
            case GameStates.SETTINGS:
                self._window_.fill('black')
                self.settings_panel.render(self._window_, pygame.Color(0, 50, 0).grayscale())
                self.back_button.at(Point(15,15).times(self.res_scalar)).render(self.mouse)
                
                self.settings_font.render(self.txt_fullscreen, Point(125, 25).times(self.res_scalar))
                
                self.settings_font.full_render("Best time:", "white", Point(375, 25).times(self.res_scalar))
                self.settings_font.full_render(str(self.config_settings["best_time"]), 'white', Point(375, self.fullscreen_button.pos.y).times(self.res_scalar))
                self.settings_font.full_render("Best score:", "white", Point(625, 25).times(self.res_scalar))
                self.settings_font.full_render(str(self.config_settings["best_score"]), 'white', Point(625, self.fullscreen_button.pos.y).times(self.res_scalar))
                
                if self.config_settings["fullscreen"]:
                    self.fullscreen_button.with_image("checkmark.png")
                else:
                    self.fullscreen_button.with_text("")
                self.fullscreen_button.at(Point(self.txt_fullscreen.get_width()/2-self.fullscreen_button.size.x/2,self.txt_fullscreen.get_height()).plus(Point(125,25).times(self.res_scalar))).render(self.mouse)
                
            case GameStates.STARTING | GameStates.PLAYING | GameStates.LOST | GameStates.PAUSED:
                self._window_.fill("black")
                self.space_bg_1.render()
                self.space_bg_2.render()
                fuel.render()
                player.render()
                asteroid_1.render()
                asteroid_2.render()
                asteroid_3.render()
                asteroid_4.render()
                asteroid_5.render()
                t = self.font.make_text_highlighted("time: " + str(timer), "white", "black")
                self.font.full_render("fuel: " + str(round(player.fuel, ndigits=2)) + "%", "white", Point(0, self.window_height-(t.get_height()*1) ))
                self.font.full_render("best time: " + str(self.config_settings["best_time"]), "white", Point(0, self.window_height-(t.get_height()*2) ))
                self.font.render(t, Point(0, self.window_height-(t.get_height()*3) ))
                
                if state == GameStates.PAUSED:
                    self.menu_button.at(Point(15, 15)).render(self.mouse)
                    ttt = self.settings_font.make_text_highlighted(" PAUSED ", "white", "orange")
                    middlepos = window_size_point.div_by(2).minus(Point.from_tuple(ttt.get_size()).div_by(2))
                    self.settings_font.render(ttt, middlepos)
                    self.settings_font.full_render("score: " + str(score), "white", middlepos.plus(Point(0,ttt.get_height())), highlighted=True, highlight_color="orange")
                    self.settings_font.full_render("best: " + str(self.config_settings["best_score"]), "white", middlepos.plus(Point(0,ttt.get_height()*2)), highlighted=True, highlight_color="orange")
                elif state == GameStates.LOST:
                    self.menu_button.at(Point(15, 15)).render(self.mouse)
                    ttt = self.settings_font.make_text_highlighted(" LOST ", "red", "gray")
                    middlepos = window_size_point.div_by(2).minus(Point.from_tuple(ttt.get_size()).div_by(2))
                    self.settings_font.render(ttt, middlepos)
                    self.settings_font.full_render("score: " + str(score), "white", middlepos.plus(Point(0,ttt.get_height())), highlighted=True, highlight_color="gray")
                    self.settings_font.full_render("best: " + str(self.config_settings["best_score"]), "white", middlepos.plus(Point(0,ttt.get_height()*2)), highlighted=True, highlight_color="gray")
            case GameStates.QUITTING:
                self._window_.fill("black")
                self.font.full_render("QUITTING...", "white", Point._key())
        pygame.display.update()
        