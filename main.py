import pygame
from sys import exit
from random import randint
import button

pygame.init()

bottom_panel_height = 150
screen_width = 800
screen_height = 400

img_scale_ratio = 1.5
game_state = ""

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
    def __init__(self, x, y, name, max_hp, strength, charms):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.charms = charms
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
        self.temp_double_dmg_effect = 1
        self.hit_sound = pygame.mixer.Sound(f"assets/Sounds/{self.name}_hit.mp3")
        self.death_sound = pygame.mixer.Sound(f"assets/Sounds/death.mp3")
        
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
        self.death_sound.play()
        self.animation_action = 3
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
    
    def attack(self, target):
        self.is_attacking = True
        self.hit_sound.play()
        self.attack_target = target
        self.attack_start_time = pygame.time.get_ticks()
        self.animation_action = 1
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
        
        rand_dmg = randint(-5, 5)
        if self.temp_double_dmg_effect > 1:
            self.pending_damage = (self.strength * self.temp_double_dmg_effect) + rand_dmg
        else:
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

class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.animation_list = []
        self.animation_index = 0
        self.current_time = pygame.time.get_ticks()
        self.scale_ratio = 1.5
        
        for i in range(1, 10):
            if self.name == "Claw" or self.name == "Blood":
                self.scale_ratio = 2.5
            else:
                self.scale_ratio = 0.8
            img = pygame.image.load(f"assets/Effects/{self.name}/0{i}.png").convert_alpha()
            img = pygame.transform.rotozoom(img, 0, self.scale_ratio)
            self.animation_list.append(img)
        
        self.image = self.animation_list[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def animation(self):
        animation_delay = 100
        
        self.image = self.animation_list[int(self.animation_index)]
        
        if pygame.time.get_ticks() - self.current_time >= animation_delay:
            self.current_time = pygame.time.get_ticks()
            self.animation_index += 1
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        self.animation()

class FloatingText:
    def __init__(self, text, x, y, duration, font, color):
        self.text = text
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.font = font
        self.color = color

    def update(self):
        self.y -= 0.5

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration

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
    global game_state
    active_effects = []
    floating_texts = []
    
    charms = {
        "refill_health": {
            "amount": 2,
            "active": False,
            "effect": 100
        },
        "double_damage": {
            "amount": 2,
            "active": False,
            "effect": 2
        },
    }
    
    background_surf = pygame.transform.scale(pygame.image.load("assets/background.png").convert_alpha(), (screen_width, screen_height))
    panel_surf = pygame.image.load("assets/panel.png").convert_alpha()
    sword_surf = pygame.image.load("assets/sword.png").convert_alpha()
    health_charm_img = pygame.image.load("assets/Buttons/Charms/flask.png").convert_alpha()
    doubledmg_charm_img = pygame.image.load("assets/Buttons/Charms/double_sword.png").convert_alpha()
    low_health_screen = pygame.image.load("assets/low_health_screen.png").convert_alpha()
    low_health_screen = pygame.transform.scale(low_health_screen, (screen_width, screen_height))
    
    samurai = Character(100, 270, 'Samurai', 200, 40, charms)
    samurai_health_bar = HealthBar(80, (screen_height + bottom_panel_height / 2) - 30, samurai.hp, samurai.max_hp)

    gotoku = Character(screen_width - 100, 270, 'Gotoku', 120, 25, None)
    gotoku_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) - 30, gotoku.hp, gotoku.max_hp)
    yorei = Character(screen_width - 200, 180, 'Yorei', 80, 30, None)
    yorei_health_bar = HealthBar(screen_width - 310, (screen_height + bottom_panel_height / 2) + 30, yorei.hp, yorei.max_hp)
    enemies = []
    enemies.append(gotoku)
    enemies.append(yorei)
    
    heal_up_sound = pygame.mixer.Sound(f"assets/Sounds/heal_up.mp3")
    double_damage_sound = pygame.mixer.Sound(f"assets/Sounds/power_up.mp3")
    
    def draw_panel():
        screen.blit(panel_surf, (0, screen_height))
        
        draw_text(f"{samurai.name}" , 110, (screen_height + bottom_panel_height / 2) - 50, fonts['default'], colors['white'])
        draw_text(f"HP: {samurai.hp}/{samurai.max_hp}" , 280, (screen_height + bottom_panel_height / 2) - 50, fonts['default'], colors['white'])
        
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
        target = None
        for count, enemy in enumerate(enemies):
            if enemy.rect.collidepoint(mouse_pos):
                if clicked:
                    attack = True
                    target = enemies[count]
        
        heath_charm_btn = button.Button(100, (screen_height + bottom_panel_height / 2) + 30, health_charm_img, 0.09)
        doubledmg_charm_btn = button.Button(100 + 50, (screen_height + bottom_panel_height / 2) + 30, doubledmg_charm_img, 0.09)
        
        heal_confirm = False
        double_damage_confirm = False
        if heath_charm_btn.draw(screen):
            samurai.charms["refill_health"]["active"] = True
            heal_confirm = True
        elif doubledmg_charm_btn.draw(screen):
            double_damage_confirm = True
            samurai.charms["double_damage"]["active"] = True
        
        draw_text(str(samurai.charms["refill_health"]["amount"]), 110, (screen_height + bottom_panel_height / 2) + 40, fonts['sm'], colors['white'])
        draw_text(str(samurai.charms["double_damage"]["amount"]), 160, (screen_height + bottom_panel_height / 2) + 40, fonts['sm'], colors['white'])
        
        if samurai.alive:
            if current_character == 1:
                action_delay = 50
                action_cooldown += 1
                if action_cooldown >= action_delay:
                    if attack and target is not None:
                        samurai.attack(target)
                        active_effects.append(Effect(target.rect.centerx, target.rect.centery, "Slash"))
                        if samurai.temp_double_dmg_effect > 1:
                            samurai.temp_double_dmg_effect = 1
                        current_character += 1
                        action_cooldown = 0
                
                    # healing charm
                    if samurai.charms["refill_health"]["active"]:
                        if samurai.charms["refill_health"]["amount"] > 0 and heal_confirm:
                            if samurai.max_hp - samurai.hp > samurai.charms["refill_health"]["effect"]:
                                heal_amount = samurai.charms["refill_health"]["effect"]
                            else:
                                heal_amount = samurai.max_hp - samurai.hp
                            samurai.hp += heal_amount
                            heal_up_sound.play()
                            floating_texts.append(FloatingText(
                                f"+{heal_amount} HP", 
                                samurai.rect.centerx,
                                samurai.rect.top - 20, 
                                3000, 
                                fonts['sm'], 
                                colors['white']
                            ))
                            samurai.charms["refill_health"]["amount"] -= 1
                            current_character += 1
                            action_cooldown = 0
                            samurai.charms["refill_health"]["active"] = False
                            heal_confirm = False
                            
                    # double damage charm
                    if samurai.charms["double_damage"]["active"]:
                        if samurai.charms["double_damage"]["amount"] > 0 and double_damage_confirm:
                            samurai.temp_double_dmg_effect = samurai.charms["double_damage"]["effect"]
                            double_damage_sound.play()
                            floating_texts.append(FloatingText(
                                f"x{samurai.charms['double_damage']['effect']} Damage",
                                samurai.rect.centerx,
                                samurai.rect.top - 20, 
                                3000, 
                                fonts['sm'], 
                                colors['white']
                            ))
                            samurai.charms["double_damage"]["amount"] -= 1
                            current_character += 1
                            action_cooldown = 0
                            samurai.charms["double_damage"]["active"] = False
                            double_damage_confirm = False
        
        for text in floating_texts:
            text.update()
            text.draw(screen)
        
        floating_texts = [text for text in floating_texts if not text.is_expired()]
        
        if not samurai.alive:
            game_state = "GAME OVER"
            restart(game_state)
        
        if all(not enemy.alive for enemy in enemies):
            game_state = "VICTORY"
            restart(game_state)
        
        action_delay = 100
        for count, enemy in enumerate(enemies):
            if current_character == 2 + count:
                if enemy.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_delay:
                        enemy.attack(samurai)
                        if enemy.name == "Yorei":
                            active_effects.append(Effect(samurai.rect.centerx, samurai.rect.centery, "Blood"))
                        elif enemy.name == "Gotoku":
                            active_effects.append(Effect(samurai.rect.centerx, samurai.rect.centery, "Claw"))
                        current_character += 1
                        action_cooldown = 0
                else:
                    current_character += 1
        
        for effect in active_effects:
            effect.update()
            effect.draw()
        
        active_effects = [effect for effect in active_effects if effect.animation_index < len(effect.animation_list)]
        
        if samurai.hp <= samurai.max_hp * 1 / 4:
            draw_bg(low_health_screen)
        
        pygame.display.update()
        clock.tick(fps)

def restart(game_state):
    screen.fill((94, 129, 162))
    
    pygame.display.set_caption("Tale of Samurai: Restart Menu")
    
    running = True
    fps = 60
    
    retry_btn_img = pygame.image.load("assets/Buttons/btn_retry.png").convert_alpha()
    menu_btn_img = pygame.image.load("assets/Buttons/btn_menu.png").convert_alpha()
    
    retry_btn = button.Button(screen_width / 2, 200, retry_btn_img, 1.2)
    menu_btn = button.Button(screen_width / 2, 280, menu_btn_img, 1.2)
    
    draw_text(f"{game_state}", screen_width / 2, 100, fonts['lg'], colors['white'])
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

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