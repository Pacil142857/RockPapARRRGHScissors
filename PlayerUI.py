import pygame
import pygame_gui
import os

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
        self._element_container.image = None

        self._hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((0, 0), (container_width, bar_thickness)), manager=ui_manager, container=self._element_container)
        self._hp_bar.border_colour = pygame.Color('Grey')
        self._hp_bar.border_width = 2

        # Adding Player Name
        self._font = pygame.freetype.SysFont('maturascriptcapitals', 20)
        self._surface, _ = self._font.render(self.player.getName(), (0, 0, 0))
        
    def update(self, delta_time):
        self.update_health_bar(delta_time)
        self._element_container.update(delta_time)

        self._element_container.background_colour = pygame.Color('White')
               
        rect = self._surface.get_rect(center=(self._hp_bar.rect.centerx, self._hp_bar.rect.centery))
        self.screen.blit(self._surface, rect)

    def update_health_bar(self, delta_time):
        percentage_health = self.player.getHP() / 100

        # Lerp between green and yellow, then yellow to red
        if percentage_health >= 0.5:
            # Green to yellow
            self.health_bar_color = self.lerp_color(pygame.Color('Green'), pygame.Color('Yellow'), (1 - percentage_health) * 2)
        else:
            # Yellow to red
            self.health_bar_color = self.lerp_color(pygame.Color('Yellow'), pygame.Color('Red'), 1 - (percentage_health * 2))

        self.health_bar_color.a = 0

        self._hp_bar.bar_filled_colour = self.health_bar_color
        self._hp_bar.percent_full = percentage_health * 100

        self._hp_bar.update(delta_time)
    
    def lerp_color(self, start_color, end_color, t):
        r = start_color.r + (end_color.r - start_color.r) * t
        g = start_color.g + (end_color.g - start_color.g) * t
        b = start_color.b + (end_color.b - start_color.b) * t
        a = start_color.a + (end_color.a - start_color.a) * t
        
        return pygame.Color(int(r), int(g), int(b), int(a))


