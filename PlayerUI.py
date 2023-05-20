import pygame
import pygame_gui

class PlayerUI:
    def __init__(self, player, container_rect, ui_manager, screen):
        self.player = player
        self.ui_manager = ui_manager        
        self.container_rect = container_rect
        self.screen = screen

        self._element_container = pygame_gui.elements.UIPanel(relative_rect=self.container_rect, manager=ui_manager)
        self._hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((0, 0), (self.container_rect.width, 20)), manager=ui_manager, container=self._element_container)

    def draw(self):
        self.ui_manager.draw_ui(self.screen)

