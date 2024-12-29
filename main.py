import pygame
from sys import exit
from random import randint

pygame.init()

# Game window screen
bottom_panel_height = 150
screen_width = 800
screen_height = 400

# Game variables
img_scale_ratio = 1.5

screen = pygame.display.set_mode((screen_width, screen_height + bottom_panel_height))
clock = pygame.time.Clock()

# Fonts
font_style = "Pixeltype"
fonts = {
    "default": pygame.font.Font(f"font/{font_style}.ttf", 24),
    "sm": pygame.font.Font(f"font/{font_style}.ttf", 20),
    "md": pygame.font.Font(f"font/{font_style}.ttf", 32),
    "lg": pygame.font.Font(f"font/{font_style}.ttf", 40),
}

# Colors
colors = {
    "white" : '#FFFFFF',
    "black" : '#000000',
    "brown" : '#AB886D',
    "green" : '#AFD198',
    "red" : '#9B4444',
}

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
        self.animation_action = 0 # 0: Idle, 1: Attack, 2: Hurt, 3: Die
        self.current_time = pygame.time.get_ticks()
        self.alpha = 255
        
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
        animation_delay = 100
        if self.animation_action == 3:
            animation_delay = 200
        self.image = self.animation_list[int(self.animation_action)][int(self.animation_index)]
        if pygame.time.get_ticks() - self.current_time >= animation_delay:
            self.current_time = pygame.time.get_ticks()
            self.animation_index += 1
            if self.animation_index >= len(self.animation_list[self.animation_action]):
                self.idle()
    
    def draw(self):
        if not self.alive:
            self.animation_action = 3
            self.animation_index = len(self.animation_list[3]) - 1
            
            if self.name != 'Samurai':
                if not hasattr(self, 'alpha'):
                    self.alpha = 255
                if self.alpha > 0:
                    self.alpha -= 10
                    self.image.set_alpha(self.alpha)
                else:
                    self.image.set_alpha(0)
            else:
                self.image = self.animation_list[3][self.animation_index]
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, self.rect)
    
    def idle(self):
        self.animation_action = 0
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
    
    def die(self):
        self.alive = False
        self.animation_action = 3
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
    
    def attack(self, target):
        rand_dmg = randint(-5, 5)
        damage = self.strength + rand_dmg
        target.hp -= damage
        target.animation_action = 2
        target.animation_index = 0
        target.current_time = pygame.time.get_ticks()
        self.animation_action = 1
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
        if target.hp <= 0:
            target.hp = 0
            target.die()
        
    def update(self):
        self.animation()

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.width = 250
        self.height = 25
        self.border_radius = 10
        self.health_bar_value = (self.hp / self.max_hp) * self.width
        
    def draw(self, hp):
        self.hp = hp
        self.health_bar_value = (self.hp / self.max_hp) * self.width
        bar_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(bar_surf, colors['red'], (0, 0, self.width, self.height), border_radius=self.border_radius)
        
        pygame.draw.rect(bar_surf, colors['green'], (0, 0, self.health_bar_value, self.height), border_radius=self.border_radius)
        pygame.draw.rect(bar_surf, colors['brown'], (0, 0, self.width, self.height), width=5, border_radius=self.border_radius)
        screen.blit(bar_surf, (self.x, self.y)) # 475

def draw_bg(bg_surf):
    screen.blit(bg_surf, (0, 0))

def draw_text(text, x, y, font, color):
    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect(center = (x, y))
    screen.blit(text_surf, text_rect)

def play():
    
    screen.fill(colors['black'])
    
    pygame.display.set_caption("Tale of Samurai: Battle")
    
    running = True
    fps = 60
    
    current_character = 1
    total_characters = 3
    action_cooldown = 0
    action_delay = 100
    clicked = False
    
    background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
    panel_surf = pygame.image.load("assets/panel.png").convert_alpha()
    sword_surf = pygame.image.load("assets/sword.png").convert_alpha()
    
    # Samurai
    samurai = Character(100, 270, 'Samurai', 100, 60, 3)
    samurai_health_bar = HealthBar(80, screen_height + bottom_panel_height / 2, samurai.hp, samurai.max_hp)

    # Enemies - Gotoku and Yorei
    gotoku = Character(screen_width - 100, 270, 'Gotoku', 120, 25, 2)
    gotoku_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) - 30, gotoku.hp, gotoku.max_hp)
    yorei = Character(screen_width - 200, 180, 'Yorei', 80, 30, 1)
    yorei_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) + 30, yorei.hp, yorei.max_hp)
    enemies = []
    enemies.append(gotoku)
    enemies.append(yorei)

    def draw_panel():
        screen.blit(panel_surf, (0, screen_height))
        
        # Samurai stats
        draw_text(f"{samurai.name}" , 110, (screen_height + bottom_panel_height / 2) - 20, fonts['default'], colors['white'])
        draw_text(f"HP: {samurai.hp}/{samurai.max_hp}" , 280, (screen_height + bottom_panel_height / 2) - 20, fonts['default'], colors['white'])
        
        # Enemies stats
        for count, enemy in enumerate(enemies):
            draw_text(f"{enemy.name}" , screen_width - 280, ((screen_height + bottom_panel_height / 2) - 50) + (count * 60), fonts['default'], colors['white'])
            draw_text(f"HP: {enemy.hp}/{enemy.max_hp}" , screen_width - 110, ((screen_height + bottom_panel_height / 2) - 50) + (count * 60), fonts['default'], colors['white'])
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        
        # Draw background
        draw_bg(background_surf)
        
        # Draw panel
        draw_panel()
        
        # Draw characters healt bar
        samurai_health_bar.draw(samurai.hp)
        gotoku_health_bar.draw(gotoku.hp)
        yorei_health_bar.draw(yorei.hp)
        
        # Draw samurai
        samurai.draw()
        samurai.update()
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw()
            enemy.update()
        
        # Cursor as sword
        mouse_pos = pygame.mouse.get_pos()
        for enemy in enemies:
            if current_character == 1:
                if enemy.alive and enemy.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_visible(False)
                    screen.blit(sword_surf, mouse_pos)
                else:
                    pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(True)
        
        if current_character > total_characters:
            current_character = 1
            total_characters = 1 + sum(1 for enemy in enemies if enemy.alive)
        
        # Character state
        attack = False
        charm = False
        target = None
        for count, enemy in enumerate(enemies):
            if enemy.rect.collidepoint(mouse_pos):
                if clicked:
                    attack = True
                    target = enemies[count]
        
        # # Samurai action
        if samurai.alive:
            if current_character == 1:
                action_delay = 50
                action_cooldown += 1
                if action_cooldown >= action_delay:
                    if attack and target != None:
                        samurai.attack(target)
                        current_character += 1
                        action_cooldown = 0
        
        # Enemies action
        action_delay = 100
        for count, enemy in enumerate(enemies):
            if current_character == 2 + count:
                if enemy.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_delay:
                        enemy.attack(samurai)
                        current_character += 1
                        action_cooldown = 0
                else:
                    current_character += 1
        
        pygame.display.update()
        clock.tick(fps)
        
def main_menu():
    screen.fill(colors['black'])
    
    pygame.display.set_caption("Tale of Samurai: Main Menu")
    
    running = True
    fps = 60
    
    background_surf = pygame.transform.scale(pygame.image.load("assets/mountain_bg.png").convert_alpha(), (screen_width, screen_height + bottom_panel_height))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
        
        draw_bg(background_surf)
        
        pygame.display.update()
        clock.tick(fps)
        
main_menu()