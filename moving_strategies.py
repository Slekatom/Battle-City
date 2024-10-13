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

class MovingStrategyB(sprite.Sprite):
    def move(self, target):
        k = key.get_pressed() 
        if k[K_s]:
            if k[K_a] != True and k[K_d] != True:
                target.rect.y += target.speed
                if target.rect.bottom > 700:
                    target.rect.bottom = 700
                target.diraction = "down"
        if k[K_w]:
            if k[K_a] != True and k[K_d] != True:
                target.rect.y -= target.speed
                if target.rect.top < 0:
                    target.rect.top = 0
                target.diraction = "up"
        
        if k[K_a]:
            target.rect.x -= target.speed
            if target.rect.left < 0:
                target.rect.left = 0
            target.diraction = "left"
            
        if k[K_d]:
            target.rect.x += target.speed
            if target.rect.right > 1200:
                target.rect.right = 1200
            target.diraction = "right"
        