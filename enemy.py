from pygame import *
from abc import ABC, abstractmethod
width = 1200
height = 700
window = display.set_mode((width, height))

class Enity(ABC): # Абстрактний клас забов'язує прилеглі класи рухатися
    @abstractmethod 
    def move(self, x, y):
        pass

class MovingStrategyA(Enity):
    def move(self, enemy):
        target_x, target_y, diraction = enemy.patrol_route[enemy.current_target]

        # Рух по горизонталі
        enemy.diraction = diraction
        if enemy.rect.x < target_x:
            enemy.rect.x += enemy.speed
            
        elif enemy.rect.x > target_x:
            enemy.rect.x -= enemy.speed
            

        # Рух по вертикалі, тільки якщо x досяг цільового
        if abs(enemy.rect.x - target_x) <= enemy.speed:
            if enemy.rect.y < target_y:
                enemy.rect.y += enemy.speed
                
            elif enemy.rect.y > target_y:
                enemy.rect.y -= enemy.speed
        enemy.rotate_image()
       # print(self.rect.x, self.rect.y)
    # Якщо досягнуто ціль, переходимо до наступної точки
        if abs(enemy.rect.x - target_x) <= enemy.speed and abs(enemy.rect.y - target_y) <= enemy.speed:
            enemy.current_target = (enemy.current_target + 1) % len(enemy.patrol_route)
class EnemyTypeA(sprite.Sprite):
    def __init__(self, x, y, damage, speed, patrol_route, enemy_image, size):
        super().__init__()
        self.size = size
        self.enemy_image = enemy_image
        self.original_image = transform.scale(image.load("player.png"), self.size)  #оригінальне незмінне фото (потрібно для обертання самого зображення)
        self.image = self.original_image.copy()  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.speed = speed
        self.patrol_route = patrol_route  
        self.current_target = 0
        self.diraction = "up"

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def set_movement_strategy(self, strategy):
        self.movement_strategy = strategy
    def rotate_image(self):
        if self.diraction == "left":
            self.image = transform.rotate(self.original_image, 90)
        elif self.diraction == "right":
            self.image = transform.rotate(self.original_image, -90)
        
        elif self.diraction == "up":
            self.image = transform.rotate(self.original_image, 0)
        elif self.diraction == "down":
            self.image = transform.rotate(self.original_image, 180)
    
        #self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        if self.movement_strategy:
            self.movement_strategy.move(self)
        

class EnemyFactory(): 
    def create_enemy(self, enemy_type, x, y, patrol_route, enemy: EnemyTypeA):
        if enemy_type == 'A':
            enemy.rect.x = x
            enemy.rect.y = y
            enemy.patrol_route = patrol_route
            return EnemyTypeA(enemy.rect.x, enemy.rect.y, enemy.damage, enemy.speed, enemy.patrol_route, enemy.enemy_image, enemy.size)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
