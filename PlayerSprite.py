import pygame
from Enums import GameOutcome
from Player import Player
import os

class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, player, character_name, frames_per_second, x, y):
        super().__init__()
        self.player = player
        self.x = x
        self.y = y
        self.frames_per_second = frames_per_second

        self.idle_frames = self.load_sprites(f"assets/images/{character_name}/idle")
        self.win_frames = self.load_sprites(f"assets/images/{character_name}/win")
        self.tie_frames = self.load_sprites(f"assets/images/{character_name}/tie")
        self.lose_frames = self.load_sprites(f"assets/images/{character_name}/lose")
        self.blunderbuss_win_frames = self.load_sprites(f"assets/images/{character_name}/blunderbuss_win")
        self.blunderbuss_lose_frames = self.load_sprites(f"assets/images/{character_name}/blunderbuss_lose")

        self.current_frames = self.win_frames  # Start with the "win" animation

        # Set the initial image and rect for the sprite
        self.current_frame_index = 0
        self.image = self.current_frames[self.current_frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, delta_time_seconds, surface):
        # Draw the current sprite and adjust frames based on the FPS
      
        # Update the animation frame based on elapsed time, to ensure consistent speed
        time_per_frame = 1.0 / self.frames_per_second
        self.current_frame_index += delta_time_seconds / time_per_frame
        if self.current_frame_index >= len(self.current_frames):
            self.current_frame_index = 0

        # Set the current image and rect for the sprite
        self.image = self.current_frames[int(self.current_frame_index)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Draw the current sprite on the surface
        surface.blit(self.image, self.rect)
    
    def load_sprites(self, folder_location):
        sprite_group = pygame.sprite.Group()

        for filename in os.listdir(folder_location):
            sprite_group.add(pygame.image.load(os.path.join(folder_location, filename)))

        return sprite_group