import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Tale of Samurai")
clock = pygame.time.Clock()
font_sm = pygame.font.Font("font/Pixeltype.ttf", 24)

running = True
fps = 30

background_surf = pygame.transform.scale(pygame.image.load("graphics/background.png"), (1200, 800))
test_font_surf = font_sm.render("Hello World!", True, (255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
     
    screen.blit(background_surf, (0, 0))
    screen.blit(test_font_surf, (100, 100))
    
    pygame.display.update()
    clock.tick(fps)