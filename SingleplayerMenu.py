from Enums import Mode, Enemy
import AI
import pygame
from pygame_button import Button

class SingleplayerMenu:
    # Create a menu
    def __init__(self, screen):
        self._screen = screen
        self._width, self._height = screen.get_size()
        self._running = True
        self._mode = Mode.QUIT
        self._buttons = []
        self._enemy = None
        
        enemies = (self.Blunderer, self.Randall, self.Gunter, self.Quartz, self.Finn, self.Captain)
        for i, enemy in enumerate(("The Blunderer", "Boatswain Randall", "Gunner Gunter", "Quartermaster Quartz",
                      "First Mate Finn", "The Captain")):
            self._buttons.append(Button((self._width // 2 - 100, self._height // 2 - 170 + 60 * i, 200, 40),
                                        (200, 200, 200), enemies[i], text=enemy, font_color=(0, 0, 0),
                                        font=pygame.font.SysFont('maturascriptcapitals', 18), hover_color=(160, 160, 160)))
    
    # Check for button inputs
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                self._mode = Mode.QUIT
            
            for button in self._buttons:
                button.check_event(event)
        
        self._screen.fill((255, 255, 255))
        
        for button in self._buttons:
            button.update(self._screen)
        
        pygame.display.update()
    
    # Check if the main menu is running
    def isRunning(self):
        return self._running
    
    def getEnemy(self):
        return self._enemy
    
    def Blunderer(self):
        self._running = False
        self._enemy = AI.TheBlunderer()

    def Randall(self):
        self._running = False
        self._enemy = AI.Randall()

    def Gunter(self):
        self._running = False
        self._enemy = AI.Gunter()

    def Quartz(self):
        self._running = False
        self._enemy = AI.Quartz()

    def Finn(self):
        self._running = False
        self._enemy = AI.Finn()

    def Captain(self):
        self._running = False
        self._enemy = AI.Captain()