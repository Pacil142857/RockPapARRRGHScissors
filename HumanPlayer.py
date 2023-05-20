from Player import Player
import pygame

class HumanPlayer(Player):
    def __init__(self, attack_keybinds):
        super().__init__()
        self.attack_keybinds = attack_keybinds
    
    def chooseAttack(self):
        # Ask the human player to input their attack choice using Pygame
        choice = None

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                choice = self.attack_keybinds[event.key]

        return choice