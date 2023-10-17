import pygame
import os

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPEED = 5
    FPS = 60
    FRICTION_FORCE = 0.2
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets\Player', 'Jump.png'))
        
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.math.Vector2(0, 0)
        self.fall_count = 0 # virtual gravity

        
        self.mask = None
        self.isJump = True
        
        # self.tag = tag
        # self.hp = 
        # self.attack_cd = 0
        # self.attack_time = 0
        # self.dash_cd = 0
        # self.pull_cd = 0
        # self.push_cd = 0
    def update(self, keys, objects):
        self.updateInput(keys)
        self.updateGravity()
        self.move()
        self.mask = pygame.mask.from_surface(self.image)
        self.vertical_collision(objects, self.velocity.y)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def updateInput(self, input_keys):
        # horizontal move
        if input_keys[pygame.K_a] or input_keys[pygame.K_LEFT]:
            self.velocity.x = -self.SPEED
        elif input_keys[pygame.K_d] or input_keys[pygame.K_RIGHT]:
            self.velocity.x = self.SPEED
        else:
            if self.velocity.x > 0.1:
                self.velocity.x -= self.FRICTION_FORCE
            elif self.velocity.x < -0.1:
                self.velocity.x += self.FRICTION_FORCE
            else:
                self.velocity.x = 0
            
        # jump
        if input_keys[pygame.K_SPACE] and self.isJump == False and self.fall_count == 0: # make sure player is on the ground
            self.velocity.y = -5
            self.isJump = True
        # attack
        elif input_keys[pygame.K_j] or input_keys[pygame.MOUSEBUTTONDOWN]:
            pass
        # dash
        elif input_keys[pygame.K_k] or input_keys[pygame.K_LSHIFT] or input_keys[pygame.K_LCTRL]:
            self.velocity.x *= 3
        # pull_skill
        elif input_keys[pygame.K_e]:
            pass
    
    ############## Physics & Collision ##############
    def updateGravity(self):
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
    
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag
    
# Ref https://github.com/techwithtim/Python-Platformer/