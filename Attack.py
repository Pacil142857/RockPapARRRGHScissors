class Attack:
    _choice = None
    _effect = None
    
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    WIN = 1
    TIE = 0
    LOSE = -1

    EXTRA_DAMAGE = 1
    HEAL_ON_HIT = 2
    WIN_TIES = 3
    
    def __init__(self, choice, effect):
        _choice = choice
        _effect = effect
    
    def __init__(self, choice):
        _choice = choice
        _effect = None
    
    # Calculate whether this attack wins, ties, or loses against another attack
    def against(self, attack):
        # Losing matchups
        if self._choice == Attack.ROCK and attack._choice == Attack.PAPER or \
            self._choice == Attack.PAPER and attack._choice == Attack.SCISSORS or \
            self._choice == Attack.SCISSORS and attack._choice == Attack.ROCK:
            return Attack.LOSE

        # Winning matchups
        if self._choice == Attack.ROCK and attack._choice == Attack.SCISSORS or \
            self._choice == Attack.PAPER and attack._choice == Attack.ROCK or \
            self._choice == Attack.SCISSORS and attack._choice == Attack.PAPER:
            return Attack.WIN

        # Ties
        if self._choice == Attack.ROCK and attack._choice == Attack.ROCK or \
            self._choice == Attack.PAPER and attack._choice == Attack.PAPER or \
            self._choice == Attack.SCISSORS and attack._choice == Attack.SCISSORS:
            # The effect is "win ties," so it's actually a win
            if self._effect == Attack.WIN_TIES and not attack._effect == Attack.WIN_TIES:
                return Attack.WIN
            # The opponent's effect is "win ties," so it's actually a loss
            if not self._effect == Attack.WIN_TIES and attack._effect == Attack.WIN_TIES:
                return Attack.LOSE
        
            # It's a normal tie (or both players have "win ties")
            return Attack.TIE

        # Something went horribly wrong, so just tie it
        return Attack.TIE
    
    # Get the damage done by this attack (if successful)
    def getDamage(self, baseAtk):
        return baseAtk * (2 if self._effect == Attack.EXTRA_DAMAGE else 1)

    # Get the amount healed by this attack
    def getHeal(self, baseAtk):
        return self.getDamage(baseAtk) if self._effect == Attack.HEAL_ON_HIT else 0
    
    # Getters
    def getChoice(self):
        return self._choice
    
    def getEffect(self):
        return self._effect
    