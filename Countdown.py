import pygame
import time

class Countdown:
    STAGES = ['Rock', 'Paper', 'Scissors', 'Shoot!']
    SECONDS_PER_STAGE = 0.75

    def __init__(self, game_display):
        self.current_stage = -1
        self.game_display = game_display
    
    def start(self):
        self.current_stage = 0
        self.current_stage_time_seconds = 0
    
    def stop(self):
        self.current_stage = -1
        self.current_stage_time_seconds = 0
    
    def isActive(self):
        return self.current_stage > -1 and self.current_stage < len(Countdown.STAGES)

    def update(self, game_time_seconds):
        if not self.isActive():
            return

        self.current_stage_time_seconds += game_time_seconds

        if self.current_stage_time_seconds >= Countdown.SECONDS_PER_STAGE:
            self.current_stage += 1
            self.current_stage_time_seconds -= Countdown.SECONDS_PER_STAGE
        