import os
os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['DISPLAY'] = ':1'
import pygame, sys
from pygame.locals import QUIT
import random
import time

clock = pygame.time.Clock()

pygame.init()

screen_width, screen_height = 800, 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

BACKGROUND_COLOR = (50, 168, 82)
SNAKE_COLOR = (0, 102, 0)
APPLE_COLOR = (200, 0, 0)
SCORE_COLOR = (255, 255, 255)

snake_block = 20
clock = pygame.time.Clock()

font_style = pygame.font.SysFont('comicsansms', 30)
score_font = pygame.font.SysFont('comicsansms', 20)

def display_score(score):
    value = score_font.render("Score: " + str(score), True, SCORE_COLOR)
    text_width, text_height = value.get_size()
    screen.blit(value, [(screen_width - text_width) / 2, 10])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, SNAKE_COLOR, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_width, text_height = mesg.get_size()
    screen.blit(mesg, [(screen_width - text_width) / 2, (screen_height - text_height) / 3])

def generate_apple(snake_body):
    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

    while (foodx, foody) in snake_body:
        foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

    return foodx, foody

def select_difficulty():
    screen.fill(BACKGROUND_COLOR)
    message("Select Difficulty: E=Easy M=Medium H=Hard N=Nightmare", SCORE_COLOR)
    pygame.display.update()

    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = "Easy"
                elif event.key == pygame.K_m:
                    difficulty = "Medium"
                elif event.key == pygame.K_h:
                    difficulty = "Hard"
                elif event.key == pygame.K_n:
                    difficulty = "Nightmare"

    if difficulty == "Easy":
        return 5
    elif difficulty == "Medium":
        return 8
    elif difficulty == "Hard":
        return 12
    elif difficulty == "Nightmare":
        return 20

def game_loop():
    snake_speed = select_difficulty()

    game_over = False
    game_close = False

    x1, y1 = screen_width // 2, screen_height // 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    direction = None
    last_direction = None

    foodx, foody = generate_apple(snake_list)

    while not game_over:

        while game_close:
            screen.fill(BACKGROUND_COLOR)
            message("You Lost! Press Q-Quit or C-Play Again", SCORE_COLOR)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

        if direction == "LEFT" and last_direction != "RIGHT":
            x1_change = -snake_block
            y1_change = 0
            last_direction = "LEFT"
        elif direction == "RIGHT" and last_direction != "LEFT":
            x1_change = snake_block
            y1_change = 0
            last_direction = "RIGHT"
        elif direction == "UP" and last_direction != "DOWN":
            y1_change = -snake_block
            x1_change = 0
            last_direction = "UP"
        elif direction == "DOWN" and last_direction != "UP":
            y1_change = snake_block
            x1_change = 0
            last_direction = "DOWN"

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BACKGROUND_COLOR)

        pygame.draw.ellipse(screen, APPLE_COLOR, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        if x1 < foodx + snake_block - 5 and x1 + snake_block > foodx + 5 and y1 < foody + snake_block - 5 and y1 + snake_block > foody + 5:
            foodx, foody = generate_apple(snake_list)
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
