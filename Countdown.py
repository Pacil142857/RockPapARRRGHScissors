import pygame
import time

class Countdown:
    STAGES = ['Flintlock', 'Cutlass', 'Blunderbuss', 'Aye!']
    SECONDS_PER_STAGE = 0.75

    def __init__(self, game_display):
        self.current_stage = -1
        self.game_display = game_display
        self.font = pygame.font.SysFont('Arial', 30)

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
        
        current_stage_text = self.font.render(Countdown.STAGES[self.current_stage], True, (255, 255, 255))
        current_stage_rect = current_stage_text.get_rect(center=(self.game_display.get_width()//2, self.game_display.get_height()//2 - 50))
        self.game_display.blit(current_stage_text, current_stage_rect)
        