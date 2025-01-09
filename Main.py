import pygame
import enum
import Util
import Constants as Css
import FileWriter


pygame.init()
pygame.font.init()
    
@enum.unique
class GameState(enum.Enum):
    launching = 0
    menu = 1
    menu_select = 2
    playing = 3
    ended = 4
    quitting = 5
    
@enum.unique
class PlayState(enum.Enum):
    travelling = 0
    aiming = 1
    fishing = 2
    success = 3
    fail = 4

def load_asset(filename, scalar: tuple):
    return pygame.transform.scale(pygame.image.load("assets/"+filename), scalar) #load background, stretch image to specified size *does not retain aspect ratio

def percent(num, percent):
    return (num*percent)/100

def if_then(bool: bool, trueVal, falseVal):
    if bool:
        val=trueVal
    else:
        val=falseVal
    return val

@enum.unique
class Mice(enum.Enum):
    cursor = 0
    hand = 1
    typing = 2

def set_cursor(type: Mice):
    if type == Mice.cursor:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if type == Mice.typing:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    if type == Mice.hand:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

class Dims:
    def __init__(self):
        self.rect_dims = (Css._ASPECT_RATIO[0]*percent(80,17), (Css._ASPECT_RATIO[1]*percent(80,17))/1.21 )
        self.caption = Css._CAPTION
        
    def create_rect(self, window, coords, dims, color):
        newRect = pygame.rect.Rect(coords[0],coords[1], dims[0],dims[1])
        newRect = pygame.draw.rect(window, color, newRect)
        return newRect
    
    def create_rect(self, window, coords, dims, color):
        newRect = pygame.rect.Rect(coords[0],coords[1], dims[0],dims[1])
        newRect = pygame.draw.rect(window, color, newRect)
        return newRect

