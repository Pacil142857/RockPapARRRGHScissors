import pygame_gui
from Countdown import Countdown
from HumanPlayer import HumanPlayer
from Player import Player
import pygame

from PlayerUI import PlayerUI

class Game:
    INPUT_WINDOW_SECONDS = 1
    INTERMISSION_TIME_SECONDS = 3

    def __init__(self, game_display, clock, player1, player2):
        self.game_display = game_display
        self.clock = clock
        self.game_running = True

        self.player1 = player1
        self.player2 = player2

        self.countdown = Countdown(self.game_display)
        self.input_window_time_seconds = 0
        self.intermission_time_seconds = 0

        display_width, display_height = pygame.display.get_surface().get_size()

        self.ui_manager = pygame_gui.UIManager((display_width, display_height))
        self.player1UI = PlayerUI(self.player1, pygame.Rect((0, display_height * 0.67), (display_width / 2, display_height * 0.33)), self.ui_manager, self.game_display)
        self.player2UI = PlayerUI(self.player2, pygame.Rect((display_width / 2, display_height * 0.67), (display_width / 2, display_height * 0.33)), self.ui_manager, self.game_display)
        
    def update(self):
        delta_time_seconds = self.clock.get_time() / 1000

        self.game_display.fill((255, 255, 255)) #fill with white color

        if self.countdown.isActive():
            self.update_countdown(delta_time_seconds)
        else:
            self.update_intermission(delta_time_seconds)

        self.drawUIElements(delta_time_seconds)    
        pygame.display.update()
        self.clock.tick(60)

    def update_countdown(self, delta_time_seconds):
        if not self.game_running:
            return
        
        key_down_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            if event.type == pygame.KEYDOWN:
                key_down_events.append(event)
        
        #Reminder: clock.get_time() returns the time since the last call to clock.tick() in milliseconds
        self.countdown.update(delta_time_seconds)

        if self.countdown.current_stage >= len(Countdown.STAGES) - 1:
            if self.input_window_time_seconds < Game.INPUT_WINDOW_SECONDS:
                self.input_window_time_seconds += delta_time_seconds

                if not self.player1.isReady():
                    self.player1.chooseAttack(key_down_events)
                if not self.player2.isReady():
                    if type(self.player2) == HumanPlayer:
                        self.player2.chooseAttack(key_down_events)
                    else:
                        self.player2.chooseAttack()
                    
            elif self.input_window_time_seconds >= Game.INPUT_WINDOW_SECONDS:
                if self.player1.isReady() and self.player2.isReady():
                    self.player1.fight(self.player2)

                self.input_window_time_seconds = 0
                self.countdown.stop()

        
    def update_intermission(self, delta_time_seconds):
        if self.intermission_time_seconds < Game.INTERMISSION_TIME_SECONDS:
            self.intermission_time_seconds += delta_time_seconds
        else:
            self.intermission_time_seconds = 0
            self.countdown.start()

    def drawUIElements(self, delta_time_seconds):
        self.ui_manager.update(delta_time_seconds)
        self.ui_manager.draw_ui(self.game_display)

        self.player1UI.update(delta_time_seconds)
        self.player2UI.update(delta_time_seconds)
    
    def isRunning(self):
        return self.game_running