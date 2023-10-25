import pygame
import os

class AnimInfo():
   def __init__(self, startFrame, numFrames):
       self.startFrame = startFrame
       self.numFrames = numFrames 

class RayCast2D():
    def __init__(self, enemy_x, enemy_y, flipPoint1, flipPoint2, enemyIsFacingRight):
        self.flipPoint1 = flipPoint1
        self.flipPoint2 = flipPoint2
        self.isFacingRight = enemyIsFacingRight
        self.x = enemy_x + Enemy.WIDTH if enemyIsFacingRight else enemy_x
        self.y = enemy_y
        self.length = min(Enemy.ATTACK_RANGE, self.flipPoint2 - self.x + 1 if self.isFacingRight else self.x - self.flipPoint1 + 1)
    
    def flip(self):
        self.x -= Enemy.WIDTH if self.isFacingRight else -Enemy.WIDTH 
        self.isFacingRight = not self.isFacingRight
        
    def change_x(self, newX):
        self.x = newX
        self.length = min(Enemy.ATTACK_RANGE, self.flipPoint2 - self.x + 1 if self.isFacingRight else self.x - self.flipPoint1 + 1)
        
    def collide_player(self, player):
        playerX = player.rect.x
        playerY = player.rect.y
        if playerY + player.HEIGHT != self.y + Enemy.HEIGHT - Enemy.FOOT_SPACE:
            return False
        if self.isFacingRight:
            return playerX >= self.x and playerX < self.x + self.length
        return playerX + player.WIDTH > self.x - self.length and playerX + player.WIDTH <= self.x  
                 
class Enemy(pygame.sprite.Sprite):   
    
    PATROL_SPEED = 1
    ATTACK_SPEED = 6
    FRAME_RATE_CHANGE_SPEED = 10
    FRAME_RATE_CHANGE_ANIM = 10
    ATTACK_RANGE = 400
    WIDTH = 68
    HEIGHT = 60
    FOOT_SPACE = 4 # Space between foot and ground according to image size 
    PATROL_STATE = 0
    ATTACK_STATE = 1  
    DEAD_STATE = 2
    
    def __init__(self, x, y, flipPoint1, flipPoint2):
        super().__init__()
        
        self.frame_count_change_speed = -1
        
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 03.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 04.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 05.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Run/Run 06.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Attack/Attack 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Attack/Attack 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Attack/Attack 03.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Attack/Attack 04.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Attack/Attack 05.png')))          
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Dead Hit/Dead Hit 01.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Dead Hit/Dead Hit 02.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Dead Hit/Dead Hit 03.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets\Enemy', 'Dead Hit/Dead Hit 04.png')))
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(self.WIDTH, self.HEIGHT))
            self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        
        self.animInfo = [AnimInfo(0, 6), AnimInfo(6, 5), AnimInfo(11, 4)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        
        self.velocity = pygame.math.Vector2(self.PATROL_SPEED, 0)
        
        self.rayCast2d = RayCast2D(x, y, flipPoint1, flipPoint2, True)

        self.isFacingRight = True
        self.state = self.PATROL_STATE
        self.flipPoint1 = flipPoint1
        self.flipPoint2 = flipPoint2

    def update(self, player):
        self.move()
        
        # Player in attack range
        if player.state != self.DEAD_STATE:
            if self.rayCast2d.collide_player(player):
                if self.state != self.ATTACK_STATE: self.attack()
            else:
                if self.state != self.PATROL_STATE: self.patrol()
        
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//self.FRAME_RATE_CHANGE_ANIM]
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*self.FRAME_RATE_CHANGE_ANIM:
            if self.state == self.DEAD_STATE: 
                self.kill()
            self.frameCount = 0
            
        # Change speed
        if self.frame_count_change_speed != -1:
            if self.state == self.PATROL_STATE:
                if self.velocity.x >= -self.PATROL_SPEED and self.velocity.x <= self.PATROL_SPEED:
                    self.velocity.x = -self.PATROL_SPEED if self.velocity.x < 0 else self.PATROL_SPEED
                    self.frame_count_change_speed = -1
                else:
                    if self.frame_count_change_speed % self.FRAME_RATE_CHANGE_SPEED == 0:    
                        self.velocity.x -= 1 if self.velocity.x > 0 else -1
                    self.frame_count_change_speed += 1
                    
            if self.state == self.ATTACK_STATE:
                if self.velocity.x >= self.ATTACK_SPEED or self.velocity.x <= -self.ATTACK_SPEED:
                    self.velocity.x = -self.ATTACK_SPEED if self.velocity.x < 0 else self.ATTACK_SPEED
                    self.frame_count_change_speed = -1
                else:
                    if self.frame_count_change_speed % self.FRAME_RATE_CHANGE_SPEED == 0:   
                        self.velocity.x -= 1 if self.velocity.x < 0 else -1
                    self.frame_count_change_speed += 1
        
    def move(self):
        self.rect.x += self.velocity.x
        self.rayCast2d.change_x(self.rect.x)
        if self.rect.x <= self.flipPoint1 or self.rect.x + self.WIDTH >= self.flipPoint2:
            self.flip()
    
    def flip(self):
        self.velocity.x = -self.velocity.x 
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        self.isFacingRight = not self.isFacingRight
        self.rayCast2d.flip()
    
    def dead(self):
        self.state = self.DEAD_STATE
        self.frameCount = 0
        self.frame_count_change_speed = -1
        self.velocity.x = 0
        
    def attack(self):
        self.state = self.ATTACK_STATE
        self.frameCount = 0
        self.frame_count_change_speed = 0  
        
    def patrol(self):
        self.state = self.PATROL_STATE
        self.frameCount = 0
        self.frame_count_change_speed = 0
        
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag

