import pygame
import time

class Countdown:
    STAGES = ['Three', 'Two', 'One', 'Aye!']
    SECONDS_PER_STAGE = 0.75

    def __init__(self, game_display):
        self.current_stage = -1
        self.game_display = game_display
        self.font = pygame.freetype.SysFont('Arial', 30)

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
            self.bounce_factor = 1.5

        current_stage_surface, _ = self.font.render(Countdown.STAGES[self.current_stage], (0, 0, 0))
        current_stage_rect = current_stage_surface.get_rect(center=(self.game_display.get_width()//2, self.game_display.get_height()//2 - 50))
                
        # apply bounce effect
        if self.bounce_factor > 1.0:
            self.bounce_factor *= 0.95

        current_stage_surface = pygame.transform.scale(current_stage_surface, (int(current_stage_surface.get_width() * self.bounce_factor), int(current_stage_surface.get_height() * self.bounce_factor)))
        current_stage_rect = current_stage_surface.get_rect(center=(self.game_display.get_width()//2, self.game_display.get_height()//2 - 50))
        
        self.game_display.blit(current_stage_surface, current_stage_rect)