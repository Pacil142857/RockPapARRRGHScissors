import pygame
import pygame_gui

class PlayerUI:
    def __init__(self, player, container_rect, ui_manager, screen):
        self.player = player
        self.ui_manager = ui_manager        
        self.container_rect = container_rect
        self.screen = screen

        self.health_bar_color = pygame.Color('Green')

        container_width, container_height = self.container_rect.size
        bar_thickness = 50

        self._element_container = pygame_gui.elements.UIPanel(relative_rect=self.container_rect, manager=ui_manager)
        self._hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((0, 0), (container_width, bar_thickness)), manager=ui_manager, container=self._element_container)
        self._hp_bar.border_colour = pygame.Color('Grey')
        self._hp_bar.border_width = 2

        
    def update(self, delta_time):
        self.update_health_bar(delta_time)

    def update_health_bar(self, delta_time):
        percentage_health = self.player.getHP() / 100

        # Lerp between green and yellow, then yellow to red
        if percentage_health > 0.5:
            # Green to yellow
            new_val = (1 - percentage_health) * 2
            self.health_bar_color.r = 255
            self.health_bar_color.g = int(255 * new_val)
        else:
            # Yellow to red
            new_val = percentage_health * 2
            self.health_bar_color.r = int(255 * new_val)
            self.health_bar_color.g = 255

        self.health_bar_color.a = 0

        self._hp_bar.bar_filled_colour = self.health_bar_color
        self._hp_bar.percent_full = percentage_health * 100
        
        self._hp_bar.update(delta_time)