class Game:
    def __init__(self):
        self._dims = Dims()
        self.fps = 60.0
        self.res = Css._SMALL_RESOLUTION
        self.run = True
        self.WIN = pygame.display.set_mode(self.res, vsync=1) #the window itself
        self.state = GameState.launching
        pygame.display.set_caption(self._dims.caption)
        self.BG = load_asset("bg.jpg", self.res)
        self.clock = pygame.time.Clock() #game clock
        self.pause = False
        
        self.generating = False
        self.defFont = pygame.font.SysFont("arial", 20)
        self.fullscreen = False
        
    def generate(self):
        if self.generating:
            return
        self.generating = True
        
    def get_res(self):
        self.res = self.WIN.get_size()
        return self.res
        
    def atState(self, goalState):
        return self.state == goalState
        
    def eventsHappened(self) -> bool:
        for event in pygame.event.get(): #all events or interactions with the window
            if event.type == pygame.QUIT:
                self.run = False
                
    def center_dif(self, dim_1: float, dim_2: float):
        return (dim_1/2) - (dim_2/2)
    
    def win_center_x(self, dim_2):
        return self.center_dif(self.WIN.get_width(), dim_2)
    
    def win_center_y(self, dim_2):
        return self.center_dif(self.WIN.get_height(), dim_2)

    def render(self, surface, coords):
        return self.WIN.blit(surface, coords)
    
    def renderRect(self, coords, dims, color: pygame.Color):
        return self._dims.create_rect(self.WIN, coords, dims, color)
    
    def percent_x(self, num):
        return percent(self.WIN.get_width(), num)
    
    def percent_y(self, num):
        return percent(self.WIN.get_height(), num)
    
    def graphics(self, dims: Dims, game_info) -> pygame.Rect:
        self.WIN.fill("white")
        self.render(self.BG,(0,0))
        world_list_text = []
        
        icon_a = load_asset("icon.png", (3*self.get_res()[0]/Css._ASPECT_RATIO[0] , 3*self.get_res()[1]/Css._ASPECT_RATIO[1]))
        yellow_dot = load_asset("yellow_dot.png", (1,1))
        blue_dot = load_asset("blue_dot.png", (1,1))
        
        menu_button = dims.rect_dims
        small_menu_button = (menu_button[0]/1.75, menu_button[1]/1.75)
        
        quit = pygame.Rect(-10, 0, 1, 1)
        play = pygame.Rect(-10, 0, 1, 1)
        new = pygame.Rect(-10, 0, 1, 1)
        
        if self.atState(GameState.launching):
            text_loading = self.defFont.render("LOADING", 1, "black")
            text_loading = pygame.transform.scale_by(text_loading, percent(1.0, 200))
            self.render(text_loading, (self.win_center_x(text_loading.get_width()), self.win_center_y(text_loading.get_height()) ))
        
        if self.atState(GameState.menu):
            icon = self.render(icon_a, (self.win_center_x(icon_a.get_width()), percent(self.get_res()[1], 2)))
            quit = self.renderRect((self.win_center_x(menu_button[0]), percent(self.get_res()[1], 65)), menu_button, "black")
            play = self.renderRect((self.win_center_x(menu_button[0]), percent(self.get_res()[1], 40)), menu_button, "black")
            
            
            quit_1=self.renderRect((self.win_center_x(menu_button[0])+Css._BUTTON_GAP,percent(self.get_res()[1],65)+Css._BUTTON_GAP),(menu_button[0]-Css._BUTTON_GAP*2,menu_button[1]-Css._BUTTON_GAP*2),if_then(quit.collidepoint(pygame.mouse.get_pos()),'red','white'))
            
            play_1=self.renderRect((self.win_center_x(menu_button[0])+Css._BUTTON_GAP,percent(self.get_res()[1],40)+Css._BUTTON_GAP),(menu_button[0]-Css._BUTTON_GAP*2,menu_button[1]-Css._BUTTON_GAP*2),if_then(play.collidepoint(pygame.mouse.get_pos()),'green','white'))
            
            text_play = self.defFont.render("PLAY", 1, "black")
            text_quit = self.defFont.render("QUIT", 1, "black")
            self.render(text_play, (play_1.x + self.center_dif(play_1.size[0], text_play.get_width()), play_1.y + self.center_dif(play_1.size[1], text_play.get_height())))
            self.render(text_quit, (quit_1.x + self.center_dif(quit_1.size[0], text_quit.get_width()), quit_1.y + self.center_dif(quit_1.size[1], text_quit.get_height())))
            
        if self.atState(GameState.menu_select):
            panel = self.renderRect((self.percent_x(15), self.percent_y(5)), (self.percent_x(70), self.percent_y(90)), "gray")
            
            new = self.renderRect((self.percent_x(3), self.percent_y(5)), small_menu_button, "black")
            new_1 = self.renderRect((self.percent_x(3) + Css._BUTTON_GAP, self.percent_y(5)+Css._BUTTON_GAP), (small_menu_button[0] - Css._BUTTON_GAP*2, small_menu_button[1] - Css._BUTTON_GAP*2), if_then(new.collidepoint(pygame.mouse.get_pos()),'gray','white'))
            
            play = self.renderRect((self.percent_x(3), self.percent_y(5*3)), small_menu_button, "black")
            play_1=self.renderRect((self.percent_x(3) + Css._BUTTON_GAP, self.percent_y(5*3)+Css._BUTTON_GAP),(small_menu_button[0] - Css._BUTTON_GAP*2, small_menu_button[1] - Css._BUTTON_GAP*2),if_then(play.collidepoint(pygame.mouse.get_pos()),'green','white'))
            
            text_new = self.defFont.render("NEW", 1, 'black')
            text_play = self.defFont.render("PLAY", 1, "black")
            self.render(text_new, (new_1.x + self.center_dif(new_1.size[0], text_new.get_width()), new_1.y + self.center_dif(new_1.size[1], text_new.get_height())))
            self.render(text_play, (play_1.x + self.center_dif(play_1.size[0], text_play.get_width()), play_1.y + self.center_dif(play_1.size[1], text_play.get_height())))
            
            
            if len(Util.get_worlds()) > 0:
                for i in range(len(Util.get_worlds())):
                    txt = self.defFont.render(Util.get_worlds()[i], 1, 'black')
                    rendered_box = self.renderRect((self.percent_x(5-2)+panel.x, self.percent_y(5*1.4*(i+1)-2)), (100,txt.get_height()+self.percent_y(2)), "darkgray")
                    rendered = self.render(txt,(self.percent_x(5)+panel.x, self.percent_y(5*1.4*(i+1)-2)+panel.y))
                    world_list_text.append(rendered)
                    if self.touch_mouse(rendered):
                        self.render(yellow_dot, (self.percent_x(1)+panel.x, self.percent_y(5*1.4*(i+1))+panel.y))
        
            if self.generating:
                text_generating = self.defFont.render("Generating world...", 1, "black")
                self.render(text_generating, (self.win_center_x(text_generating.get_width()), self.win_center_y(text_generating.get_height())))
            
        if self.atState(GameState.playing):
            
            if self.pause:
                text_paused = self.defFont.render("Game Paused", 1, "black")
                text_continue = self.defFont.render("press ESC to continue", 1, "black")
                paused_rect = self.render(text_paused, (self.win_center_x(text_paused.get_width()) , text_paused.get_height()+Css._BUTTON_GAP))
                self.render(text_continue, (self.win_center_x(text_continue.get_width()) , paused_rect.y*2))
            
        if self.atState(GameState.quitting):
            text_quitting = self.defFont.render("QUITTING", 1, "black")
            self.render(text_quitting, (self.center_dif(self.get_res()[0], text_quitting.get_width()) , self.center_dif(self.get_res()[1], text_quitting.get_height())))
        
        triggers = {
            "quit": quit,
            "play": play,
            "new": new
        }
        return triggers
    
    def gameplay(self, keys, triggers, dt, last):
        player_x, player_y, player_vel_x, player_vel_y = last[-1]["player"]["x"], last[-1]["player"]["y"], last[-1]["player"]["x_vel"], last[-1]["player"]["y_vel"]
        
        currentInfo = {
            "player": {
                "x": player_x,
                "y": player_y,
                "x_vel": player_vel_x,
                "y_vel": player_vel_y
            }
        }
        packedInfo = [
            last[1],
            last[2],
            currentInfo
        ]
        return packedInfo 

    def touch_mouse(self, button: pygame.Rect):
        return button.collidepoint(pygame.mouse.get_pos())
    
    def click_l(self):
        return pygame.mouse.get_pressed()[0]
    
    def click_r(self):
        return pygame.mouse.get_pressed()[2]
    
    def main(self):
        self.state = GameState.launching
        self.run = True
        self.pause = False

        while self.run: #game loop
            set_cursor(Mice.cursor)
            #State actions
            if self.atState(GameState.launching):
                dt = 1 / self.fps
                keys = pygame.key.get_pressed() #keys being pressed
                empty_info = {
                    "player": {
                        "x": 0,
                        "y": 0,
                        "x_vel": 0,
                        "y_vel": 0
                    }
                }
                buttons = self.graphics(Dims(), [empty_info,empty_info,empty_info])
                info_pack = self.gameplay(keys, buttons, dt, [empty_info,empty_info,empty_info])
        
                pause_delay = Util.Stopwatch()
                fullscreen_delay = Util.Stopwatch()
                esc_delay = Util.Stopwatch()
                
                self.pause = False
                self.generating = False
                self.state = GameState.menu #Adding the transition from state to another at the end of all actions
            if self.atState(GameState.menu):
                if keys[pygame.K_ESCAPE] and esc_delay.elapsed(Css._TRANSITION_DELAY):
                    self.state = GameState.quitting
                    esc_delay.reset()

                if self.touch_mouse(buttons["play"]): #transition
                    set_cursor(Mice.hand)
                    if self.click_l():
                        self.state = GameState.menu_select
                        
                if self.touch_mouse(buttons["quit"]): #transition
                    set_cursor(Mice.hand)
                    if self.click_l():
                        self.state = GameState.quitting
            if self.atState(GameState.menu_select):
                selected_world = 0
                if self.touch_mouse(buttons['new']):
                    set_cursor(Mice.hand)
                    if self.click_l():
                        self.generate()
                    
                if self.touch_mouse(buttons['play']):
                    set_cursor(Mice.hand)
                    # if self.click_l():
                    #     if not selected_world == 0:
                    
                if keys[pygame.K_ESCAPE] and esc_delay.elapsed(Css._TRANSITION_DELAY):
                    self.state = GameState.menu
                    esc_delay.reset()
            if self.atState(GameState.playing):
                if keys[pygame.K_ESCAPE] and pause_delay.elapsed(Css._TRANSITION_DELAY):
                    self.pause = not self.pause
                    pause_delay.reset()
                    
                if not self.pause:
                    info_pack = self.gameplay(keys, buttons, dt, info_pack)
                    
            if keys[pygame.K_F11] and fullscreen_delay.elapsed(Css._TRANSITION_DELAY):
                self.fullscreen = not self.fullscreen
                fullscreen_delay.reset()
                
                pygame.display.toggle_fullscreen()
                    
            self.eventsHappened()
            keys = pygame.key.get_pressed()
            buttons = self.graphics(self._dims, info_pack)
            pygame.display.flip()
            dt = self.clock.tick(self.fps) / 1000 #setting the fps, seconds since last frame
            
            
            if (self.state == GameState.quitting):
                self.run = False

        self.run = False
        pygame.quit() #game quits once the loop ends
        
        return self
    

game = Game().main()