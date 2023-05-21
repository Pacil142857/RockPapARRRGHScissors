#create a starter project using pygame
from Countdown import Countdown
from Game import Game
from HumanPlayer import HumanPlayer
from Player import Player
from Enums import AttackChoice, Mode
from Menu import Menu
from SingleplayerMenu import SingleplayerMenu
import pygame

pygame.init()

info = pygame.display.Info()

game_display = pygame.display.set_mode((info.current_w - 40, info.current_h - 90))

#this line is temporary and will be removed later. its just to make the game be less annyoing to use while testing
game_display = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Rock, Paper, ARRGH!')

player1_keybinds = {pygame.K_w: AttackChoice.PAPER, pygame.K_d: AttackChoice.ROCK, pygame.K_a: AttackChoice.SCISSORS} 
player2_keybinds = {pygame.K_UP: AttackChoice.PAPER, pygame.K_RIGHT: AttackChoice.ROCK, pygame.K_LEFT: AttackChoice.SCISSORS}

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
        
        player1 = HumanPlayer("Player 1", player1_keybinds)
        game = Game(game_display, pygame.time.Clock(), player1, singleplayerMenu.getEnemy())
        while game.isRunning():
            game.update()
    
    if (menu.getMode() == Mode.MULTIPLAYER):
        player1 = HumanPlayer(name="Player 1", attack_keybinds=player1_keybinds)
        player2 = HumanPlayer(name="Player 2", attack_keybinds=player2_keybinds)

        game = Game(game_display, pygame.time.Clock(), player1, player2)
        game.countdown.start()

        while game.game_running:
            game.update()
        
        menu.reset()
