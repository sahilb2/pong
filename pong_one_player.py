from pong_one_agent_env import *
from human_agent import HumanAgent
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

pygame.display.set_caption('One Player Pong Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_ON_LEFT = 0
PADDLE_ON_RIGHT = 1

PADDLE_WIDTH_SCALE = 10
WIDTH_SCALE = 500 + PADDLE_WIDTH_SCALE
HEIGHT_SCALE = 500
PADDLE_HEIGHT_SCALE = HEIGHT_SCALE * 0.2
BALL_RADIUS = 10

# Canvas Declaration
window = pygame.display.set_mode((WIDTH_SCALE, HEIGHT_SCALE), 0, 32)
pygame.display.set_caption('One Player Pong Game')

def draw(canvas, state, score):
    canvas.fill(WHITE)
    # Draw Borders
    pygame.draw.line(canvas, BLACK, [(WIDTH_SCALE * (1-state.paddle_x)), 0], [(WIDTH_SCALE * (1-state.paddle_x)), HEIGHT_SCALE], 5)
    pygame.draw.line(canvas, BLACK, [0, 0], [WIDTH_SCALE, 0], 5)
    pygame.draw.line(canvas, BLACK, [0, HEIGHT_SCALE], [WIDTH_SCALE, HEIGHT_SCALE], 5)
    # Draw Ball and Paddle
    pygame.draw.circle(canvas, BLACK, [int(state.ball_x * WIDTH_SCALE), int(state.ball_y * HEIGHT_SCALE)], BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, BLACK, [[int(WIDTH_SCALE * state.paddle_x), int(state.paddle_y * HEIGHT_SCALE)], [int((WIDTH_SCALE * state.paddle_x) + PADDLE_WIDTH_SCALE - (state.paddle_x * 2 * PADDLE_WIDTH_SCALE)), int(state.paddle_y * HEIGHT_SCALE)], [int((WIDTH_SCALE * state.paddle_x) + PADDLE_WIDTH_SCALE - (state.paddle_x * 2 * PADDLE_WIDTH_SCALE)), int((state.paddle_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)], [int(WIDTH_SCALE * state.paddle_x), int((state.paddle_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)]], 0)
    # Update Scores
    myfont = pygame.font.SysFont("Comic Sans MS", 25)
    label = myfont.render("Score " + str(score), 1, BLACK)
    canvas.blit(label, ((WIDTH_SCALE//2)-50, 20))

"""""""""""""""""""""
SIMULATION CODE BELOW
"""""""""""""""""""""

agent = HumanAgent()
agent.set_paddle_x(PADDLE_ON_RIGHT)
curr_state = get_initial_state(PADDLE_ON_RIGHT)
score = 0

while True:
    draw(window, curr_state, score)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                agent.up_pressed()
            if event.key == K_DOWN:
                agent.down_pressed()
        else:
            agent.nothing_pressed()
    if curr_state.game_over:
        print('GG')
        print('You Scored: ' + str(score))
        pygame.quit()
        sys.exit()
    if curr_state.hit:
        score += 1
    curr_state = get_next_state(curr_state, agent)
    pygame.display.update()
    fps.tick(50)
