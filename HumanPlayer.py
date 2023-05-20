from Player import Player
import pygame

class HumanPlayer(Player):
    def __init__(self, attack_keybinds=None):
        super().__init__()
        self.attack_keybinds = attack_keybinds
    
    def chooseAttack(self, key_down_events):
        if self._chosenAttack is not None:
            return None

        for event in key_down_events:
            if event.type == pygame.KEYDOWN:
                self._chosenAttack = self.attack_keybinds.get(event.key)
                
                if self._chosenAttack is not None:
                    break

        return self._chosenAttack