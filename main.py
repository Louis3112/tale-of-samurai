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

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f"assets/{self.name}/Idle/1.png").convert_alpha()
        if self.name != 'Samurai':
            img = pygame.transform.flip(img, True, False)
        self.image = pygame.transform.rotozoom(img, 0, 1.4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def draw(self):
        screen.blit(self.image, self.rect)

background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
panel_surf = pygame.image.load("assets/panel.png").convert_alpha()

# Samurai
samurai = Character(100, 270, 'Samurai', 100, 40, 3)
# Gotoku
gotoku = Character(screen_width - 100, 270, 'Gotoku', 100, 40, 3)

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
     
    # Draw background
    draw_bg()
    
    # Draw panel
    draw_panel()
    
    # Draw samurai
    samurai.draw()
    
    # Draw Gotoku
    gotoku.draw()
    
    pygame.display.update()
    clock.tick(fps)