import pygame
import os
import random
from player import Player
from enemy import Enemy
from cannon import Cannon
from object import Block, BreakableObject, Apple, Banana

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
        

        scene_name = FONT.render('Option Scene', True, (255, 255, 255))
        screen.blit(scene_name, SCENE_NAME_AREA)
        
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
        
        Sum = (pygame.image.load(os.path.join('Assets\Background', 'Sum.png')))
        Sum = pygame.transform.scale(Sum, (450,400))
        screen.blit(Sum, (SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2 - 250))
        
        scene_name = FONT.render('Score', True, (255, 255, 255))
        screen.blit(scene_name, (600,300))
        
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
                self.nextscene = PlayScene()
            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                self.nextscene = MenuScene()
        
        

############ PLAY SCENE ############

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 50, 50)
        
        # Enemy
        self.enemyGroup = pygame.sprite.Group()
        # enemy = Enemy(BLOCK_SIZE*3, SCREEN_HEIGHT - BLOCK_SIZE - Enemy.HEIGHT + Enemy.FOOT_SPACE, BLOCK_SIZE*2, (SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE)
        # self.enemyGroup.add(enemy)
        
        # Cannon
        self.cannonGroup = pygame.sprite.Group()
        cannon = Cannon(0, SCREEN_HEIGHT - BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, True)
        self.cannonGroup.add(cannon)
        # cannon = Cannon((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE, SCREEN_HEIGHT - 2 * BLOCK_SIZE - Cannon.HEIGHT + Cannon.FOOT_SPACE, False)
        # self.cannonGroup.add(cannon)
        
        # generate ground
        self.blocks = []
        for i in range(SCREEN_WIDTH // (BLOCK_SIZE * 2)):
            self.blocks.append(Block(i * BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE))
        # self.blocks.append(Block(0, SCREEN_HEIGHT - 2*BLOCK_SIZE))
        # self.blocks.append(Block(BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE))
        self.blocks.append(Block((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 1) * BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE))
        self.blocks.append(Block((SCREEN_WIDTH // (BLOCK_SIZE * 2) - 2) * BLOCK_SIZE, SCREEN_HEIGHT - 2*BLOCK_SIZE))
        
        # Breakable objects
        self.generate_breakable_objects()
        # self.blocks.append(Block(i * BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE))
            
    def next_scene(self):
        return EndScene()

    def update(self, inputs):
        objects = []
        objects.extend(self.blocks)
        objects.extend(self.breakable_objects)
        objects.extend(self.enemyGroup)
        objects.extend(self.cannonGroup)
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
        screen.fill((255, 255, 255))
        
        # Draw the blocks
        for block in self.blocks:
            block.draw(screen)
        
        # draw objects
        for obj in self.breakable_objects:
            obj.itemGroup.draw(screen)
            obj.draw(screen)
        
        
        self.enemyGroup.draw(screen)
        self.cannonGroup.draw(screen)
        for cannon in self.cannonGroup.sprites():
            cannon.cannonBallGroup.draw(screen)
            
        # Display the current level and score
        level_text = FONT.render(f'Level: {self.player.level}', True, (0, 0, 0))
        score_text = FONT.render(f'Score: {self.player.score}', True, (0, 0, 0))
    
        screen.blit(level_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))

        
        self.player.draw(screen)
        
        # Upgrde character menu
        if self.player.score >= 50:
            button = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 300, 600, 300)
            buff_atk = pygame.Rect(SCREEN_WIDTH // 2 - 300 + 25, SCREEN_HEIGHT // 2 - 300 + 25, 250, 250)
            buff_hp = pygame.Rect(SCREEN_WIDTH // 2 + 25, SCREEN_HEIGHT // 2 - 300 + 25, 250, 250)
            pygame.draw.rect(screen, (150, 70, 70), button, 10)
            pygame.draw.rect(screen, (150, 70, 70), buff_atk, 10)
            pygame.draw.rect(screen, (150, 70, 70), buff_hp, 10)
            if pygame.mouse.get_pressed()[0]:
                if buff_atk.collidepoint(pygame.mouse.get_pos()):
                    self.player.atk += 1
                    self.player.score -= 50
                elif buff_hp.collidepoint(pygame.mouse.get_pos()):
                    self.player.hp += 1
                    self.player.score -= 50
        
    def generate_breakable_objects(self):
        self.breakable_objects = pygame.sprite.Group()
        existing_positions = []

        for i in range(5):
            valid_position = False
            while not valid_position:
                x = random.randint(BLOCK_SIZE * 2, SCREEN_WIDTH // 2 - BLOCK_SIZE * 2)
                y = SCREEN_HEIGHT - BLOCK_SIZE * 2
                new_object = BreakableObject(x, y)
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