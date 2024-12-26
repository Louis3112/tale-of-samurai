import pygame
from sys import exit

pygame.init()

# Game window screen
bottom_panel_height = 150
screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height + bottom_panel_height))
pygame.display.set_caption("Tale of Samurai")
clock = pygame.time.Clock()

running = True
fps = 30

background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
panel_surf = pygame.image.load("assets/panel.png").convert_alpha()

def draw_bg():
    screen.blit(background_surf, (0, 0))

def draw_panel():
    screen.blit(panel_surf, (0, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
     
    draw_bg()
    draw_panel()
    
    pygame.display.update()
    clock.tick(fps)