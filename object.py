import pygame
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

BLOCK_SIZE = 40
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
        self.image = pygame.image.load(os.path.join('Assets/Terrain', '1.png'))
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)
        
class GrassBlock(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join('Assets/Terrain', '0.png'))
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.name = "Obstacle"
        self.image = pygame.image.load(os.path.join('Assets/Terrain', '17.png'))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
            
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)

class BreakableObject(Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.dropped_item = False
        self.name = "Breakable Object"
        
        self.box_sprite = [
            pygame.image.load(os.path.join('Assets/Objects', 'Idle.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'Broken.png')),
            pygame.image.load(os.path.join('Assets/Objects', 'blank_box.png')),
        ]
        
        for i in range(len(self.box_sprite)):
            self.box_sprite[i] = pygame.transform.scale(self.box_sprite[i], (BLOCK_SIZE, BLOCK_SIZE))
        self.image = self.box_sprite[0]
        
        self.is_broken = False
        self.animation_timer = 0
        self.animation_duration = 30
        self.itemGroup = pygame.sprite.Group()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def break_object(self):
        self.is_broken = True
            
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)
        
        # Animation
        if self.is_broken:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_duration:
                self.image = self.box_sprite[2]
            else:
                self.image = self.box_sprite[1]
        else:
            self.image = self.box_sprite[0]
        
        # Drop item
        if self.is_broken == True:
            drop_prob = random.uniform(0, 1)
            if drop_prob >= 0.5 and self.dropped_item == False:
                self.itemGroup.add(self.drop_item())
                
            self.dropped_item = True
            # Play particle effect
    
    def drop_item(self):
        if self.is_broken:
            item_prob = random.uniform(0, 1)
            if item_prob <= 0.6667:
                print("Spawn apple")
                return Apple(self.rect.x, self.rect.y)
            else:
                print("Spawn banana")
                return Banana(self.rect.x, self.rect.y)
        return None
            
class Item(Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = None
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.score_value = -1
        self.is_collected = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.collision_with_player(player)
        self.animation_timer += 1
        
        if self.animation_timer >= self.animation_duration:
            self.current_sprite += 1
            if self.current_sprite >= len(self.item_sprites):
                self.current_sprite = 0
            self.animation_timer = 0
            self.image = self.item_sprites[self.current_sprite]
    
    def collision_with_player(self, player):
        if pygame.sprite.collide_mask(self, player):
            item_sound = pygame.mixer.Sound(os.path.join('Assets\Sound', 'item.mp3'))
            pygame.mixer.Sound.play(item_sound)
            self.is_collected = True
            player.score += self.score_value
            self.kill()
            
class Apple(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score_value = 5
        self.name = "Apple"
        
        self.item_sprites = []
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_0.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_1.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_2.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_3.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_4.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_5.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_6.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_7.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_8.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_9.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_10.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_11.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_12.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_13.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_14.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'apple_15.png')))
        
        for i in range(len(self.item_sprites)):
            self.item_sprites[i] = pygame.transform.scale(self.item_sprites[i], (BLOCK_SIZE, BLOCK_SIZE))
        
        self.current_sprite = 0
        self.image = self.item_sprites[self.current_sprite]
        
        self.animation_timer = 0
        self.animation_duration = 3

class Banana(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score_value = 10
        self.name = "Banana"
        
        self.item_sprites = []
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_0.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_1.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_2.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_3.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_4.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_5.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_6.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_7.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_8.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_9.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_10.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_11.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_12.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_13.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_14.png')))
        self.item_sprites.append(pygame.image.load(os.path.join('Assets/Objects', 'banana_15.png')))
        
        
        for i in range(len(self.item_sprites)):
            self.item_sprites[i] = pygame.transform.scale(self.item_sprites[i], (BLOCK_SIZE, BLOCK_SIZE))
                    
        self.current_sprite = 0
        self.image = self.item_sprites[self.current_sprite]
        
        self.animation_timer = 0
        self.animation_duration = 3

class Star(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score_value = 0
        self.name = "Star"
        
        self.image = pygame.image.load(os.path.join('Assets/Objects', 'star.png'))
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.animation_timer = 0
        self.animation_duration = 0
        self.current_sprite = 0
        self.item_sprites = []
        self.item_sprites.append(self.image)
        
    def collision_with_player(self, player):
        if pygame.sprite.collide_mask(self, player):
            item_sound = pygame.mixer.Sound(os.path.join('Assets\Sound', 'item.mp3'))
            pygame.mixer.Sound.play(item_sound)
            self.is_collected = True
            player.stars += 1
            print("Star collected")
            self.kill()

class Flag(Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score_value = 0
        self.name = "Flag"
        
        self.image = pygame.image.load(os.path.join('Assets/Terrain', '13.png'))
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE * 2, BLOCK_SIZE * 2))
        self.animation_timer = 0
        self.animation_duration = 0
        self.current_sprite = 0
        self.item_sprites = []
        self.item_sprites.append(self.image)
        
    def update(self, player):
        self.update_camera(player.velocity.x, player.move_camera)
        self.mask = pygame.mask.from_surface(self.image)