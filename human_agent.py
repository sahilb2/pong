from pong_one_agent_env import *
import pygame, sys
from pygame.locals import *

class HumanAgent(Agent):
    def __init__(self):
        self.action = 0
        super().__init__()
    def get_action(self, state):
        return self.action
    def up_pressed(self):
        self.action = -1
    def down_pressed(self):
        self.action = 1
    def nothing_pressed(self):
        self.action = 0
