import Attack
import random

class Hand:
    _rock = None
    _paper = None
    _scissors = None
    
    # Create a hand with 3 specific attacks
    def __init__(self, rock, paper, scissors):
        self._rock = rock
        self._paper = paper
        self._scissors = scissors
    
    # Create a hand with 3 basic attacks
    def __init__(self):
        self._rock = Attack(Attack.ROCK)
        self._paper = Attack(Attack.PAPER)
        self._scissors = Attack(Attack.SCISSORS)
        
    # Create a hand with 1 effect attack
    def __init__(self, effect):
        # Get an effect
        if effect == None:
            effect = random.choice((Attack.EXTRA_DAMAGE, Attack.HEAL_ON_HIT, Attack.WIN_TIES))
        
        # Set default attacks
        self._rock = Attack(Attack.ROCK)
        self._paper = Attack(Attack.PAPER)
        self._scissors = Attack(Attack.SCISSORS)
        
        # Overwrite the effect attack
        if effect == Attack.EXTRA_DAMAGE:
            self._rock = Attack(Attack.ROCK, effect)
        elif effect == Attack.HEAL_ON_HIT:
            self._paper = Attack(Attack.PAPER, effect)
        elif effect == Attack.WIN_TIES:
            self._scissors = Attack(Attack.SCISSORS, effect)
    
    # Get the attack used
    def getAttack(self, choice):
        if choice == Attack.ROCK:
            return self._rock
        if choice == Attack.PAPER:
            return self._paper
        return self._scissors
    
    def getRock(self):
        return self._rock

    def getPaper(self):
        return self._paper
    
    def getScissors(self):
        return self._scissors