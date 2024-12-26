import pygame
from sys import exit

pygame.init()

# Game window screen
bottom_panel_height = 150
screen_width = 800
screen_height = 400
img_scale_ratio = 1.5

screen = pygame.display.set_mode((screen_width, screen_height + bottom_panel_height))
pygame.display.set_caption("Tale of Samurai")
clock = pygame.time.Clock()

running = True
fps = 60

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.animation_index = 0 
        self.animation_action = 3 # 0: Idle, 1: Attack, 2: Hurt, 3: Die
        self.current_time = pygame.time.get_ticks()
        
        # Idle animation
        temp_animation_list = []
        for i in range(1, 6):
            img = pygame.image.load(f"assets/{self.name}/Idle/{i}.png").convert_alpha()
            if self.name != 'Samurai':
                img = pygame.transform.flip(img, True, False)
            img = pygame.transform.rotozoom(img, 0, img_scale_ratio)
            temp_animation_list.append(img)
        self.animation_list.append(temp_animation_list)
        
        # Attack animation
        temp_animation_list = []
        for i in range(1, 7):
            if self.name != 'Samurai':
                img = pygame.image.load(f"assets/{self.name}/Attack_3/{i}.png").convert_alpha()
                img = pygame.transform.flip(img, True, False)
            else:
                img = pygame.image.load(f"assets/{self.name}/Attack_1/{i}.png").convert_alpha()
            img = pygame.transform.rotozoom(img, 0, img_scale_ratio)
            temp_animation_list.append(img)
        self.animation_list.append(temp_animation_list)
        
        # Hurt animation
        temp_animation_list = []
        for i in range(1, 4):
            img = pygame.image.load(f"assets/{self.name}/Hurt/{i}.png").convert_alpha()
            if self.name != 'Samurai':
                img = pygame.transform.flip(img, True, False)
            img = pygame.transform.rotozoom(img, 0, img_scale_ratio)
            temp_animation_list.append(img)
        self.animation_list.append(temp_animation_list)
        
        # Death animation
        temp_animation_list = []
        for i in range(1, 6):
            img = pygame.image.load(f"assets/{self.name}/Dead/{i}.png").convert_alpha()
            if self.name != 'Samurai':
                img = pygame.transform.flip(img, True, False)
            img = pygame.transform.rotozoom(img, 0, img_scale_ratio)
            temp_animation_list.append(img)
        self.animation_list.append(temp_animation_list)
        
        self.image = self.animation_list[self.animation_action][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def animation(self):
        animation_delay = 150
        if self.animation_action == 3:
            animation_delay = 200
        self.image = self.animation_list[int(self.animation_action)][int(self.animation_index)]
        if pygame.time.get_ticks() - self.current_time >= animation_delay:
            self.current_time = pygame.time.get_ticks()
            self.animation_index += 1
            if self.animation_index >= len(self.animation_list[self.animation_action]):
                self.animation_index = 0
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        self.animation()

background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
panel_surf = pygame.image.load("assets/panel.png").convert_alpha()

# Samurai
samurai = Character(100, 270, 'Samurai', 100, 45, 3)

gotoku = Character(screen_width - 100, 270, 'Gotoku', 150, 25, 2)
yorei = Character(screen_width - 200, 180, 'Yorei', 80, 40, 1)
enemies = []
enemies.append(gotoku)
enemies.append(yorei)

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
    samurai.update()
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
        enemy.update()
    
    pygame.display.update()
    clock.tick(fps)