from enum import Enum

class AttackChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class GameOutcome(Enum):
    WIN = 1
    TIE = 0
    LOSE = -1

class AttackEffect(Enum):
    EXTRA_DAMAGE = 1
    HEAL_ON_HIT = 2
    WIN_TIES = 3

class Mode(Enum):
    SINGLEPLAYER = 1
    MULTIPLAYER = 2
    QUIT = 0

class Enemy(Enum):
    BLUNDERER = 1
    RANDALL = 2
    GUNTER = 3
    QUARTZ = 4
    FINN = 5
    CAPTAIN = 6