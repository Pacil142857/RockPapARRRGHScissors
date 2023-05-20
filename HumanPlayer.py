from Player import Player
import pygame

class HumanPlayer(Player):
    def __init__(self, attack_keybinds=None):
        super().__init__()
        self.attack_keybinds = attack_keybinds
    
    def chooseAttack(self, game_events):
        # Ask the human player to input their attack choice using Pygame
        choice = None

        for event in game_events:
            if event.type == pygame.KEYDOWN:
                choice = self.attack_keybinds[event.key]

        return choice