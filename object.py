import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.name = name
        self.width = width
        self.height = height
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
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.image.fill(self.color)
        self.name = 'block'
        self.mask = pygame.mask.from_surface(self.image)
    