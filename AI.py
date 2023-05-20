import Hand
import Player
from Enums import AttackChoice
import random

CHOICES = (AttackChoice.ROCK, AttackChoice.PAPER, AttackChoice.SCISSORS)

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
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Gunter(Player):
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
        self._name = "Gunner Gunter"
    
    # Gunner Gunter will always choose the strongest attack he has
    def chooseAttack(self):
        # Choose the attack that has an effect
        for choice in CHOICES:
            if self._hand.getAttack(choice).hasEffect():
                return self._hand.getAttack(choice)
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Quartz(Player):
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
        self._name = "Quartermaster Quartz"
    
    # Quartermaster Quartz will always choose the option that loses to his effect attack
    def chooseAttack(self):
        # Choose the attack that loses to the effect attack
        for i, choice in enumerate(CHOICES):
            if self._hand.getAttack(choice).hasEffect():
                return self._hand.getAttack(CHOICES[(i - 1) % 3])
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Finn(Player):
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
        self._name = "First Mate Finn"
    
    # First Mate Finn acts as Gunner Gunter 67% of the time and as Quartermaster Quartz 33% of the time
    def chooseAttack(self):
        # Choose the attack that loses to the effect attack
        for i, choice in enumerate(CHOICES):
            if self._hand.getAttack(choice).hasEffect():
                subtrahend = random.choice((0, 0, 1))
                return self._hand.getAttack(CHOICES[(i - subtrahend) % 3])
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)
