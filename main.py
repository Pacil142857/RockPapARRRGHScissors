#create a starter project using pygame
from Countdown import Countdown
from Game import Game
from Player import Player
import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Test')

game = Game(game_display, pygame.time.Clock())

while game.game_running:
    game.update()

pygame.quit()
