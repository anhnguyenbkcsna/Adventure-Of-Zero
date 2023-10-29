from typing import Any
import pygame
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = None
        self.rect = None
        self.score_value = 0
        
        
class Apple(Item):
    def __init__(self, item_type, x, y):
        super().__init__(item_type, x, y)
        
        self.item_sprites = []
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_0')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_1')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_2')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_3')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_4')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_5')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_6')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_7')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_8')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_9')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_10')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_11')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_12')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_13')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_14')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_15')))
        
        self.current_sprite = 0
        self.image = self.item_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
    
    def update(self):
        self.current_sprite += 1
        
        if self.current_sprite >= len(self.item_sprites):
            self.current_sprite = 0
            
        self.image = self.item_sprites[self.current_sprite]
        