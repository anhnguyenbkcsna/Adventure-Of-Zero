import pygame
import os
import random
from player import Player
from enemy import Enemy
from cannon import Cannon
from object import Block, BreakableObject
from item import Apple

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()

SCENE_NAME_AREA = (0, 0)
BLOCK_SIZE = 32
FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_TEXT_STYLE = pygame.font.Font('freesansbold.ttf', 20)
FPS = 60

pygame.display.set_caption('Adventure Of Zero')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
class Scene():
    def __init__(self):
        self.nextscene = self
    
    def next_scene(self):
        raise NotImplementedError
    
    def update(self, inputs):
        raise NotImplementedError
    
    def render(self, screen):
        raise NotImplementedError
    
    def terminate(self):
        self.nextscene = None
    
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return PlayScene()

    def update(self, inputs):
        pass
    
    def render(self):
        screen.fill((0, 0, 0))
        scene_name = FONT.render('Menu Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)
class EndScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return MenuScene()

    def update(self, inputs):
        pass
    
    def render(self):
        screen.fill((0, 0, 0))
        scene_name = FONT.render('End Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)

############ PLAY SCENE ############

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 30, 50)
        
        # Enemy
        self.enemyGroup = pygame.sprite.Group()
        enemy = Enemy(BLOCK_SIZE*3, SCREEN_HEIGHT - BLOCK_SIZE - Enemy.HEIGHT + Enemy.FOOT_SPACE, BLOCK_SIZE*2, (SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE)
        self.enemyGroup.add(enemy)
        
        # Cannon
        self.cannonGroup = pygame.sprite.Group()
        cannon = Cannon(0, SCREEN_HEIGHT - 2 * BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, True)
        self.cannonGroup.add(cannon)
        cannon = Cannon((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE, SCREEN_HEIGHT - 2 * BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, False)
        self.cannonGroup.add(cannon)
        
        # generate ground
        self.blocks = []
        for i in range(SCREEN_WIDTH // (BLOCK_SIZE * 2)):
            self.blocks.append(Block(i * BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
        self.blocks.append(Block(0, SCREEN_HEIGHT - 2*BLOCK_SIZE, BLOCK_SIZE))
        self.blocks.append(Block(BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE, BLOCK_SIZE))
        self.blocks.append(Block((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 1) * BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE, BLOCK_SIZE))
        self.blocks.append(Block((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE, BLOCK_SIZE))
        
        # Breakable objects
        self.generate_breakable_objects()
        self.items = pygame.sprite.Group()
            
    def next_scene(self):
        return EndScene()

    def update(self, inputs):
        self.player.update(inputs, self.blocks, self.breakable_objects)
        
        for obj in self.breakable_objects:
            obj.update()
            if obj.is_broken == True:
                print('not object')
                item = obj.drop_item()
                if item:
                    self.items.add(item)
        
        for item in self.items:
            item.update()
        
        for item in self.items:
            if pygame.sprite.collide_rect(self.player, item):
                self.player.collect_item(item)
        
        self.enemyGroup.update(self.player)
        self.cannonGroup.update()
        for cannon in self.cannonGroup.sprites():
            cannon.cannonBallGroup.update(self.player)
    
    def render(self):
        screen.fill((255, 255, 255))
        # Draw the blocks
        for block in self.blocks:
            block.draw(screen)
        
        # draw objects
        for obj in self.breakable_objects:
            obj.draw(screen)
        
        for item in self.items:
            item.draw(screen)
        
        # Draw the player 
        self.player.draw(screen)
        self.enemyGroup.draw(screen)
        self.cannonGroup.draw(screen)
        for cannon in self.cannonGroup.sprites():
            cannon.cannonBallGroup.draw(screen)
            
        # Display the current level and score
        level_text = FONT.render(f'Level: {self.player.level}', True, (0, 0, 0))
        score_text = FONT.render(f'Score: {self.player.score}', True, (0, 0, 0))
    
        screen.blit(level_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))

        scene_name = FONT.render('Play Scene', True, (0, 0, 0))
        screen.blit(scene_name, SCENE_NAME_AREA)
        
    def generate_breakable_objects(self):
        self.breakable_objects = pygame.sprite.Group()
        existing_positions = []

        for i in range(5):
            valid_position = False
            while not valid_position:
                x = random.randint(BLOCK_SIZE * 2, SCREEN_WIDTH // 2 - BLOCK_SIZE * 2)
                y = SCREEN_HEIGHT - BLOCK_SIZE * 2
                new_object = BreakableObject(x, y, BLOCK_SIZE, BLOCK_SIZE)
                valid_position = True

                for position in existing_positions:
                    if abs(x - position[0]) <= 20:
                        valid_position = False
                        break

                if valid_position:
                    self.breakable_objects.add(new_object)
                    existing_positions.append((x, y))
        
    
class Game():
    def __init__(self):
        self.active_scene = MenuScene()
    
    def run(self):
        while self.active_scene != None:
            pressed_keys = pygame.key.get_pressed()
            # filtered_events = []
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active_scene.terminate()
                else:
                    # TAB to next scene
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        self.active_scene = self.active_scene.next_scene()
                # filtered_events.append(event)
            
            # Manage scene
            input_keys = pygame.key.get_pressed()
            self.active_scene.update(input_keys)
            self.active_scene.render()
            
            self.active_scene = self.active_scene.nextscene
            
            # Update and tick
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    clock = pygame.time.Clock()
    game = Game()
    game.run()
    pygame.quit()
    
# Ref https://github.com/joncoop/pygame-scene-manager/blob/master/scene_manager.py