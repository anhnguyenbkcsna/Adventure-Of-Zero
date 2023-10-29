import pygame
import random
import os

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
        self.image = pygame.image.load(os.path.join('Assets/Objects', 'Idle.png'))
        
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
    
        self.broken_pieces = [
            pygame.image.load(os.path.join('Assets/Objects', 'Box Pieces 1.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Box Pieces 2.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Box Pieces 3.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Box Pieces 4.png'))
        ]
        
        self.is_broken = False
        self.broken_animation_timer = 20
        self.broken_animation_duration = 800

    def draw(self, screen):
        if not self.is_broken:
            screen.blit(self.image, self.rect)

    def break_object(self):
        self.is_broken = True
            
    def update(self):
        if self.is_broken:
            if self.broken_animation_timer < self.broken_animation_duration:
                self.image = self.broken_pieces[self.broken_animation_timer // (self.broken_animation_duration // 4)]
                self.broken_animation_timer += 1
            else:
                self.kill()

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.image.fill((0, 100, 50))
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)