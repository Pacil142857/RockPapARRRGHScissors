import pygame_gui
from BouncyText import BouncyText
from Countdown import Countdown
from Enums import GameOutcome, AttackChoice
from HumanPlayer import HumanPlayer
from Player import Player
import pygame
import os
from PlayerSprite import PlayerSprite

from PlayerUI import PlayerUI

class Game:
    INPUT_WINDOW_SECONDS = 0.5
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

        self.player1_sprite = PlayerSprite(self.player1, "test_character", 2, 100, 100)
        self.player2_sprite = PlayerSprite(self.player2, "test_character", 2, 300, 100)

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

        self.board_texture = pygame.image.load(f"assets{os.sep}images{os.sep}1BottomPart{os.sep}BottomBoard.png")
        self.background_texture = pygame.image.load(f"assets{os.sep}images{os.sep}background.png")
        
    def update(self):
        delta_time_seconds = self.clock.get_time() / 1000

        self.game_display.fill((255, 255, 255)) #fill with white color
        
        #stretch the background texture so that it matches the size of the game display
        self.background_texture = pygame.transform.scale(self.background_texture, (self.game_display.get_width(), self.game_display.get_height()))

        #draw the background texture
        self.game_display.blit(self.background_texture, (0, 0))

        if self.gamestate == Game.COUNTDOWN:
            self.update_countdown(delta_time_seconds)
        elif self.gamestate == Game.INTERMISSION:
            self.update_intermission(delta_time_seconds)
        elif self.gamestate == Game.GAMEOVER:
            self.update_ending(delta_time_seconds)

        self.drawUIElements(delta_time_seconds)
        self.drawPlayers(delta_time_seconds)

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
                    is_blunderbuss = self.player1._chosenAttack == AttackChoice.SCISSORS and self.player2._chosen_attack == AttackChoice.SCISSORS
                    result = self.player1.fight(self.player2)

                    if result == GameOutcome.WIN:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(GameOutcome.LOSE, is_blunderbuss)
                    elif result == GameOutcome.LOSE:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(GameOutcome.WIN, is_blunderbuss)
                    elif result == GameOutcome.TIE:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(result, is_blunderbuss)

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

    def drawPlayers(self, delta_time_seconds):
        self.player1_sprite.draw(delta_time_seconds, self.game_display)
        self.player2_sprite.draw(delta_time_seconds, self.game_display)

    def drawUIElements(self, delta_time_seconds):
        #stretch the border texture so that it matches the hieght of the container rect of player1UI
        self.board_texture = pygame.transform.scale(self.board_texture, (self.player1UI.container_rect.width * 2, self.player1UI.container_rect.height))

        #draw the texture board using the container rect of player1UI
        self.game_display.blit(self.board_texture, self.player1UI.container_rect)

        self.ui_manager.update(delta_time_seconds)
        self.ui_manager.draw_ui(self.game_display)

        self.player1UI.update(delta_time_seconds)
        self.player2UI.update(delta_time_seconds)
        
        # Add images of the weapon triangles
        p1Hand = self.player1.getHand()
        if p1Hand.getRock().hasEffect():
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "LeftBuffRock.png")
        elif p1Hand.getPaper().hasEffect():
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "LeftBuffPaper.png")
        elif p1Hand.getScissors().hasEffect():
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "LeftBuffScissors.png")
        else:
            p1Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Left.png")
        sideLen = self.height // (1 / 0.4) - 40
        y = self.height - sideLen - 5
        x = self.width // 4 - sideLen // 2
        p1Triangle = pygame.transform.scale(p1Triangle, (sideLen, sideLen))
        self.game_display.blit(p1Triangle, (x, y, sideLen, sideLen))
        
        p2Hand = self.player2.getHand()
        if p2Hand.getRock().hasEffect():
            p2Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "RightBuffRock.png")
        elif p2Hand.getPaper().hasEffect():
            p2Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "RightBuffPaper.png")
        elif p2Hand.getScissors().hasEffect():
            p2Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "RightBuffScissors.png")
        else:
            p2Triangle = pygame.image.load("assets" + os.sep + "images" + os.sep + "1BottomPart" + os.sep + "Right.png")
        sideLen = self.height // (1 / 0.4) - 40
        y = self.height - sideLen - 5
        x = self.width // 4 * 3 - sideLen // 2
        p2Triangle = pygame.transform.scale(p2Triangle, (sideLen, sideLen))
        self.game_display.blit(p2Triangle, (x, y, sideLen, sideLen))
    
    def isRunning(self):
        return self.game_running