################################################
# Run instructions: To start the game, press the green Start button (pygame, sys must be installed).
# To restart/replay the game, press Enter
##################################################

import pygame
import sys
from pygame.locals import *
import random
import numpy as np

pygame.init()

start_time_counting = pygame.time.get_ticks()
small_font = pygame.font.SysFont("Geneva", 25)  # for timer

# variables for counting wins
x_wins = 0
o_wins = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (200, 0, 0)
BLUE = (0, 0, 255)
BUTTONCOLOR = WHITE

# Screen
width, height = 450, 520
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")

images_list = ["Images/meme1.jpg", "Images/meme2.jpg", "Images/meme3.jpg", "Images/meme4.jpg"]
which_image = 0
link = images_list[0]


def set_background(link):  # function for applying background image
    background_img = pygame.image.load(link)
    background_img = pygame.transform.scale(background_img, (width, 450))
    return background_img


set_background(link)

board = np.zeros((3, 3))  # 3x3 board, basically a matrix
screen.blit(set_background(link), (0, 0))  # (0, 0) places the image starting from upper-left corner
pygame.draw.line(screen, WHITE, (0, 470), (450, 470), 35)


# Functions
def draw_lines():
    # 1 horizontal line, screen, color, start coordinate, end coordinate, width
    pygame.draw.line(screen, WHITE, (0, 150), (450, 150), 5)
    # 2 horizontal line
    pygame.draw.line(screen, WHITE, (0, 300), (450, 300), 5)
    # 1 vertical line
    pygame.draw.line(screen, WHITE, (150, 0), (150, 450), 5)
    # 2 vertical line
    pygame.draw.line(screen, WHITE, (300, 0), (300, 450), 5)


def draw_XO(row, col):
    if board[row][col] == 1:  # draw X
        pygame.draw.line(screen, WHITE, (col * 150 + 45, row * 150 + 150 - 45), (col * 150 + 150 - 45, row * 150 + 45),
                         23)
        pygame.draw.line(screen, WHITE, (col * 150 + 45, row * 150 + 45), (col * 150 + 150 - 45, row * 150 + 150 - 45),
                         23)
    elif board[row][col] == 2:  # draw O
        pygame.draw.circle(screen, WHITE, (int(col * 150 + 150 / 2), int(row * 150 + 150 / 2)), 40, 14)


def display_timer():
    elapsed_seconds = (pygame.time.get_ticks() - start_time_counting) // 1000
    pygame.draw.rect(screen, BLACK, (0, 500, width, 30))  # Clean previous timer area
    timer_text = small_font.render(f"Time: {elapsed_seconds}s", True, WHITE)
    timer_x = (width - timer_text.get_width()) // 2
    screen.blit(timer_text, (timer_x, 500))  # show timer text


def display_win_message(message):
    global x_wins, o_wins
    font = pygame.font.SysFont("Geneva", 50)  # large font for win/tie
    wins_font = pygame.font.SysFont("Geneva", 30)
    text = font.render(message, True, WHITE)
    text_x = (width - text.get_width()) // 2
    text_y = (450 - text.get_height()) // 2 - 25

    pygame.draw.rect(screen, RED, (text_x - 20, text_y - 20, text.get_width() + 40, text.get_height() + 90),
                     border_radius=20)

    screen.blit(text, (text_x, text_y))

    if "X won" in message:
        x_wins += 1
    elif "O won" in message:
        o_wins += 1

    score_text = small_font.render(f"X : {x_wins} | O : {o_wins}", True, WHITE)
    score_x = (width - score_text.get_width()) // 2
    score_y = text_y + 60
    screen.blit(score_text, (score_x, score_y))


def mark_square(row, col, player):  # marks matrix based on which player clicked
    board[row][col] = player


def check_square(row, col):  # check if cell is empty
    if board[row][col] == 0:
        return True
    else:
        return False


def board_full(row, col):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:  # found empty square
                return False
    return True  # no empty squares found


def who_won(player):
    # vertical win
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_line(col, player)
            return True

    # horizontal win
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_line(row, player)
            return True

    # diagonal check 1
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_first_diagonal(player)
        return True

    # diagonal check 2
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_second_diagonal(player)
        return True

    return False


def draw_vertical_line(col, player):
    X = col * 150 + 75
    pygame.draw.line(screen, WHITE, (X, 10), (X, 450 - 10), 10)


def draw_horizontal_line(row, player):
    Y = row * 150 + 75
    pygame.draw.line(screen, WHITE, (10, Y), (450 - 10, Y), 10)


def draw_first_diagonal(player):
    pygame.draw.line(screen, WHITE, (15, 450 - 15), (450 - 15, 15), 15)


def draw_second_diagonal(player):
    pygame.draw.line(screen, WHITE, (15, 15), (450 - 15, 450 - 15), 15)


def player_one_turn():
    pygame.draw.line(screen, RED, (0, 470), (225, 470), 45)
    pygame.draw.line(screen, WHITE, (225, 470), (450, 470), 45)

    pygame.draw.line(screen, BLACK, (330, 459), (345, 476), 5)
    pygame.draw.line(screen, BLACK, (345, 459), (330, 476), 5)

    pygame.draw.circle(screen, BLACK, (112, 465), 10, 3)


def player_two_turn():
    pygame.draw.line(screen, RED, (225, 470), (450, 470), 45)
    pygame.draw.line(screen, WHITE, (0, 470), (225, 470), 45)

    pygame.draw.line(screen, BLACK, (330, 459), (345, 476), 5)
    pygame.draw.line(screen, BLACK, (345, 459), (330, 476), 5)

    pygame.draw.circle(screen, BLACK, (112, 465), 10, 3)


def timer_box():
    pygame.draw.line(screen, BLACK, (0, 515), (450, 515), 45)


def restart():
    global which_image, link, background_img, player, start_time_counting
    start_time_counting = pygame.time.get_ticks()  # reset timer
    which_image += 1
    if which_image == len(images_list):
        which_image = 0
    link = images_list[which_image]
    screen.blit(set_background(link), (0, 0))
    player_two_turn()
    draw_lines()
    for row in range(3):
        for col in range(3):
            board[row][col] = 0
    player = 1

    for row in range(3):
        for col in range(3):
            board[row][col] = 0

    player = 1


draw_lines()
player = 1
game_end = False

player_two_turn()
timer_box()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_end:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // 150)
            clicked_col = int(mouseX // 150)

            if player == 1:
                player_one_turn()
            else:
                player_two_turn()

            if check_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    if who_won(player):
                        display_win_message("X won!")
                        game_end = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    if who_won(player):
                        display_win_message("O won!")
                        game_end = True
                    player = 1
                if board_full(0, 0) and not game_end:
                    display_win_message("Tie!")
                    game_end = True

                draw_XO(clicked_row, clicked_col)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                restart()
                game_end = False

    display_timer()
    pygame.display.update()
    print(board)
