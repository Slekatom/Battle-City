from pygame import *
from abc import ABC, abstractmethod
width = 1200
height = 700
window = display.set_mode((width, height))
class Enity(ABC): # Абстрактний клас забов'язує прилеглі класи рухатися
    @abstractmethod 
    def move(self, x, y):
        pass

class Player(Enity, sprite.Sprite): 
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

    def take_damage(self, amount, game):
        self.hp -= amount
        if self.hp <= 0:
            game.end()

    def add_score(self, points):
        self.score += points