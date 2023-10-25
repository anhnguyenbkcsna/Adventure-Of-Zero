import pygame
import os

PATROL_SPEED = 1
ATTACK_SPEED = 6
FRAME_RATE_CHANGE_SPEED = 10
ATTACK_RANGE = 300
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 55
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PATROL_STATE = 0
ATTACK_STATE = 1  
DEAD_STATE = 2

class AnimInfo():
   def __init__(self, startFrame, numFrames):
       self.startFrame = startFrame
       self.numFrames = numFrames 

class RayCast2D():
    def __init__(self, enemy_x, enemy_y, flipPoint1, flipPoint2, enemyIsFacingRight):
        self.flipPoint1 = flipPoint1
        self.flipPoint2 = flipPoint2
        self.isFacingRight = enemyIsFacingRight
        self.x = enemy_x + ENEMY_WIDTH if enemyIsFacingRight else enemy_x
        self.y = enemy_y
        self.length = min(ATTACK_RANGE, self.flipPoint2 - self.x + 1 if self.isFacingRight else self.x - self.flipPoint1 + 1)
    
    def flip(self):
        self.x -= ENEMY_WIDTH if self.isFacingRight else -ENEMY_WIDTH 
        self.isFacingRight = not self.isFacingRight
        
    def change_x(self, newX):
        self.x = newX
        self.length = min(ATTACK_RANGE, self.flipPoint2 - self.x + 1 if self.isFacingRight else self.x - self.flipPoint1 + 1)
        
    def collide_player(self, playerX, playerY):
        if playerY > self.y + ENEMY_HEIGHT or playerY + PLAYER_HEIGHT < self.y:
            return False
        if self.isFacingRight:
            return playerX >= self.x and playerX < self.x + self.length
        return playerX + PLAYER_WIDTH > self.x - self.length and playerX + PLAYER_WIDTH <= self.x  
                 
class Enemy(pygame.sprite.Sprite):   
    
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
            self.sprites[i] = pygame.transform.scale(self.sprites[i],(ENEMY_WIDTH, ENEMY_HEIGHT))
            self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
        
        self.animInfo = [AnimInfo(0, 6), AnimInfo(6, 5), AnimInfo(11, 4)]
        self.frameCount = 0 
        
        self.image = self.sprites[0]
        
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        
        self.velocity = pygame.math.Vector2(PATROL_SPEED, 0)
        
        self.rayCast2d = RayCast2D(x, y, flipPoint1, flipPoint2, True)

        self.isFacingRight = True
        self.state = PATROL_STATE
        self.flipPoint1 = flipPoint1
        self.flipPoint2 = flipPoint2

    def update(self, keys, playerX, playerY):
        self.update_input(keys)
        self.move()
        
        # Player in attack range
        if self.rayCast2d.collide_player(playerX, playerY):
            if self.state != ATTACK_STATE: self.attack()
        else:
            if self.state != PATROL_STATE: self.patrol()
        
        # Animation
        if self.frameCount % 10 == 0:
            self.image = self.sprites[self.animInfo[self.state].startFrame + self.frameCount//10]
            if not self.isFacingRight:
                self.image = pygame.transform.flip(self.image, True, False)
        self.frameCount += 1
        if self.frameCount > (self.animInfo[self.state].numFrames - 1)*10:
            if self.state == DEAD_STATE: 
                self.kill()
            self.frameCount = 0
            
        # Change speed
        if self.frame_count_change_speed != -1:
            if self.state == PATROL_STATE:
                if self.velocity.x >= -PATROL_SPEED and self.velocity.x <= PATROL_SPEED:
                    self.velocity.x = -PATROL_SPEED if self.velocity.x < 0 else PATROL_SPEED
                    self.frame_count_change_speed = -1
                else:
                    if self.frame_count_change_speed % FRAME_RATE_CHANGE_SPEED == 0:    
                        self.velocity.x -= 1 if self.velocity.x > 0 else -1
                    self.frame_count_change_speed += 1
                    
            if self.state == ATTACK_STATE:
                if self.velocity.x >= ATTACK_SPEED or self.velocity.x <= -ATTACK_SPEED:
                    self.velocity.x = -ATTACK_SPEED if self.velocity.x < 0 else ATTACK_SPEED
                    self.frame_count_change_speed = -1
                else:
                    if self.frame_count_change_speed % FRAME_RATE_CHANGE_SPEED == 0:   
                        self.velocity.x -= 1 if self.velocity.x < 0 else -1
                    self.frame_count_change_speed += 1
        
    def move(self):
        self.rect.x += self.velocity.x
        self.rayCast2d.change_x(self.rect.x)
        if self.rect.x <= self.flipPoint1 or self.rect.x + ENEMY_WIDTH >= self.flipPoint2:
            self.flip()
    
    def flip(self):
        self.velocity.x = -self.velocity.x 
        self.isFacingRight = not self.isFacingRight
        self.rayCast2d.flip()

    def update_input(self, input_keys):
        if input_keys[pygame.K_a]:
            self.attack()   
        if input_keys[pygame.K_p]:
            self.patrol()
        if input_keys[pygame.K_d]:
            self.dead()
    
    def dead(self):
        self.state = DEAD_STATE
        self.frameCount = 0
        self.frame_count_change_speed = -1
        self.velocity.x = 0
        
    def attack(self):
        self.state = ATTACK_STATE
        self.frameCount = 0
        self.frame_count_change_speed = 0  
        
    def patrol(self):
        self.state = PATROL_STATE
        self.frameCount = 0
        self.frame_count_change_speed = 0
        
    ############## Getters & Setters ##############
    def set_hp(self, hp):
        self.hp = hp     
    
    def get_hp(self):
        return self.hp
        
    def get_tag(self):
        return self.tag

