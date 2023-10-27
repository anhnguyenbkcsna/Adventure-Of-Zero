import pygame
import os

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPEED = 5
    FPS = 60
    FRICTION_FORCE = 1
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets\Player', 'Jump.png'))
        
        self.rect = pygame.Rect(x, y, width, height)
        self.tag = "Player"
        self.velocity = pygame.math.Vector2(0, 0)
        self.fall_count = 0 # virtual gravity

        self.isFacingRight = True
        self.isJump = True
        self.mask = None
        
        
        # Cooldown & Timer
        self.dash_cd_timer = 0
        self.dash_cd = 1
        
        self.attack_cd_timer = 0
        self.attack_cd = 0.2
        
        # self.dash_cd = 0
        # self.pull_cd = 0
        # self.push_cd = 0
        self.attack = Attack()
    def update(self, keys, objects):
        self.update_input(keys)
        self.update_gravity()
        self.move()
        self.mask = pygame.mask.from_surface(self.image)
        self.vertical_collision(objects, self.velocity.y)
        
        self.update_cd_timer()
        
        self.attack.collision(objects)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.attack_cd_timer > 0:
            pos = self.rect
            if self.isFacingRight:
                pos = (self.rect.x + 3 * self.rect.width / 2, self.rect.y + self.rect.height / 2)
            else:
                pos = (self.rect.x - self.rect.width / 2, self.rect.y + self.rect.height / 2)
            # draw attack range
            self.attack.draw(screen, pos)
            # pygame.draw.circle(screen, (255, 100, 0), pos, int(self.ATTACK_RANGE / 2))
        
    def move(self):
        # self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
    
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.isFacingRight = not self.isFacingRight

    def update_input(self, input_keys):
        # horizontal move
        if input_keys[pygame.K_a] or input_keys[pygame.K_LEFT]:
            if self.isFacingRight:
                self.flip()
            if self.velocity.x < -self.SPEED:
                self.velocity.x += self.FRICTION_FORCE
            else:
                self.velocity.x = -self.SPEED
        elif input_keys[pygame.K_d] or input_keys[pygame.K_RIGHT]:
            if not self.isFacingRight:
                self.flip()
            if self.velocity.x > self.SPEED:
                self.velocity.x -= self.FRICTION_FORCE
            else:
                self.velocity.x = self.SPEED
        else:
            if self.velocity.x > 0.1 or self.velocity.x > self.SPEED:
                self.velocity.x -= self.FRICTION_FORCE
            elif self.velocity.x < -0.1 or self.velocity.x < -self.SPEED:
                self.velocity.x += self.FRICTION_FORCE
            else:
                self.velocity.x = 0
            
        # jump
        if input_keys[pygame.K_SPACE] and self.isJump == False and self.fall_count == 0: # make sure player is on the ground
            self.velocity.y = -5
            self.isJump = True
        # attack
        elif input_keys[pygame.K_j] and self.attack_cd_timer <= 0:
            self.attack_cd_timer = self.attack_cd
        # dash
        elif input_keys[pygame.K_k] or input_keys[pygame.K_LSHIFT] or input_keys[pygame.K_LCTRL]:
            if self.dash_cd_timer <= 0:
                self.velocity.x *= 5
                self.dash_cd_timer = self.dash_cd
        # pull_skill
        elif input_keys[pygame.K_e]:
            self.attack()
    
    def update_cd_timer(self):
        self.dash_cd_timer -= 1 / self.FPS
        self.attack_cd_timer -= 1/self.FPS
    
    ############## Physics & Collision ##############
    def update_gravity(self):
        if self.isJump == True:            
            self.velocity.y += min(1, (self.fall_count / self.FPS) * self.GRAVITY)
            self.fall_count += 1
    
    def landed(self):
        self.fall_count = 0
        self.velocity.y = 0
        self.isJump = False

    def hit_head(self):
        self.fall_count = 0
        self.velocity.y = -1
        
    def vertical_collision(self, objects, dy):
        collide_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if dy > 0:
                    # land on the object
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif dy < 0:
                    # Head hit the object
                    self.rect.top = obj.rect.bottom
                    self.hit_head()
                    
                collide_objects.append(obj)
        return collide_objects
    
    def attack(self):
        pass
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag
    
    def get_pos(self):
        return self.rect
# Ref https://github.com/techwithtim/Python-Platformer/

class Attack(pygame.sprite.Sprite):
    ATTACK_RANGE = 32
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets\Player', 'Jump.png'))
        self.rect = pygame.Rect(0, 0, self.ATTACK_RANGE, self.ATTACK_RANGE)
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, objects):
        collide_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                print("Collision detect: Attack + " +obj.get_tag())
                collide_objects.append(obj)
    
    def draw(self, screen, pos):
        self.rect = pygame.Rect(pos[0] - self.ATTACK_RANGE / 2, pos[1] - self.ATTACK_RANGE / 2, self.ATTACK_RANGE, self.ATTACK_RANGE)
        pygame.draw.rect(screen, (150, 150, 40), self.rect)    