from Enums import AttackChoice, GameOutcome, AttackEffect

class Attack:
    _choice = None
    _effect = None

    def __init__(self, choice, effect=None):
        _choice = choice
        _effect = effect
    
    # Calculate whether this attack wins, ties, or loses against another attack
    def against(self, attack):
        # Losing matchups
        if self._choice == AttackChoice.ROCK and attack._choice == AttackChoice.PAPER or \
            self._choice == AttackChoice.PAPER and attack._choice == AttackChoice.SCISSORS or \
            self._choice == AttackChoice.SCISSORS and attack._choice == AttackChoice.ROCK:
            return GameOutcome.LOSE

        # Winning matchups
        if self._choice == AttackChoice.ROCK and attack._choice == AttackChoice.SCISSORS or \
            self._choice == AttackChoice.PAPER and attack._choice == AttackChoice.ROCK or \
            self._choice == AttackChoice.SCISSORS and attack._choice == AttackChoice.PAPER:
            return GameOutcome.WIN

        # Ties
        if self._choice == AttackChoice.ROCK and attack._choice == AttackChoice.ROCK or \
            self._choice == AttackChoice.PAPER and attack._choice == AttackChoice.PAPER or \
            self._choice == AttackChoice.SCISSORS and attack._choice == AttackChoice.SCISSORS:
            # The effect is "win ties," so it's actually a win
            if self._effect == AttackEffect.WIN_TIES and not attack._effect == AttackEffect.WIN_TIES:
                return GameOutcome.WIN
            # The opponent's effect is "win ties," so it's actually a loss
            if not self._effect == AttackEffect.WIN_TIES and attack._effect == AttackEffect.WIN_TIES:
                return GameOutcome.LOSE
        
            # It's a normal tie (or both players have "win ties")
            return GameOutcome.TIE

        # Something went horribly wrong, so just tie it
        return GameOutcome.TIE
    
    # Get the damage done by this attack (if successful)
    def getDamage(self, baseAtk):
        return baseAtk * (2 if self._effect == AttackEffect.EXTRA_DAMAGE else 1)

    # Get the amount healed by this attack
    def getHeal(self, baseAtk):
        return self.getDamage(baseAtk) if self._effect == AttackEffect.HEAL_ON_HIT else 0
    
    # Getters
    def getChoice(self):
        return self._choice
    
    def getEffect(self):
        return self._effect
    