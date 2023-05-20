import pygame
import time

from BouncyText import BouncyText

class Countdown:
    STAGES = ['Three', 'Two', 'One', 'Aye!']
    SECONDS_PER_STAGE = 0.75

    def __init__(self, game_display):
        self.current_stage = -1
        self.game_display = game_display
        self.font = pygame.freetype.SysFont('Arial', 30)
        self.countdown_text = BouncyText(self.font, "", (0, 0), self.game_display)

    def start(self):
        self.current_stage = 0
        self.current_stage_time_seconds = 0
        self.bounce_factor = 1.0

    def stop(self):
        self.current_stage = -1
        self.current_stage_time_seconds = 0
    
    def isActive(self):
        return self.current_stage > -1 and self.current_stage < len(Countdown.STAGES)

    def update(self, game_time_seconds):
        if not self.isActive():
            return

        self.current_stage_time_seconds += game_time_seconds

        if self.current_stage_time_seconds >= Countdown.SECONDS_PER_STAGE and self.current_stage < len(Countdown.STAGES) - 1:
            self.current_stage += 1
            self.current_stage_time_seconds -= Countdown.SECONDS_PER_STAGE
            self.countdown_text.bounce_factor = 1.5

        self.countdown_text.update()
        self.countdown_text.draw()