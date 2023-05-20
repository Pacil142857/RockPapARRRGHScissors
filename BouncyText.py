import pygame

class BouncyText:
    def __init__(self, font, text, pos, game_display):
        self.font = font
        self.text = text
        self.pos = pos
        self.game_display = game_display
                
        self.bounce_factor = 1.0
        
    def update(self):
        surface, _ = self.font.render(self.text, (0, 0, 0))   
        rect = surface.get_rect(center=(self.game_display.get_width()//2, self.game_display.get_height()//2 - 50))
                
        if self.bounce_factor > 1.0:
            self.bounce_factor *= 0.95

        surface = pygame.transform.scale(surface, (int(surface.get_width() * self.bounce_factor), int(surface.get_height() * self.bounce_factor)))
        rect = surface.get_rect(center=(self.game_display.get_width()//2, self.game_display.get_height()//2 - 50))
        
        self.current_surface = surface
        self.current_rect = rect
        
    def draw(self):
        self.game_display.blit(self.current_surface, self.current_rect)