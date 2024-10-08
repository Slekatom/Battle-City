from abc import ABC, abstractmethod
from pygame import *
import patrol_route
import notmoving
import enemy

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



class MovingStrategyB(enemy.Enity):
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
        
        

class Player(enemy.Enity, sprite.Sprite): 
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

    def set_strategy(self, strategy):
        self.strategy = strategy

    def move(self, walls):
        prev_pos = self.rect.copy() # При колізії повернення на позицію до
        if self.strategy:
            self.strategy.move(self)
        if not self.allowed_move(walls):
            self.rect = prev_pos
        self.rotate_image()

    def take_damage(self, amount, game):
        self.hp -= amount
        if self.hp <= 0:
            game.end()

    def add_score(self, points):
        self.score += points

class Scene():  # Сцена 
    pass


class Shoot():  # Класс для шмаляння
    pass

class Colision():
    def check_tank_colision(self, player: Player, enemy_list, game: Game):
        if sprite.spritecollide(player, enemy_list, False):
            game.end()
            return True
        else:
            return False
        
game = Game(1, 2, 3, 4)
game.start()

game_back_ground = notmoving.NotMoving("background.jpg", 0, 0, (1200, 700))

move_stratagyA = enemy.MovingStrategyA()
move_stratagyB = MovingStrategyB()

player = Player(1100, 600, 100, 0, 5, (50, 90))
player.set_strategy(move_stratagyB)

wall1 = notmoving.NotMoving("wall.jpg", 200, 600, (50, 250))
wall2 = notmoving.NotMoving("wall.jpg", 0, 450, (300, 50))
wall3 = notmoving.NotMoving("wall.jpg", 150, 450-200, (50, 200))
wall4 = notmoving.NotMoving("wall.jpg", 450, 400, (50, 300))
wall5 = notmoving.NotMoving("wall.jpg", 650, 550, (250, 50))
wall6 = notmoving.NotMoving("wall.jpg", 650, 550-300, (50, 300))
wall7 = notmoving.NotMoving("wall.jpg", 550-100, 250, (200, 50))
wall8 = notmoving.NotMoving("wall.jpg", 550-100, 0, (50, 150))
wall9 = notmoving.NotMoving("wall.jpg", 950, 0, (50, 150))
wall10 = notmoving.NotMoving("wall.jpg", 1200-300, 350, (300, 50))

walls = sprite.Group()
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)
walls.add(wall7)
walls.add(wall8)
walls.add(wall9)
walls.add(wall10)

enemy_creator = enemy.EnemyFactory()

enemy_type_A = enemy.EnemyTypeA(100, 300, 4, 5, patrol_route.patrol_route1, "player.png", (50, 90))
enemy1 = enemy_creator.create_enemy('A', 100, 300, patrol_route.patrol_route1, enemy_type_A)
enemy2 = enemy_creator.create_enemy('A', 50, 600, patrol_route.patrol_route2, enemy_type_A)
enemy3 = enemy_creator.create_enemy('A', 1100, 50, patrol_route.patrol_route3, enemy_type_A)


enemy1.set_movement_strategy(move_stratagyA)
enemy2.set_movement_strategy(move_stratagyA)
enemy3.set_movement_strategy(move_stratagyA)
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)

end_hammer = Colision()
while game.game == True:
    for e in event.get():
        if e.type == QUIT:                    
            game.end()
    
    game_back_ground.reset()
    player.reset()
    player.move(walls)
    
    for i in walls:
        i.reset()

    for i in enemies:
        i.reset()
        i.move()       
 
    end_hammer.check_tank_colision(player, enemies, game)
    game.update()