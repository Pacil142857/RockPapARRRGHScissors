from Enums import AttackChoice, AttackEffect
from Attack import Attack
import random

class Hand:
    _rock = None
    _paper = None
    _scissors = None
        
    # Create a hand with 3 attacks
    def __init__(self, effect=None):
        # Get an effect
        if effect != None:
            effect = random.choice((AttackEffect.EXTRA_DAMAGE, AttackEffect.HEAL_ON_HIT, AttackEffect.WIN_TIES))
        
        # Set default attacks
        self._rock = Attack(AttackChoice.ROCK)
        self._paper = Attack(AttackChoice.PAPER)
        self._scissors = Attack(AttackChoice.SCISSORS)
        
        # Overwrite the effect attack
        if effect == AttackEffect.EXTRA_DAMAGE:
            self._rock = Attack(AttackChoice.ROCK, effect)
        elif effect == AttackEffect.HEAL_ON_HIT:
            self._paper = Attack(AttackChoice.PAPER, effect)
        elif effect == AttackEffect.WIN_TIES:
            self._scissors = Attack(AttackChoice.SCISSORS, effect)
    
    # Get the attack used
    def getAttack(self, choice):
        if choice == AttackChoice.ROCK:
            return self._rock
        if choice == AttackChoice.PAPER:
            return self._paper
        if choice == AttackChoice.SCISSORS:
            return self._scissors
        
        return None
    
    def getRock(self):
        return self._rock

    def getPaper(self):
        return self._paper
    
    def getScissors(self):
        return self._scissors