# Complete your game here

import pygame 
import random 

class MonsterEscape:
    def __init__(self):
        pygame.init()

       
        self.window_width = 640 
        self.window_height = 480
        self.tile_size = 40
        self.speed = 4
        self.robot_speed = 2

        self.load_images()
        self.new_game()

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
          
        self.monster_img, self.robot_img, self.coin_img, self.door_img = self.images
        self.font = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Monster Escape")  

        self.loop()

    def load_images(self):
        self.images = []
        for name in ["monster", "robot", "coin", "door"]:
            self.images.append(pygame.image.load(name + ".png"))

    def new_game(self):
        self.monster = [0, 0]
        self.spawn_new_coin()  
        self.robot = [random.randint(5, 14) * self.tile_size, random.randint(5, 10) * self.tile_size]
        self.door = None
        self.score = 0
        self.has_coin = False
        self.game_over = False
        self.win = False

    def spawn_new_coin(self):
        self.coin = [random.randint(1, 14) * self.tile_size, random.randint(1, 10) * self.tile_size]

    def move_robot_towards_monster(self):
        dx = self.monster[0] - self.robot[0]
        dy = self.monster[1] - self.robot[1]

        if dx > 0:
            self.robot[0] += min(self.robot_speed, dx)
        elif dx < 0:
            self.robot[0] -= min(self.robot_speed, -dx)

        if dy > 0:
            self.robot[1] += min(self.robot_speed, dy)
        elif dy < 0:
            self.robot[1] -= min(self.robot_speed, -dy)


    def loop(self):
            clock = pygame.time.Clock()
            while True:
                self.handle_events()
                self.update_game()
                self.draw_screen()
                clock.tick(60)

    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    self.new_game()


        if not self.game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.monster[0] -= self.speed
            if keys[pygame.K_RIGHT]:
                self.monster[0] += self.speed
            if keys[pygame.K_UP]:
                self.monster[1] -= self.speed
            if keys[pygame.K_DOWN]:
                self.monster[1] += self.speed

     
            self.monster[0] = max(0, min(self.monster[0], self.window_width - self.tile_size))
            self.monster[1] = max(0, min(self.monster[1], self.window_height - self.tile_size))


    def update_game(self):
        if self.game_over:
            return

        self.move_robot_towards_monster()

        monster_rect = pygame.Rect(self.monster[0], self.monster[1], self.tile_size, self.tile_size)
        robot_rect = pygame.Rect(self.robot[0], self.robot[1], self.tile_size, self.tile_size)
        
        if monster_rect.colliderect(robot_rect):
            self.game_over = True
            return

        if not self.has_coin and self.coin:
            coin_rect = pygame.Rect(self.coin[0], self.coin[1], self.tile_size, self.tile_size)
            if monster_rect.colliderect(coin_rect):
                self.has_coin = True
                self.door = [random.randint(1, 14) * self.tile_size, random.randint(1, 10) * self.tile_size]
                self.coin = None 

        if self.has_coin and self.door:
            door_rect = pygame.Rect(self.door[0], self.door[1], self.tile_size, self.tile_size)
            if monster_rect.colliderect(door_rect):
                self.score += 1
                self.has_coin = False
                self.door = None
                if self.score >= 10:
                    self.win = True
                    self.game_over = True
                else:
                    self.spawn_new_coin()


    def draw_screen(self):
        self.screen.fill((128, 128, 128))

        if self.coin:
            self.screen.blit(self.coin_img, self.coin)

        if self.door:
            self.screen.blit(self.door_img, self.door)

        self.screen.blit(self.robot_img, self.robot)
        self.screen.blit(self.monster_img, self.monster)

     
        text = self.font.render(f"Banked Coins: {self.score}", True, (255, 192, 203))
        self.screen.blit(text, (10, 10))

        if self.has_coin:
            status = "You have a coin! Find the door!"
        else:
            status = "Find a coin!"
        text2 = self.font.render(status, True, (200, 200, 255))
        self.screen.blit(text2, (10, 40))

        if self.game_over:
            if self.win:
                msg = "Winner, Winner, Chicken dinner. Press F2 to play again."
            else:
                msg = "That's an L! Press F2 to try again."
            game_text = self.font.render(msg, True, (255, 0, 0))
            self.screen.blit(game_text, (self.window_width // 2 - game_text.get_width() // 2, self.window_height // 2))

     
        pygame.display.flip()

if __name__ == "__main__":
    MonsterEscape()