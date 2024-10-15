from pygame import *
import entity
width = 1200
height = 700
window = display.set_mode((width, height))


class Enemy(sprite.Sprite, entity.Entity):
    def __init__(self, start_x, start_y, x, y, damage, speed, patrol_route, enemy_image, size):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.size = size
        self.enemy_image = enemy_image
        self.original_image = transform.scale(image.load("pictures_and_sounds/player.png"), self.size)  #оригінальне незмінне фото (потрібно для обертання самого зображення)
        self.image = self.original_image.copy()  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.speed = speed
        self.patrol_route = patrol_route  
        self.current_target = 0
        self.diraction = "up"
        self.size = size

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
    def moved_home(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.current_target = 0

        

class EnemyFactory(): 
    def create_enemy(self, enemy_type, x, y, patrol_route, enemytype: Enemy, start_x, start_y):
        if enemy_type == 'A':
            enemytype.start_x = start_x
            enemytype.start_y = start_y
            enemytype.rect.x = x
            enemytype.rect.y = y
            enemytype.patrol_route = patrol_route
            return Enemy(start_x, start_y, enemytype.rect.x, enemytype.rect.y, enemytype.damage, enemytype.speed, enemytype.patrol_route, enemytype.enemy_image, enemytype.size)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
