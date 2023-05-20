from Enums import GameOutcome
from Attack import Attack
from Hand import Hand
import pygame

BASE_DAMAGE = 10

class Player:
    _hp = 100
    _attacks = None
    _hand = None
    
    # Create a player with 100 HP and basic attacks
    def __init__(self, attack_keybinds=None):
        self._hp = 100
        self._hand = Hand()
        self.attack_keybinds = attack_keybinds
    
    #Choose an attack to use based on the keybinds and input from pygame
    def chooseAttackFromInput(self):
        if self.attack_keybinds == None:
            return

        for key, value in self.attack_keybinds.items():
            if pygame.key.get_pressed()[key]:
                self.chooseAttack(value)
    
    # Choose an attack to use
    def chooseAttack(self, choice):
        self._chosenAttack = self._hand.getAttack(choice)
    
    # Fight another player
    def fight(self, player):
        result = self._chosenAttack.against(player._chosenAttack)
        
        # You won, so deal damage, get health, and give the opponent an effect in their hand
        if result == GameOutcome.WIN:
            player.takeDamage(self._chosenAttack.getDamage(BASE_DAMAGE))
            self.heal(self._chosenAttack.getHeal(BASE_DAMAGE))
            self._hand = Hand()
            player._hand = Hand(None)
        # You lost, so you take damage, the opponent gets healed, and you get an effect in your hand 
        elif result == GameOutcome.LOSE:
            self.takeDamage(player._chosenAttack.getDamage(BASE_DAMAGE))
            player.heal(player._chosenAttack.getHeal(BASE_DAMAGE))
            self._hand = Hand(None)
            player._hand = Hand()

    # Take a certain amount of damage
    def takeDamage(self, damage):
        self._hp -= damage
        self._hp = 0 if self._hp < 0 else self._hps
    
    # Heal a certain amount
    def heal(self, amount):
        self.takeDamage(-1 * amount)
    