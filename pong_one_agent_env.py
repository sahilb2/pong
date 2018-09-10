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
    def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle_x, paddle_y):
        # True if the ball passes the paddle
        self.game_over = False
        # True if the ball hits the paddle
        self.hit = False
        # Setting minimum for paddle_y
        if paddle_y < 0:
            paddle_y = 0
        # Setting maximum for paddle_y
        if paddle_y > 1 - PADDLE_HEIGHT:
            paddle_y = 1 - PADDLE_HEIGHT
        # Dealing with bounces
        side_wall_bounce = False
        if ball_y < 0:
            ball_y = -ball_y
            velocity_y = -velocity_y
        if ball_y > 1:
            ball_y = 2-ball_y
            velocity_y = -velocity_y
        if (ball_x < 0 and paddle_x == 1) or (ball_x > 1 and paddle_x == 0):
            ball_x = (2 * (1 - paddle_x)) - ball_x
            velocity_x = -velocity_x
            side_wall_bounce = True
        if ((ball_x > 1 and paddle_x == 1) or (ball_x < 0 and paddle_x == 0)) and not side_wall_bounce:
            # Check if ball hit the paddle or not
            if ball_y > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT:
                # Hit!
                self.hit = True
                ball_x = (2 * paddle_x) - ball_x
                U = random.uniform(-0.015, 0.015)
                V = random.uniform(-0.03, 0.03)
                velocity_x = -velocity_x + U
                velocity_y = -velocity_y + V
            else:
                # Miss :(
                self.game_over = True
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
        self.paddle_y = paddle_y
        self.paddle_x = paddle_x

class Agent(ABC):
    def __init__(self):
        self.paddle_x = -1
        super().__init__()
    def set_paddle_x(self, paddle_x):
        self.paddle_x = paddle_x
    def get_paddle_x(self):
        return self.paddle_x
    @abstractmethod
    def get_action(self, state):
        # Return 1 for up, -1 for down, or 0 to stay
        pass

def get_initial_state(paddle_x):
    return State(0.5, 0.5, 0.03, 0.01, paddle_x, 0.5-(PADDLE_HEIGHT/2))

def get_next_state(curr_state, agent):
    assert (agent.get_paddle_x() != -1)
    simple_curr_state = SimpleState(curr_state.ball_x, curr_state.ball_y, curr_state.velocity_x, curr_state.velocity_y, curr_state.paddle_y, curr_state.hit, curr_state.game_over)
    if agent.get_paddle_x() == 0:
        simple_curr_state.ball_x = 1 - simple_curr_state.ball_x
        simple_curr_state.velocity_x = -simple_curr_state.velocity_x
    new_paddle_y = curr_state.paddle_y + (agent.get_action(simple_curr_state) * 0.04)
    new_ball_x = curr_state.ball_x + curr_state.velocity_x
    new_ball_y = curr_state.ball_y + curr_state.velocity_y
    new_velocity_x = curr_state.velocity_x
    new_velocity_y = curr_state.velocity_y
    return State(new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, curr_state.paddle_x, new_paddle_y)
