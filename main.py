import pygame
import os
import csv
import random
from player import Player
from enemy import Enemy
from cannon import Cannon
from object import Block, GrassBlock, BreakableObject, Apple, Banana, Star, Flag

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

pygame.init()

SCENE_NAME_AREA = (0, 0)
BLOCK_SIZE = 40
FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_TEXT_STYLE = pygame.font.Font('freesansbold.ttf', 20)
FPS = 60

pygame.display.set_caption('Adventure Of Zero')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# class World():
    

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
        return PlayScene("Easy")

    def update(self, inputs):
        pass
    
    def render(self):
        background = (pygame.image.load(os.path.join('Assets\Background', 'background.png')))
        background = pygame.transform.scale(background, (1280, 720))
        screen.blit(background, (SCREEN_WIDTH // 2 - 640, SCREEN_HEIGHT // 2 - 360))
        
        start_btn = (pygame.image.load(os.path.join('Assets\Button', 'startbutton.png')))
        start_btn = pygame.transform.scale(start_btn, (215, 100))
        
        setting_btn = (pygame.image.load(os.path.join('Assets\Button', 'setbutton.png')))
        setting_btn = pygame.transform.scale(setting_btn, (215, 100))
        
        about_btn = (pygame.image.load(os.path.join('Assets\Button', 'Aboutbutton.png')))
        about_btn = pygame.transform.scale(about_btn, (215, 100))
        
        quit_btn = (pygame.image.load(os.path.join('Assets\Button', 'quitbutton.png')))
        quit_btn = pygame.transform.scale(quit_btn, (215, 100))

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 - 250, 215, 100)
        option_button = pygame.Rect(SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 - 125, 215, 100)
        about_button = pygame.Rect(SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 + 0, 215, 100)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 + 125, 215, 100)
        
        screen.blit(start_btn, (SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 - 250))
        screen.blit(setting_btn, (SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 - 125))
        screen.blit(about_btn, (SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 + 0))
        screen.blit(quit_btn, (SCREEN_WIDTH // 2 - 108, SCREEN_HEIGHT // 2 + 125))
        
        if pygame.mouse.get_pressed()[0]:
            if play_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = self.next_scene()
            elif option_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = OptionScene()
            elif about_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = AboutScene()
            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                return
class OptionScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return MenuScene()

    def update(self, inputs):
        pass
    
    def render(self):
        background = (pygame.image.load(os.path.join('Assets\Background', 'background.png')))
        background = pygame.transform.scale(background, (1280, 720))
        screen.blit(background, (SCREEN_WIDTH // 2 - 640, SCREEN_HEIGHT // 2 - 360))
        
        ez_mode = (pygame.image.load(os.path.join('Assets\Button', 'Easy.png')))
        ez_mode = pygame.transform.scale(ez_mode, (215, 100))
        ez_button = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 215, 100)
    
        hard_mode = (pygame.image.load(os.path.join('Assets\Button', 'Hard.png')))
        hard_mode = pygame.transform.scale(hard_mode, (215, 100))
        hard_button = pygame.Rect(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2, 215, 100)
        
        screen.blit(ez_mode, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
        screen.blit(hard_mode, (SCREEN_WIDTH // 2 + 300 - 215, SCREEN_HEIGHT // 2))
        
        if pygame.mouse.get_pressed()[0]:
            if ez_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = PlayScene("Easy")
            elif hard_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = PlayScene("Hard")
class AboutScene(Scene):
    def __init__(self):
        super().__init__()
    
    def next_scene(self):
        return MenuScene()

    def update(self, inputs):
        pass
    
    def render(self):
        background = (pygame.image.load(os.path.join('Assets\Background', 'background.png')))
        background = pygame.transform.scale(background, (1280, 720))
        screen.blit(background, (SCREEN_WIDTH // 2 - 640, SCREEN_HEIGHT // 2 - 360))
        

        scene_name = FONT.render('About Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)
        
class EndScene(Scene):
    def __init__(self, score, stars):
        super().__init__()
        self.score = score
        self.stars = stars
    
    def next_scene(self):
        return MenuScene()

    def update(self, inputs):
        pass
    
    def render(self):
        background = (pygame.image.load(os.path.join('Assets\Background', 'background.png')))
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))
        
        Sum = (pygame.image.load(os.path.join('Assets\Background', 'Sum.png')))
        Sum = pygame.transform.scale(Sum, (450,400))
        screen.blit(Sum, (SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2 - 250))
        
        for i in range(self.stars):
            star = (pygame.image.load(os.path.join('Assets\Objects', 'star.png')))
            star = pygame.transform.scale(star, (50,50))
            # screen.blit(star, (SCREEN_WIDTH // 2 - 100 + 75 * i, SCREEN_HEIGHT // 2 - 250 + 200))
            screen.blit(star, (SCREEN_WIDTH // 2 - 100 + 75 * i, 20))
        
        scene_name = FONT.render(f'Score: {self.score}', True, (145, 24, 29))
        screen.blit(scene_name, (335,350))
        
        restart_btn = (pygame.image.load(os.path.join('Assets\Button', 'restartbutton.png')))
        restart_btn = pygame.transform.scale(restart_btn, (160, 75))
        quit_btn = (pygame.image.load(os.path.join('Assets\Button', 'quitbutton.png')))
        quit_btn = pygame.transform.scale(quit_btn, (160, 75))
        
        replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 +170, 160, 75)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 170, 160, 75)
        
        screen.blit(restart_btn, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 + 170))
        screen.blit(quit_btn, (SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 170))
        if pygame.mouse.get_pressed()[0]:
            if replay_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = PlayScene("Easy")
            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = MenuScene("Hard")
        
        

############ PLAY SCENE ############

class PlayScene(Scene):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        # Generate map
        ROWS = 16
        COLS = 150 + 12
        world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)
        # Load in level data and create world
        with open(f'Levels/level0_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
                    
        # Generate world based on data
        self.blocks = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.cannonGroup = pygame.sprite.Group()
        self.breakable_objects = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.end = pygame.sprite.Group()
        
        for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    if tile == 0:
                        block = GrassBlock(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        self.blocks.add(block)
                    elif tile == 1:
                        block = Block(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        self.blocks.add(block)
                    elif tile == 9:
                        self.player = Player(x * BLOCK_SIZE, y * BLOCK_SIZE, 60, 60, self.mode)
                    elif tile == 10:
                        enemy = Enemy(BLOCK_SIZE * x, y * BLOCK_SIZE + Enemy.FOOT_SPACE, BLOCK_SIZE * (x - 3), BLOCK_SIZE * (x + 7))
                        # enemy = Enemy(x * BLOCK_SIZE, y * BLOCK_SIZE + Enemy.FOOT_SPACE, BLOCK_SIZE * (x-1), 5 * BLOCK_SIZE)  
                        self.enemyGroup.add(enemy)
                    elif tile == 11:
                        cannon = Cannon(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, False)
                        self.cannonGroup.add(cannon)
                    elif tile == 12:
                        cannon = Cannon(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, True)
                        self.cannonGroup.add(cannon)
                    elif tile == 13:
                        obj = BreakableObject(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        self.breakable_objects.add(obj)
                    elif tile == 14:
                        star = Star(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        self.stars.add(star)
                    elif tile == 15:
                        flag = Flag(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        self.end.add(flag)
            
    def next_scene(self):
        return EndScene(self.player.score, self.player.stars)

    def update(self, inputs):
        objects = []
        objects.extend(self.blocks)
        objects.extend(self.breakable_objects)
        objects.extend(self.stars)
        objects.extend(self.enemyGroup)
        objects.extend(self.cannonGroup)
        objects.extend(self.end)
        for cannon in self.cannonGroup.sprites():
            objects.extend(cannon.cannonBallGroup)
        for breakableObject in self.breakable_objects.sprites():
            objects.extend(breakableObject.itemGroup)
        
        self.player.update(inputs, objects)
        
        for obj in objects:
            obj.update(self.player)
        
        if self.player.hp <= 0:
            self.nextscene = self.next_scene()
    
    def render(self):
        background = (pygame.image.load(os.path.join('Assets\Background', 'background.png')))
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))
        
        # Draw the blocks
        for block in self.blocks:
            block.draw(screen)
        
        # draw objects
        for obj in self.breakable_objects:
            obj.itemGroup.draw(screen)
            obj.draw(screen)
        
        for breakable_object in self.breakable_objects:
            breakable_object.itemGroup.draw(screen)
        
        for star in self.stars:
            star.draw(screen)
        
        for flag in self.end:
            flag.draw(screen)
        
        self.enemyGroup.draw(screen)
        self.cannonGroup.draw(screen)
        for cannon in self.cannonGroup.sprites():
            cannon.cannonBallGroup.draw(screen)
            
        # Display the current level and score
        score_text = FONT.render(f'Score: {self.player.score}', True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 170, 0))

        
        self.player.draw(screen)
        
        # Upgrde character menu
        if (self.player.score // 50) > self.player.upgrade_time:
            button = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200, 400, 250)
            buff_atk = pygame.Rect(SCREEN_WIDTH // 2 - 200 + 25, SCREEN_HEIGHT // 2 - 200 + 25, 150, 150)
            add_atk = pygame.image.load(os.path.join('Assets\Button', 'addatk.png'))
            add_atk = pygame.transform.scale(add_atk, (150, 150))
            
            buff_hp = pygame.Rect(SCREEN_WIDTH // 2 + 25, SCREEN_HEIGHT // 2 - 200 + 25, 150, 150)
            add_hp = pygame.image.load(os.path.join('Assets\Button', 'addhp.png'))
            add_hp = pygame.transform.scale(add_hp, (150, 150))
            
            skip_btn = pygame.Rect(SCREEN_WIDTH // 2 - 107.5/2, SCREEN_HEIGHT // 2 - 10, 107.5, 50)
            skip_image = pygame.image.load(os.path.join('Assets\Button', 'quitbutton.png'))
            skip_image = pygame.transform.scale(skip_image, (107.5, 50))
            
            pygame.draw.rect(screen, (214, 124, 93), button)
            screen.blit(add_atk, (SCREEN_WIDTH // 2 - 200 + 25, SCREEN_HEIGHT // 2 - 200 + 25))
            screen.blit(add_hp, (SCREEN_WIDTH // 2 + 25, SCREEN_HEIGHT // 2 - 200 + 25))
            screen.blit(skip_image, (SCREEN_WIDTH // 2 - 107.5/2, SCREEN_HEIGHT // 2 - 10))
            
            if pygame.mouse.get_pressed()[0]:
                if buff_atk.collidepoint(pygame.mouse.get_pos()):
                    self.player.atk += 1
                    self.player.score -= 50
                    self.player.upgrade_time += 1
                elif buff_hp.collidepoint(pygame.mouse.get_pos()):
                    self.player.hp += 1
                    self.player.score -= 50
                    self.player.upgrade_time += 1
                elif skip_btn.collidepoint(pygame.mouse.get_pos()):
                    self.player.upgrade_time = self.player.score // 50
                    print(self.player.upgrade_time)
    
class Game():
    def __init__(self):
        self.active_scene = MenuScene()
    
    def run(self):
        bg_sound = pygame.mixer.Sound(os.path.join('Assets\Sound', 'Game_sound.mp3'))
        bg_sound.set_volume(0.5)
        pygame.mixer.Sound.play(bg_sound, -1)
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