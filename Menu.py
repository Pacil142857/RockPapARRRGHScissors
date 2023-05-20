from Enums import Mode
import pygame
from pygame_button import Button

class Menu:
    # Create a menu
    def __init__(self, screen):
        self._screen = screen
        self._width, self._height = screen.get_size()
        self._running = True
        self._font = pygame.freetype.Font(None, 30)
        self._mode = Mode.QUIT
        self._singleplayer = Button((self._width // 2 - 75, self._height - 200, 150, 40), (200, 200, 200),
                                    self.singleplayer, text="Singleplayer (1P)", font_color=(0, 0, 0),
                                    font=pygame.font.Font(None, 24), hover_color=(160, 160, 160))
        self._multiplayer = Button((self._width // 2 - 75, self._height - 140, 150, 40), (200, 200, 200),
                                   self.multiplayer, text="Multiplayer (2P)", font_color=(0, 0, 0),
                                   font=pygame.font.Font(None, 24), hover_color=(160, 160, 160))
    
    # Check for button inputs
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                self._mode = Mode.QUIT
            
            self._singleplayer.check_event(event)
            self._multiplayer.check_event(event)
        
        self._screen.fill((255, 255, 255))
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