#create a starter project using pygame
from Countdown import Countdown
from Game import Game
from Player import Player
from Enums import AttackChoice, Mode
from Menu import Menu
from SingleplayerMenu import SingleplayerMenu
from SingleplayerGame import SingleplayerGame
import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
#
pygame.display.set_caption('Test')

player1_keybinds = {pygame.K_w: AttackChoice.PAPER, pygame.K_d: AttackChoice.SCISSORS, pygame.K_a: AttackChoice.ROCK} 
player2_keybinds = {pygame.K_UP: AttackChoice.PAPER, pygame.K_RIGHT: AttackChoice.SCISSORS, pygame.K_LEFT: AttackChoice.ROCK}

menu = Menu(game_display)
while menu.isRunning():
    menu.update()

if (menu.getMode() == Mode.QUIT):
    pygame.quit()
    quit()

if (menu.getMode() == Mode.SINGLEPLAYER):
    singleplayerMenu = SingleplayerMenu(game_display)
    while singleplayerMenu.isRunning():
        singleplayerMenu.update()
    
    game = SingleplayerGame(game_display, pygame.time.Clock(), [player1_keybinds], singleplayerMenu.getEnemy())
    while game.isRunning():
        game.update()
    
    pygame.quit()
    quit()

game = Game(game_display, pygame.time.Clock(), [player1_keybinds, player2_keybinds])
game.countdown.start()

while game.game_running:
    game.update()

pygame.quit()
