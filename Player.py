from Enums import GameOutcome
from Attack import Attack
from Hand import Hand

BASE_DAMAGE = 10

class Player:
    _hp = 100
    _attacks = None
    _hand = None
    
    # Create a player with 100 HP and basic attacks
    def __init__(self):
        self._hp = 100
        self._hand = Hand()
    
    # Choose an attack to use
    def chooseAttack(self, choice):
        _chosenAttack = self._hand.getAttack(choice)
    
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
    
    # Check if the player has already chosen a move
    def isReady(self):
        return self._choice != None

    # Check if the player is dead (HP <= 0)
    def isDead(self):
        return self._hp <= 0
    
    def getHP(self):
        return self._hp
    