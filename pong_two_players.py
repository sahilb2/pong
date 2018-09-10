from pong_two_agents_env import *
from human_agent import HumanAgent
import pygame, sys, time
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH_SCALE = 10
WIDTH_SCALE = 500 + (2 * PADDLE_WIDTH_SCALE)
HEIGHT_SCALE = 500
PADDLE_HEIGHT_SCALE = HEIGHT_SCALE * 0.2
BALL_RADIUS = 10

# Canvas Declaration
pygame.display.set_caption('Two Player Pong Game')
window = pygame.display.set_mode((WIDTH_SCALE, HEIGHT_SCALE), 0, 32)

def draw(canvas, state, total_hits):
    canvas.fill(WHITE)
    # Draw Borders
    pygame.draw.line(canvas, BLACK, [0, 0], [WIDTH_SCALE, 0], 5)
    pygame.draw.line(canvas, BLACK, [0, HEIGHT_SCALE], [WIDTH_SCALE, HEIGHT_SCALE], 5)
    # Draw Ball and Paddle
    pygame.draw.circle(canvas, BLACK, [int(state.ball_x * WIDTH_SCALE), int(state.ball_y * HEIGHT_SCALE)], BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, BLACK, [[0, int(state.paddle0_y * HEIGHT_SCALE)], [int(PADDLE_WIDTH_SCALE), int(state.paddle0_y * HEIGHT_SCALE)], [int(PADDLE_WIDTH_SCALE), int((state.paddle0_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)], [0, int((state.paddle0_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)]], 0)
    pygame.draw.polygon(canvas, BLACK, [[int(WIDTH_SCALE), int(state.paddle1_y * HEIGHT_SCALE)], [int(WIDTH_SCALE - PADDLE_WIDTH_SCALE), int(state.paddle1_y * HEIGHT_SCALE)], [int(WIDTH_SCALE - PADDLE_WIDTH_SCALE), int((state.paddle1_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)], [int(WIDTH_SCALE), int((state.paddle1_y * HEIGHT_SCALE) + PADDLE_HEIGHT_SCALE)]], 0)
    # Update Scores
    myfont = pygame.font.SysFont("Comic Sans MS", 25)
    label = myfont.render("Total Hits " + str(total_hits), 1, BLACK)
    canvas.blit(label, ((WIDTH_SCALE//2)-75, 20))

"""""""""""""""""""""
SIMULATION CODE BELOW
"""""""""""""""""""""

left_agent = HumanAgent()
right_agent = HumanAgent()
curr_state = get_initial_state()
total_hits = 0

while True:
    draw(window, curr_state, total_hits)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_w:
                left_agent.up_pressed()
            if event.key == K_s:
                left_agent.down_pressed()
            if event.key == K_UP:
                right_agent.up_pressed()
            if event.key == K_DOWN:
                right_agent.down_pressed()
        else:
            left_agent.nothing_pressed()
            right_agent.nothing_pressed()
    if curr_state.game_over0 or curr_state.game_over1:
        if curr_state.game_over0:
            print('Right Player Wins!')
        else:
            print('Left Player Wins!')
        print('Rally Score: ' + str(total_hits))
        pygame.quit()
        sys.exit()
    if curr_state.hit0 or curr_state.hit1:
        total_hits += 1
    curr_state = get_next_state(curr_state, left_agent, right_agent)
    pygame.display.update()
    fps.tick(50)
