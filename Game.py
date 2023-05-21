import pygame_gui
from BouncyText import BouncyText
from Countdown import Countdown
from HumanPlayer import HumanPlayer
from Player import Player
import pygame
import os

from PlayerUI import PlayerUI

class Game:
    INPUT_WINDOW_SECONDS = 1
    INTERMISSION_TIME_SECONDS = 3
    GAMEOVER_SECONDS = 3

    COUNTDOWN = 1
    INTERMISSION = 2
    GAMEOVER = 3

    def __init__(self, game_display, clock, player1, player2):
        self.game_display = game_display
        self.clock = clock
        self.game_running = True
        
        self.width, self.height = self.game_display.get_size()

        self.player1 = player1
        self.player2 = player2

        self.countdown = Countdown(self.game_display)
        self.input_window_time_seconds = 0
        self.intermission_time_seconds = 0

        self.gamestate = Game.INTERMISSION

        self.font = self.countdown.font

        display_width, display_height = pygame.display.get_surface().get_size()

        self.ui_manager = pygame_gui.UIManager((display_width, display_height))
        self.player1UI = PlayerUI(self.player1, pygame.Rect((0, display_height * 0.6), (display_width / 2, display_height * 0.4)), self.ui_manager, self.game_display)
        self.player2UI = PlayerUI(self.player2, pygame.Rect((display_width / 2, display_height * 0.6), (display_width / 2, display_height * 0.4)), self.ui_manager, self.game_display)

        self.gameover_text = BouncyText(self.font, "", (self.game_display.get_width()//2, self.game_display.get_height()//2 - 50), self.game_display)
        self.gameover_time_seconds = 0
        
    def update(self):
        delta_time_seconds = self.clock.get_time() / 1000

        self.game_display.fill((255, 255, 255)) #fill with white color

        if self.gamestate == Game.COUNTDOWN:
            self.update_countdown(delta_time_seconds)
        elif self.gamestate == Game.INTERMISSION:
            self.update_intermission(delta_time_seconds)
        elif self.gamestate == Game.GAMEOVER:
            self.update_ending(delta_time_seconds)

        self.drawUIElements(delta_time_seconds)    
        
        # Add images of the weapon triangles
        p1Hand = self.player1.getHand()
        if p1Hand.getRock().hasEffect():
            # TODO: Change to buff image
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Left.png")
        elif p1Hand.getPaper().hasEffect():
            # TODO: see above
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Left.png")
        elif p1Hand.getScissors().hasEffect():
            # TODO: see above
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Left.png")
        else:
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Left.png")
        sideLen = self.height // (1 / 0.4) - 0
        y = self.height - sideLen + 35
        x = self.width // 4 - sideLen // 2
        p1Triangle = pygame.transform.scale(p1Triangle, (sideLen, sideLen))
        self.game_display.blit(p1Triangle, (x, y, sideLen, sideLen)) # TODO: use relative coordinates

        pygame.display.update()
        self.clock.tick(60)

    def update_countdown(self, delta_time_seconds):
        if not self.game_running:
            return
        
        key_down_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.quit()
                quit()
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

                if self.player1.getHP() <= 0 or self.player2.getHP() <= 0:
                    self.gamestate = Game.GAMEOVER
                else:
                    self.gamestate = Game.INTERMISSION

        
    def update_intermission(self, delta_time_seconds):
        if self.intermission_time_seconds < Game.INTERMISSION_TIME_SECONDS:
            self.intermission_time_seconds += delta_time_seconds
        else:
            self.intermission_time_seconds = 0
            self.countdown.start()

            self.gamestate = Game.COUNTDOWN
    
    def update_ending(self, delta_time_seconds):
        self.gameover_text.text = f"{self.player1.getName()} wins!" if self.player1.getHP() > 0 else f"{self.player2.getName()} wins!"

        self.gameover_text.update()
        self.gameover_text.draw()

        self.gameover_time_seconds += delta_time_seconds
        if self.gameover_time_seconds > Game.GAMEOVER_SECONDS:
            self.game_running = False

        pass

    def drawUIElements(self, delta_time_seconds):
        self.ui_manager.update(delta_time_seconds)
        self.ui_manager.draw_ui(self.game_display)

        self.player1UI.update(delta_time_seconds)
        self.player2UI.update(delta_time_seconds)
    
    def isRunning(self):
        return self.game_running