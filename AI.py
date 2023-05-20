import Hand
import Player
from Enums import AttackChoice
import random

class TheBlunderer(Player):
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
        self._name = "The Blunderer"
    
    # The blunderer always uses the blunderbuss!
    def chooseAttack(self):
        self._chosenAttack = self._hand.getAttack(AttackChoice.SCISSORS)

class Randall(Player):
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
        self._name = "Boatswain Randall"
    
    # Boatswain Randall will always choose their attack randomly
    def chooseAttack(self):
        choice = random.choice((AttackChoice.ROCK, AttackChoice.PAPER, AttackChoice.SCISSORS))
        self._chosenAttack = self._hand.getAttack(choice)