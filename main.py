import pygame
from sys import exit
from random import randint
import button

pygame.init()

bottom_panel_height = 150
screen_width = 800
screen_height = 400

img_scale_ratio = 1.5

screen = pygame.display.set_mode((screen_width, screen_height + bottom_panel_height))
clock = pygame.time.Clock()

font_style = "Pixeltype"
fonts = {
    "default": pygame.font.Font(f"font/{font_style}.ttf", 24),
    "sm": pygame.font.Font(f"font/{font_style}.ttf", 20),
    "md": pygame.font.Font(f"font/{font_style}.ttf", 32),
    "lg": pygame.font.Font(f"font/{font_style}.ttf", 40),
}

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
        self.is_attacking = False
        self.attack_target = None
        self.waiting_to_hurt = False
        self.attack_start_time = 0
        self.hurt_delay = 450
        
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
        elif self.animation_action == 1:
            animation_delay = 150
            
        self.image = self.animation_list[int(self.animation_action)][int(self.animation_index)]
        
        if pygame.time.get_ticks() - self.current_time >= animation_delay:
            self.current_time = pygame.time.get_ticks()
            self.animation_index += 1
            if self.is_attacking and self.animation_index >= len(self.animation_list[1]):
                self.is_attacking = False
                self.attack_target = None
                self.idle()
                return
                
            if self.animation_index >= len(self.animation_list[self.animation_action]):
                if self.animation_action == 2:
                    self.waiting_to_hurt = False
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
        self.is_attacking = True
        self.attack_target = target
        self.attack_start_time = pygame.time.get_ticks()
        self.animation_action = 1
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
        
        rand_dmg = randint(-5, 5)
        self.pending_damage = self.strength + rand_dmg
        
        target.waiting_to_hurt = True
    
    def take_damage(self, damage):
        self.hp -= damage
        self.animation_action = 2
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
        
        if self.hp <= 0:
            self.hp = 0
            self.die()
    
    def update(self):
        self.animation()
        
        if self.attack_target and self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start_time >= self.hurt_delay:
                if self.attack_target.waiting_to_hurt:
                    self.attack_target.take_damage(self.pending_damage)
                    self.attack_target.waiting_to_hurt = False

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
    game_active = True
    
    background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
    panel_surf = pygame.image.load("assets/panel.png").convert_alpha()
    sword_surf = pygame.image.load("assets/sword.png").convert_alpha()
    
    samurai = Character(100, 270, 'Samurai', 100, 60, 3)
    samurai_health_bar = HealthBar(80, screen_height + bottom_panel_height / 2, samurai.hp, samurai.max_hp)

    gotoku = Character(screen_width - 100, 270, 'Gotoku', 120, 25, 2)
    gotoku_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) - 30, gotoku.hp, gotoku.max_hp)
    yorei = Character(screen_width - 200, 180, 'Yorei', 80, 30, 1)
    yorei_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) + 30, yorei.hp, yorei.max_hp)
    enemies = []
    enemies.append(gotoku)
    enemies.append(yorei)

    def draw_panel():
        screen.blit(panel_surf, (0, screen_height))
        
        draw_text(f"{samurai.name}" , 110, (screen_height + bottom_panel_height / 2) - 20, fonts['default'], colors['white'])
        draw_text(f"HP: {samurai.hp}/{samurai.max_hp}" , 280, (screen_height + bottom_panel_height / 2) - 20, fonts['default'], colors['white'])
        
        for count, enemy in enumerate(enemies):
            draw_text(f"{enemy.name}" , screen_width - 280, ((screen_height + bottom_panel_height / 2) - 50) + (count * 60), fonts['default'], colors['white'])
            draw_text(f"HP: {enemy.hp}/{enemy.max_hp}" , screen_width - 110, ((screen_height + bottom_panel_height / 2) - 50) + (count * 60), fonts['default'], colors['white'])
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if game_active and event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        
        if game_active:
            draw_bg(background_surf)
            
            draw_panel()
            
            samurai_health_bar.draw(samurai.hp)
            gotoku_health_bar.draw(gotoku.hp)
            yorei_health_bar.draw(yorei.hp)
            
            samurai.draw()
            samurai.update()
            
            for enemy in enemies:
                enemy.draw()
                enemy.update()
            
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
            
            attack = False
            charm = False
            target = None
            for count, enemy in enumerate(enemies):
                if enemy.rect.collidepoint(mouse_pos):
                    if clicked:
                        attack = True
                        target = enemies[count]
            
            if samurai.alive:
                if current_character == 1:
                    action_delay = 50
                    action_cooldown += 1
                    if action_cooldown >= action_delay:
                        if attack and target != None:
                            samurai.attack(target)
                            current_character += 1
                            action_cooldown = 0
            
            if not samurai.alive:
                game_active = False
            
            count_enemies_alive = sum(1 for enemy in enemies if enemy.alive)
            if count_enemies_alive == 0:
                running = False
                game_active = False
            
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
        else:
            restart()
        
        pygame.display.update()
        clock.tick(fps)

def restart():
    screen.fill((94, 129, 162))
    
    pygame.display.set_caption("Tale of Samurai: Restart Menu")
    
    running = True
    fps = 60
    
    retry_btn_img = pygame.image.load("assets/Buttons/btn_retry.png").convert_alpha()
    menu_btn_img = pygame.image.load("assets/Buttons/btn_menu.png").convert_alpha()
    
    retry_btn = button.Button(screen_width / 2, 200, retry_btn_img, 1.2)
    menu_btn = button.Button(100, 300, menu_btn_img, 1.2)
    
    draw_text("GAME OVER", screen_width / 2, 100, fonts['lg'], colors['white'])
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        # draw buttons
        if retry_btn.draw(screen):
            play()
        if menu_btn.draw(screen):
            main_menu()
        
        pygame.display.update()
        clock.tick(fps)
 
def main_menu():
    screen.fill(colors['black'])
    
    pygame.display.set_caption("Tale of Samurai: Main Menu")
    
    running = True
    fps = 60
    
    background_surf = pygame.transform.scale(pygame.image.load("assets/mountain_bg.png").convert_alpha(), (screen_width, screen_height + bottom_panel_height))
    
    play_btn_img = pygame.image.load("assets/Buttons/btn_play.png").convert_alpha()
    exit_btn_img = pygame.image.load("assets/Buttons/btn_exit.png").convert_alpha()
    
    play_btn = button.Button(screen_width / 2, 200, play_btn_img, 1.2)
    exit_btn = button.Button(100, 300, exit_btn_img, 1.2)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
                
        draw_bg(background_surf)

        if play_btn.draw(screen):
            play()
        if exit_btn.draw(screen):
            running = False
            pygame.quit()
            exit()
        
        pygame.display.update()
        clock.tick(fps)
        
main_menu()