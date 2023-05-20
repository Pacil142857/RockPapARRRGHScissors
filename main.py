#create a starter project using pygame
from Player import Player
import pygame

pygame.init()

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Test')

white = (255, 255, 255)
clock = pygame.time.Clock()


player1 = Player()
player2 = Player()

# define a game loop
def game_loop():
    game_running = True
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        
        game_display.fill(white)
                
        pygame.display.update()
        
        clock.tick(60)

game_loop()

pygame.quit()
