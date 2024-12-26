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
font_sm = pygame.font.Font("font/Pixeltype.ttf", 24)

running = True
fps = 30

background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
test_font_surf = font_sm.render("Hello World!", True, (255, 255, 255))

def draw_bg():
    screen.blit(background_surf, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
     
    draw_bg()
    screen.blit(test_font_surf, (100, 100))
    
    pygame.display.update()
    clock.tick(fps)