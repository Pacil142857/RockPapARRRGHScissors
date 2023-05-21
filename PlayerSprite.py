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

        self.idle_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}idle")
        self.win_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}win")
        self.tie_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}tie")
        self.lose_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}lose")
        self.blunderbuss_win_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}blunderbuss_win")
        self.blunderbuss_lose_frames = self.load_sprites(f"assets{os.sep}images{os.sep}{character_name}{os.sep}blunderbuss_lose")

        self.current_frames = self.idle_frames

        # Set the initial image and rect for the sprite
        self.current_frame_index = 0
        self.current_sprite = self.current_frames[self.current_frame_index]
        self.rect = self.current_sprite.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, delta_time_seconds, surface):
        # Draw the current sprite and adjust frames based on the FPS
      
        # Update the animation frame based on elapsed time, to ensure consistent speed
        time_per_frame = 1.0 / self.frames_per_second
        self.current_frame_index += delta_time_seconds / time_per_frame
        if self.current_frame_index >= len(self.current_frames):
            self.current_frame_index = 0
            self.current_frames = self.idle_frames

        # Set the current image and rect for the sprite
        self.current_sprite = self.current_frames[int(self.current_frame_index)]
        self.rect = self.current_sprite.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Draw the current sprite on the surface
        surface.blit(self.current_sprite.image, self.rect)
    
    def change_anim(self, game_outcome, is_blunderbuss):
        if game_outcome == GameOutcome.WIN:
            self.current_frames = self.win_frames if not is_blunderbuss else self.blunderbuss_win_frames
        elif game_outcome == GameOutcome.TIE:
            self.current_frames = self.tie_frames
        elif game_outcome == GameOutcome.LOSE:
            self.current_frames = self.lose_frames if not is_blunderbuss else self.blunderbuss_lose_frames
        else:
            self.current_frames = self.idle_frames

        self.current_frame_index = 0
    
    def load_sprites(self, folder_location):
        sprites = []

        for filename in sorted(os.listdir(folder_location)):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(os.path.join(folder_location, filename))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.x
            sprite.rect.y = self.y

            sprites.append(sprite)

        return sprites