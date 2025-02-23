import pygame

from util.mathextra.Location import Point
from visuals.Sprite import Sprite
from GameStates import GameStates

class Rocket(Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__(window, Point.fill(75))
        self.with_image("rocket.png")
        self.appear_states = (GameStates.PLAYING, GameStates.LOST, GameStates.STARTING)
    def update(self, state: GameStates):
        for i in self.appear_states:
            if i == state:
                self.show()
            else:
                self.hide()
        self.render()