import pygame

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
        # pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
    
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