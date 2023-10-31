# from typing import Any
# import pygame
# import os
# from object import Object

# class Item(Object, pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height):
#         super().__init__(x, y)
#         self.image = None
#         self.width = width
#         self.height = height
#         self.rect = pygame.Rect(x, y, width, height)
#         self.score_value = 0
#         self.is_collected = False
        
#     def draw(self, screen):
#         screen.blit(self.image, self.rect)
        
#     def update(self):
#         self.animation_timer += 1
        
#         if self.animation_timer >= self.animation_duration:
#             self.current_sprite += 1
#             if self.current_sprite >= len(self.item_sprites):
#                 self.current_sprite = 0
#             self.animation_timer = 0
#             self.image = self.item_sprites[self.current_sprite]
        
        
# class Apple(Item):
#     def __init__(self, x, y, width, height):
#         super().__init__(x, y, width, height)
#         self.rect = pygame.Rect(x, y, width, height)
#         self.score = 10
#         self.name = "Apple"
        
#         self.item_sprites = []
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_0.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_1.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_2.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_3.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_4.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_5.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_6.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_7.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_8.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_9.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_10.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_11.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_12.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_13.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_14.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_15.png')))
        
#         for i in range(len(self.item_sprites)):
#             self.item_sprites[i] = pygame.transform.scale(self.item_sprites[i], (width, height))
        
#         self.current_sprite = 0
#         self.image = self.item_sprites[self.current_sprite]
        
#         self.animation_timer = 0
#         self.animation_duration = 3

# class Banana(Item):
#     def __init__(self, x, y, width, height):
#         super().__init__(x, y, width, height)
#         self.rect = pygame.Rect(x, y, width, height)
#         self.score = 15
        
#         self.item_sprites = []
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_0.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_1.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_2.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_3.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_4.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_5.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_6.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_7.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_8.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_9.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_10.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_11.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_12.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_13.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_14.png')))
#         self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_15.png')))
        
        
#         for i in range(len(self.item_sprites)):
#             self.item_sprites[i] = pygame.transform.scale(self.item_sprites[i], (width, height))
                    
#         self.current_sprite = 0
#         self.image = self.item_sprites[self.current_sprite]
        
#         self.animation_timer = 0
#         self.animation_duration = 3
        
    
        