import pygame
import random
import os
from item import Apple, Banana

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLOCK_SIZE = 32

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.name = name
        self.width = width
        self.height = height
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BreakableObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.dropped_item = False
        
        self.box_sprite = [
            pygame.image.load(os.path.join('Assets/Objects', 'Idle.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Broken.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'blank_box.png')),
        ]
        
        self.is_broken = False
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
                self.image = self.box_sprite[2]
            else:
                self.image = self.box_sprite[1]
        else:
            self.image = self.box_sprite[0]
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        
    
    def drop_item(self):
        if self.is_broken:
            item_prob = random.uniform(0, 1)
            if item_prob <= 0.6667:
                return Apple(self.rect.x, self.rect.y, BLOCK_SIZE, BLOCK_SIZE)
            else:
                return Banana(self.rect.x, self.rect.y, BLOCK_SIZE, BLOCK_SIZE)
        return None
            

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.image.fill((0, 100, 50))
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)