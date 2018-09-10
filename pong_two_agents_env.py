from abc import ABC, abstractmethod
import numpy as np
from numpy.random import randint
import random

PADDLE_HEIGHT = 0.2

class SimpleState:
    def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle_y, hit, game_over):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y
        self.hit = hit
        self.game_over = game_over

class State:
    def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle0_y, paddle1_y):
        # True if the ball passes the paddle
        self.game_over0 = False
        self.game_over1 = False
        # True if the ball hits the paddle
        self.hit0 = False
        self.hit1 = False
        # Setting minimum for paddle_y
        if paddle0_y < 0:
            paddle0_y = 0
        if paddle1_y < 0:
            paddle1_y = 0
        # Setting maximum for paddle_y
        if paddle0_y > 1 - PADDLE_HEIGHT:
            paddle0_y = 1 - PADDLE_HEIGHT
        if paddle1_y > 1 - PADDLE_HEIGHT:
            paddle1_y = 1 - PADDLE_HEIGHT
        # Dealing with bounces
        side_wall_bounce0 = False
        side_wall_bounce1 = False
        if ball_y < 0:
            ball_y = -ball_y
            velocity_y = -velocity_y
        if ball_y > 1:
            ball_y = 2-ball_y
            velocity_y = -velocity_y
        if ball_x < 0:
            if ball_y > paddle0_y and ball_y < paddle0_y + PADDLE_HEIGHT:
                # Hit!
                self.hit0 = True
                ball_x = -ball_x
                U = random.uniform(-0.015, 0.015)
                V = random.uniform(-0.03, 0.03)
                velocity_x = -velocity_x + U
                velocity_y = -velocity_y + V
            else:
                # Miss :(
                self.game_over0 = True
        if ball_x > 1:
            if ball_y > paddle1_y and ball_y < paddle1_y + PADDLE_HEIGHT:
                # Hit!
                self.hit1 = True
                ball_x = 2-ball_x
                U = random.uniform(-0.015, 0.015)
                V = random.uniform(-0.03, 0.03)
                velocity_x = -velocity_x + U
                velocity_y = -velocity_y + V
            else:
                # Miss :(
                self.game_over1 = True
        # Setting minimum for velocity_x
        if abs(velocity_x) < 0.03:
            if velocity_x < 0:
                velocity_x = -0.03
            else:
                velocity_x = 0.03
        # Setting maximum for velocity_x
        if abs(velocity_x) > 1:
            if velocity_x < 0:
                velocity_x = -1
            else:
                velocity_x = 1
        # Setting maximum for velocity_y
        if abs(velocity_y) > 1:
            if velocity_y < 0:
                velocity_y = -1
            else:
                velocity_y = 1
        # Set necessary variables
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle0_y = paddle0_y
        self.paddle1_y = paddle1_y

class Agent(ABC):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def get_action(self, state):
        # Return 1 for up, -1 for down, or 0 to stay
        pass

def get_initial_state():
    return State(0.5, 0.5, 0.03, 0.01, 0.5-(PADDLE_HEIGHT/2), 0.5-(PADDLE_HEIGHT/2))

def get_next_state(curr_state, left_agent, right_agent):
    left_simple_state = SimpleState(1 - curr_state.ball_x, curr_state.ball_y, -curr_state.velocity_x, curr_state.velocity_y, curr_state.paddle0_y, curr_state.hit0, curr_state.game_over0)
    right_simple_state = SimpleState(curr_state.ball_x, curr_state.ball_y, curr_state.velocity_x, curr_state.velocity_y, curr_state.paddle1_y, curr_state.hit1, curr_state.game_over1)
    new_paddle0_y = curr_state.paddle0_y + (left_agent.get_action(left_simple_state) * 0.04)
    new_paddle1_y = curr_state.paddle1_y + (right_agent.get_action(right_simple_state) * 0.04)
    new_ball_x = curr_state.ball_x + curr_state.velocity_x
    new_ball_y = curr_state.ball_y + curr_state.velocity_y
    new_velocity_x = curr_state.velocity_x
    new_velocity_y = curr_state.velocity_y
    return State(new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, new_paddle0_y, new_paddle1_y)
