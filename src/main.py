import pygame
from os.path import join
from random import randint

# general setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100

# importing image
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
star_positions = [(randint(10,WINDOW_WIDTH),randint(10,WINDOW_HEIGHT)) for i in range(20)]
AMOUNT_OF_STARS=20

while running:
    
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draw the game
    # fill window with red color
    x +=0.1
    display_surface.fill('darkgrey')

    for pos in star_positions:   
        display_surface.blit(star_surf,pos)
        
    display_surface.blit(player_surf,(x,150))

    pygame.display.update()
    
    
pygame.quit()