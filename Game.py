from Countdown import Countdown
from Player import Player
import pygame

class Game:
    def __init__(self, game_display, clock):
        self.game_display = game_display
        self.clock = clock
        self.game_running = True

        self.player1 = Player()
        self.player2 = Player()

        self.countdown = Countdown(self.game_display)
        
    def update(self):
        if self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
            
            self.game_display.fill((255, 255, 255)) #fill with white color

            #Reminder: clock.get_time() returns the time since the last call to clock.tick() in milliseconds
            self.countdown.update(self.clock.get_time() / 1000.0)
                    
            pygame.display.update()
            self.clock.tick(60)