from abc import ABC, abstractmethod
from pygame import *

width = 1200
height = 700
window = display.set_mode((width, height))
display.set_caption("Battle City")
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('War.mp3')
mixer.music.set_volume(0.9)
mixer.music.play(0)

class Game: # Клас гри в нього додаємо усі об'єкти класів (по типу контроллера)
    def __init__(self, scene, player, enemies, map):
        self.scene = scene
        self.player = player
        self.enemies = enemies
        self.map = map
        self.game = None
    def start(self):
        self.game = True
    def end(self):
        self.game = False
    def update(self):
        clock.tick(FPS)
        display.update()        

class Object(ABC): # Абстрактний клас забов'язує прилеглі класи рухатися
    @abstractmethod 
    def move(self, x, y):
        pass

class NotMoving(sprite.Sprite):  
    def __init__(self, b_image, x, y, size):
        super().__init__()
        self.image = transform.scale(image.load(b_image), size)    
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Object, sprite.Sprite): 
    def __init__(self, x, y, hp, score, speed, size):
        sprite.Sprite.__init__(self)  
        self.hp = hp  
        self.score = score   
        self.original_image = transform.scale(image.load("player.png"), size)  #оригінальне незмінне фото (потрібно для обертання самого зображення)
        self.image = self.original_image.copy() # Точна копія незмінного фото але воно буде обертатись
        self.speed = speed
        self.rect = self.image.get_rect() # Треба для колізій
        self.rect.x = x
        self.rect.y = y
        self.diraction = None

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def rotate_image(self):
        if self.diraction == "left":
            self.image = transform.rotate(self.original_image, 90)
        elif self.diraction == "right":
            self.image = transform.rotate(self.original_image, -90)
        elif self.diraction == "up":
            self.image = self.original_image.copy() 
        elif self.diraction == "down":
            self.image = transform.rotate(self.original_image, 180)
    
        self.rect = self.image.get_rect(center=self.rect.center)

    def allowed_move(self, walls):
        if sprite.spritecollide(self, walls, False):
            return False
        return True

    def move(self, walls):
        k = key.get_pressed()
        prev_pos = self.rect.copy() # При колізії повернення на позицію до

        if k[K_s]:
            if k[K_a] != True and k[K_d] != True:
                self.rect.y += self.speed
                if self.rect.bottom > 700:
                    self.rect.bottom = 700
                self.diraction = "down"
        if k[K_w]:
            if k[K_a] != True and k[K_d] != True:
                self.rect.y -= self.speed
                if self.rect.top < 0:
                    self.rect.top = 0
                self.diraction = "up"
        
        if k[K_a]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            self.diraction = "left"
            
        if k[K_d]:
            self.rect.x += self.speed
            if self.rect.right > 1200:
                self.rect.right = 1200
            self.diraction = "right"
        
        if not self.allowed_move(walls):
            self.rect = prev_pos

        self.rotate_image()

    def take_damage(self, amount, game: Game):
        self.hp -= amount
        if self.hp <= 0:
            game.end()

    def add_score(self, points):
        self.score += points

class Scene():  # Сцена 
    pass

class Enemy(Object, sprite.Sprite): 
    pass

class Shoot():  # Класс для шмаляння
    pass


game = Game(1, 2, 3, 4)
game.start()

game_back_ground = NotMoving("background.jpg", 0, 0, (1200, 700))

player = Player(100, 100, 100, 0, 5, (50, 90))

wall1 = NotMoving("wall.jpg", 200, 300, (50, 200))
wall2 = NotMoving("wall.jpg", 350, 300, (50, 200))

walls = sprite.Group()
walls.add(wall1)
walls.add(wall2)

while game.game == True:
    for e in event.get():
        if e.type == QUIT:                    
            game.end()
    
    game_back_ground.reset()
    player.reset()
    player.move(walls)
    wall1.reset()
    wall2.reset()
    
    game.update()