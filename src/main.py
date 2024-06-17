import pygame

# general setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')


while running:
    
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draw the game
    # fill window with red color
    
    display_surface.fill('blue')

    pygame.display.update()
    
    
pygame.quit()