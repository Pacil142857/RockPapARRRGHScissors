from Countdown import Countdown
from HumanPlayer import HumanPlayer
from Player import Player
import pygame

class Game:
    INPUT_WINDOW_SECONDS = 1

    def __init__(self, game_display, clock, player_keybinds):
        self.game_display = game_display
        self.clock = clock
        self.game_running = True
        self.player_keybinds = player_keybinds

        self.player1 = HumanPlayer(player_keybinds[0])
        self.player2 = HumanPlayer(player_keybinds[1])

        self.countdown = Countdown(self.game_display)
        self.input_window_time_seconds = 0
        
    def update(self):
        if self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

            clock_elasped_time_second = self.clock.get_time() / 1000.0
            
            self.game_display.fill((255, 255, 255)) #fill with white color

            #Reminder: clock.get_time() returns the time since the last call to clock.tick() in milliseconds
            self.countdown.update(clock_elasped_time_second)

            if self.countdown.current_stage >= len(Countdown.STAGES) and self.input_window_time_seconds < Game.INPUT_WINDOW_SECONDS:
                input_window_time_seconds += clock_elasped_time_second

                if not self.player1.isReady():
                    self.player1.chooseAttack()
                if not self.player2.isReady():
                    self.player2.chooseAttack()
                    
            elif self.input_window_time_seconds >= Game.INPUT_WINDOW_SECONDS and self.player1.isReady() and self.player2.isReady:
                self.player1.fight(self.player2)
                self.input_window_time_seconds = 0
                self.countdown.stop()
            elif not self.player1.isReady() and not self.player2.isReady():
                self.input_window_time_seconds = 0
                self.countdown.stop()
            
            pygame.display.update()
            self.clock.tick(60)