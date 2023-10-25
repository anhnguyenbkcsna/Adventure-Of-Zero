import pygame
import os

class AnimInfo():
   def __init__(self, startFrame, numFrames):
       self.startFrame = startFrame
       self.numFrames = numFrames 
                 
class Cannon(pygame.sprite.Sprite):   
    
    SHOOTING_FRAME_RATE = 120
    CANNON_BALL_FLY_RANGE = 400
    FRAME_RATE_CHANGE_ANIM = 10
    WIDTH = 80
    HEIGHT = 52
    FOOT_SPACE = 0 # Space between foot and ground according to image size 
    STAND_STATE = 0
    SHOOTING_STATE = 1  
    DEAD_STATE = 2
    
    def __init__(self, x, y, isFacingRight):
        super().__init__()
        
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Idle/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/4.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/5.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Fire/6.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Cannon', 'Cannon Destroyed/4.png')))          
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(self.WIDTH, self.HEIGHT))
            if isFacingRight: 
                self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        
        self.animInfo = [AnimInfo(0, 1), AnimInfo(1, 6), AnimInfo(7, 4)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

        self.frameCountShooting = 0
        self.isFacingRight = isFacingRight
        self.state = self.SHOOTING_STATE

    def update(self, keys):
        self.update_input(keys)
        
        # Auto shoot every SHOOTING_FRAME_RATE
        if self.state != self.DEAD_STATE:
            if self.frameCountShooting == 0:
                self.shoot()
            self.frameCountShooting += 1
            if self.frameCountShooting == self.SHOOTING_FRAME_RATE:
                self.frameCountShooting = 0
        
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//10]
            if not self.isFacingRight:
                self.image = pygame.transform.flip(self.image, True, False)
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*10:
            if self.state == self.DEAD_STATE: 
                self.kill()
            if self.state == self.SHOOTING_STATE:
                self.stand() 
            else:
                self.frameCount = 0
    
    def update_input(self, input_keys):
        if input_keys[pygame.K_k]:
            self.dead()
    
    def dead(self):
        self.state = self.DEAD_STATE
        self.frameCount = 0
        
    def stand(self):
        self.state = self.STAND_STATE
        self.frameCount = 0
        
    def shoot(self):
        self.state = self.SHOOTING_STATE
        self.frameCount = 0
        
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag

