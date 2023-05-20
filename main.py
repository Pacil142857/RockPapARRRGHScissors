#create a starter project using pygame
from Countdown import Countdown
from Game import Game
from HumanPlayer import HumanPlayer
from Player import Player
from Enums import AttackChoice, Mode
from Menu import Menu
import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
#
pygame.display.set_caption('Test')

menu = Menu(game_display)
while menu.isRunning():
    menu.update()

if (menu.getMode() != Mode.MULTIPLAYER):
    pygame.quit()
    quit()

player1_keybinds = {pygame.K_w: AttackChoice.PAPER, pygame.K_d: AttackChoice.SCISSORS, pygame.K_a: AttackChoice.ROCK} 
player2_keybinds = {pygame.K_UP: AttackChoice.PAPER, pygame.K_RIGHT: AttackChoice.SCISSORS, pygame.K_LEFT: AttackChoice.ROCK}

player1 = HumanPlayer(player1_keybinds)
player2 = HumanPlayer(player2_keybinds)

game = Game(game_display, pygame.time.Clock(), player1, player2)
game.countdown.start()

while game.game_running:
    game.update()

pygame.quit()
