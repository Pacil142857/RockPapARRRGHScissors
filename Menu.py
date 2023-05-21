import os
from Enums import Mode
import pygame
from pygame_button import Button

class Menu:
    # Create a menu
    def __init__(self, screen):
        self._screen = screen
        self._width, self._height = screen.get_size()
        self._running = True
        self._mode = None
        self._singleplayer = Button((self._width // 2 - 75, self._height - 200, 150, 40), (200, 200, 200),
                                    self.singleplayer, text="Singleplayer (1P)", font_color=(0, 0, 0),
                                    font=pygame.font.SysFont('maturascriptcapitals', 18), hover_color=(160, 160, 160))
        self._multiplayer = Button((self._width // 2 - 75, self._height - 140, 150, 40), (200, 200, 200),
                                   self.multiplayer, text="Multiplayer (2P)", font_color=(0, 0, 0),
                                   font=pygame.font.SysFont('maturascriptcapitals', 18), hover_color=(160, 160, 160))
        
        self._background = pygame.image.load("assets" + os.sep + "images" + os.sep + "backgroundMenu.png")

        self._background_images = self.load_sprites(f"assets{os.sep}images{os.sep}backgroundMenu")
        self._background_index = 0
        self._background_image = self._background_images[self._background_index]

        self._counting_up = True
        self.frames_per_second = 10
        self.frame_count = 0
    
    # Check for button inputs
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                self._mode = Mode.QUIT
            
            self._singleplayer.check_event(event)
            self._multiplayer.check_event(event)
        
        self._screen.fill((255, 255, 255))

        #transform background to fit screen
        self._background_image = self._background_images[self._background_index]

         # increment or decrement background index every FPS
        time_per_frame = 1.0 / self.frames_per_second
        self.frame_count += 1
        if self.frame_count >= time_per_frame * 1000:
            if self._background_index < len(self._background_images) - 1 and self._counting_up:
                self._background_index += 1
            elif self._background_index == len(self._background_images) - 1:
                self._counting_up = False
                self._background_index -= 1
            elif self._background_index > 0 and not self._counting_up:
                self._background_index -= 1
            elif self._background_index == 0:
                self._counting_up = True
                self._background_index += 1
            self.frame_count -= time_per_frame * 1000

        self._background = pygame.transform.scale(self._background_image.image, (self._width, self._height))
        self._screen.blit(self._background, (0, 0))

        self._singleplayer.update(self._screen)
        self._multiplayer.update(self._screen)
        
        pygame.display.update()
    
    # Singleplayer mode
    def singleplayer(self):
       self._running = False
       self._mode = Mode.SINGLEPLAYER
    
    # Multiplayer mode
    def multiplayer(self):
        self._running = False
        self._mode = Mode.MULTIPLAYER
    
    # Get the mode selected by the player
    def getMode(self):
        return self._mode
    
    # Check if the main menu is running
    def isRunning(self):
        return self._running
    
    # Reset the menu
    def reset(self):
        self._running = True
        self._mode = None
    
    def load_sprites(self, folder_location):
        sprites = []

        for filename in sorted(os.listdir(folder_location)):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(os.path.join(folder_location, filename))
            sprite.rect = sprite.image.get_rect()

            sprites.append(sprite)

        return sprites