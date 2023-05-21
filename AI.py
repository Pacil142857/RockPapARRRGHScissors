from Hand import Hand
from Player import Player
from Enums import AttackChoice
import random

CHOICES = (AttackChoice.ROCK, AttackChoice.PAPER, AttackChoice.SCISSORS)

class TheBlunderer(Player):
    def __init__(self):
        super().__init__("The Blunderer")
    
    # The blunderer always uses the blunderbuss!
    def chooseAttack(self):
        self._chosenAttack = self._hand.getAttack(AttackChoice.SCISSORS)

class Randall(Player):
    def __init__(self):
        super().__init__("Boatswain Randall")
    
    # Boatswain Randall will always choose their attack randomly
    def chooseAttack(self):
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Gunter(Player):
    def __init__(self):
        super().__init__("Gunner Gunter")
    
    # Gunner Gunter will always choose the strongest attack he has
    def chooseAttack(self):
        # Choose the attack that has an effect
        for choice in CHOICES:
            if self._hand.getAttack(choice).hasEffect():
                self._chosenAttack = self._hand.getAttack(choice)
                return
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Quartz(Player):
    def __init__(self):
        super().__init__("Quartermaster Quartz")
    
    # Quartermaster Quartz will always choose the option that loses to his effect attack
    def chooseAttack(self):
        # Choose the attack that loses to the effect attack
        for i, choice in enumerate(CHOICES):
            if self._hand.getAttack(choice).hasEffect():
                self._chosenAttack = self._hand.getAttack(CHOICES[(i - 1) % 3])
                return
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Finn(Player):
    def __init__(self):
        super().__init__("First Mate Finn")
    
    # First Mate Finn acts as Gunner Gunter 67% of the time and as Quartermaster Quartz 33% of the time
    def chooseAttack(self):
        # Choose the attack that loses to the effect attack
        for i, choice in enumerate(CHOICES):
            if self._hand.getAttack(choice).hasEffect():
                subtrahend = random.choice((0, 0, 1))
                self._chosenAttack = self._hand.getAttack(CHOICES[(i - subtrahend) % 3])
                return
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)

class Captain(Player):
    def __init__(self):
        super().__init__("The Captain")
    
    # The Captain acts as Gunner Gunter 66% of the time, Quartermaster Quartz 17% of the time, and as the
    # other person who would complement these three 17% of the time.
    def chooseAttack(self):
        # Choose the attack that loses to the effect attack
        for i, choice in enumerate(CHOICES):
            if self._hand.getAttack(choice).hasEffect():
                subtrahend = random.choice((0, 0, 0, 0, 1, 2))
                self._chosenAttack = self._hand.getAttack(CHOICES[(i - subtrahend) % 3])
                return
        
        # No effect exists, so choose randomly
        choice = random.choice(CHOICES)
        self._chosenAttack = self._hand.getAttack(choice)
