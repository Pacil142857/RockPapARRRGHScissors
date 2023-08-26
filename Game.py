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
        #clock
        self.game_display = game_display
        self.clock = clock
        self.game_running = True
        
        self.width, self.height = self.game_display.get_size()

        #players
        self.player1 = player1
        self.player2 = player2

        self.player1_sprite = PlayerSprite(self.player1, "test_character", 2, 100, 100)
        self.player2_sprite = PlayerSprite(self.player2, "test_character", 2, 300, 100)

        # animated elements
        self._background_images = self.load_sprites(f"assets{os.sep}images{os.sep}OceanBackground")
        self._background_index = 0 #starting index
        self._background_image = self._background_images[self._background_index]

        self._idle_images = self.load_sprites(f"assets{os.sep}images{os.sep}Idle")
        self._idle_index = 0 #starting index
        self._idle_image = self._idle_images[self._idle_index]


        

        self._attack_animation_playing = False
        self._attack_animation_images = self.load_sprites(f"assets{os.sep}images{os.sep}Idle") #temporary
        self._attack_animation_index = 0
        self._attack_animation_image = self._attack_animation_images[self._attack_animation_index]

        #frame things
        self._counting_up = True
        self.frames_per_second = 30
        self.frame_count = 0

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
        
        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play(-1)
    
    def update(self):
        delta_time_seconds = self.clock.get_time() / 1000

        self.game_display.fill((65, 168, 209)) #fill with white color
        
        
        self._background_image = self._background_images[self._background_index]
        self._idle_image = self._idle_images[self._idle_index]

        #p1Hand = self.player1.getHand().getAttack

        # update the attack animation if playing, stop when ended.
        if(self._attack_animation_playing):
            self._attack_animation_index += 1
            if(self._attack_animation_index>=len(self._attack_animation_images)):
                self._attack_animation_index = 0
                self._attack_animation_playing = False
            self._attack_animation_image = self._attack_animation_images[self._attack_animation_index]

        # increment or decrement background index every FPS
        time_per_frame = 1.0 / self.frames_per_second

        self.frame_count += 1
        if self.frame_count >= time_per_frame * 100:
            #update background
            self._background_index+=1
            if(self._background_index>=len(self._background_images)):
                self._background_index=0
            #update idle
            self._idle_index+=1
            if(self._idle_index>=len(self._idle_images)):
                self._idle_index=0

            self.frame_count -= time_per_frame * 100 

        #use this if the animations are not looping. All assets in this game will naturally loop. 
        #this uses _background_index as an example but may be done with the index of any element

        # if self.frame_count >= time_per_frame * 100:
        #     if self._background_index < len(self._background_images) - 1 and self._counting_up:
        #         self._background_index += 1
        #     elif self._background_index == len(self._background_images) - 1:
        #         self._counting_up = False
        #         self._background_index -= 1
        #     elif self._background_index > 0 and not self._counting_up:
        #         self._background_index -= 1
        #     elif self._background_index == 0:
        #         self._counting_up = True
        #         self._background_index += 1
        #     self.frame_count -= time_per_frame * 100    

        #transform image
        display_width, display_height = pygame.display.get_surface().get_size()
        self._background = pygame.transform.scale(self._background_image.image, (display_width, display_height * 0.66))
        self._idle = pygame.transform.scale(self._idle_image.image, (display_width, display_height * 0.66))
        self._attack_animation = pygame.transform.scale(self._attack_animation_image.image, (display_width, display_height * 0.66))
        
        
        self.game_display.blit(self._background, (0, 0))
        if(self._attack_animation_playing):
            self.game_display.blit(self._attack_animation, (0, 0))
        else:
            self.game_display.blit(self._idle, (0, 0))
        
        if self.gamestate == Game.COUNTDOWN:
            self.update_countdown(delta_time_seconds)
        elif self.gamestate == Game.INTERMISSION:
            self.update_intermission(delta_time_seconds)
        elif self.gamestate == Game.GAMEOVER:
            self.update_ending(delta_time_seconds)

        self.drawUIElements(delta_time_seconds)
        #self.drawPlayers(delta_time_seconds)

        pygame.display.update()
        self.clock.tick(60)

    def update_countdown(self, delta_time_seconds):
        if not self.game_running:
            return
        
        key_down_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.mixer.music.stop()
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
                    #rock is cutlass
                    #paper is flintlock
                    #scissors is blunder 
                    choice1 = self.player1.getChosenAttack().getChoice()
                    choice2 = self.player2.getChosenAttack().getChoice()
                    
                    stringChoice1 =''
                    stringChoice2=''

                    if(choice1 == AttackChoice.ROCK):
                        stringChoice1 = 'Flint'
                    elif (choice1 == AttackChoice.PAPER):
                        stringChoice1 = 'Cut'
                    elif (choice1 == AttackChoice.SCISSORS):
                        stringChoice1 = 'Blund'

                    if(choice2 == AttackChoice.ROCK):
                        stringChoice2 = 'Flint'
                    elif (choice2 == AttackChoice.PAPER):
                        stringChoice2 = 'Cut'
                    elif (choice2 == AttackChoice.SCISSORS):
                        stringChoice2 = 'Blund'

                    is_blunderbuss = self.player1._chosenAttack == AttackChoice.SCISSORS and self.player2._chosen_attack == AttackChoice.SCISSORS
                    result = self.player1.fight(self.player2)
                    stringResult = ''
                    if result == GameOutcome.WIN:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(GameOutcome.LOSE, is_blunderbuss)
                        stringResult = 'Wins'
                        
                    elif result == GameOutcome.LOSE:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(GameOutcome.WIN, is_blunderbuss)
                        stringResult = 'Loses'
                        
                    elif result == GameOutcome.TIE:
                        self.player1_sprite.change_anim(result, is_blunderbuss)
                        self.player2_sprite.change_anim(result, is_blunderbuss)
                        stringResult = 'Ties'
                        
                    
                    
                    stringFileName = 'Red' + stringChoice1 + stringResult + 'Blue' + stringChoice2
                    
                    self._attack_animation_playing = True
                    self._attack_animation_images = self.load_sprites(f"assets{os.sep}images{os.sep}" + stringFileName) #temporary
                    self._attack_animation_index = 0
                    self._attack_animation_image = self._attack_animation_images[self._attack_animation_index]

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
            pygame.mixer.music.stop()

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

    def load_sprites(self, folder_location):
        sprites = []

        for filename in sorted(os.listdir(folder_location)):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(os.path.join(folder_location, filename))
            sprite.rect = sprite.image.get_rect()

            sprites.append(sprite)

        return sprites