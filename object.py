import pygame
import random
import os
from item import Apple

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLOCK_SIZE = 32

BLOCK_SIZE = 32
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.name = name
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.color = (0, 100, 100)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Camera
    def update_camera(self, player_velocity_x, move_camera): 
        if move_camera:
            self.rect.x -= player_velocity_x
        
    def get_tag(self):
        return self.name
    
    def change_color(self, color):
        self.color = color
        self.image.fill(self.color)

class Block(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(self.color)
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)
        

class BreakableObject(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        
        self.box_sprite = [
            pygame.image.load(os.path.join('Assets/Objects', 'Idle.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Broken.png')),
        ]
        
        self.is_broken = False
        self.box_state = "idle"
        self.image = self.box_sprite[0]
        self.image = pygame.transform.scale(self.image, (width, height))
        
        self.animation_timer = 0
        self.animation_duration = 30

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def break_object(self):
        self.is_broken = True
            
    def update(self):
        if self.is_broken:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_duration:
                self.animation_timer = 0
                self.box_state = "disappear"

            if self.box_state == "disappear":
                self.kill()
            else:
                self.image = self.box_sprite[1]
        else:
            self.image = self.box_sprite[0]
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        
    
    def drop_item(self):
        if self.is_broken:
            item = Apple(self.rect.x, self.rect.y, BLOCK_SIZE, BLOCK_SIZE)
            return item
        return None
            
        # pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
    