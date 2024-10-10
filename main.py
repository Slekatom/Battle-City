from abc import ABC, abstractmethod
from pygame import *

width = 1200
height = 700
window = display.set_mode((width, height))
display.set_caption("Battle City")
clock = time.Clock()
FPS = 60

# mixer.init()
# mixer.music.load('War.mp3')
# mixer.music.set_volume(0.9)
# mixer.music.play(0)

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

class Enity(ABC): # Абстрактний клас забов'язує прилеглі класи рухатися
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

    def take_damage(self, amount, game: Game):
        self.hp -= amount
        if self.hp <= 0:
            game.end()

    def add_score(self, points):
        self.score += points

class Scene():  # Сцена 
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

    def move(self, strategy):
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

game_back_ground = NotMoving("background.jpg", 0, 0, (1200, 700))

player = Player(1100, 600, 100, 0, 5, (50, 90))

wall1 = NotMoving("wall.jpg", 200, 600, (50, 250))
wall2 = NotMoving("wall.jpg", 0, 450, (300, 50))
wall3 = NotMoving("wall.jpg", 150, 450-200, (50, 200))
wall4 = NotMoving("wall.jpg", 450, 400, (50, 300))
wall5 = NotMoving("wall.jpg", 650, 550, (250, 50))
wall6 = NotMoving("wall.jpg", 650, 550-300, (50, 300))
wall7 = NotMoving("wall.jpg", 550-100, 250, (200, 50))
wall8 = NotMoving("wall.jpg", 550-100, 0, (50, 150))
wall9 = NotMoving("wall.jpg", 950, 0, (50, 150))
wall10 = NotMoving("wall.jpg", 1200-300, 350, (300, 50))

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

patrol_route1 = [
    (100, 100, "up"),  
    (300, 100, "right"),
    (300, 180, "down"), 
    (800, 200, "right"),
    (800, 455, "down"), 
    (1000, 455, "right"), 
    (1000, 650, "down"), 
    (550, 650, "left"),
    (550, 300, "up") ,
    (300, 300, "left") ,
    (300, 100, "up") ,
    (100, 100, "left") ,
    (100, 300, "down") 
    
]
patrol_route2 = [
    (50, 600, "up"),  
    (50, 500, "up"),
    (350, 520, "right"), 
    (350, 300, "up"),
    (540, 300, "right"), 
    (540, 630, "down"), 
    (1100, 650, "right"), 
    (1100, 450, "up"),
    (850, 450, "left") ,
    (800, 200, "up") ,
    (350, 200, "left") ,
    (350, 500, "down") ,
    (50, 500, "left"),
    (50, 600, "down") 
    
]
patrol_route3 = [
    (1100, 50, "down"),  
    (1100, 250, "down"),
    (800, 250, "left"), 
    (800, 500, "down"),
    (1100, 500, "right"), 
    (1100, 630, "down"), 
    (530, 630, "left"), 
    (530, 300, "up"),
    (280, 300, "left") ,
    (280, 200, "up") ,
    (1100, 200, "right") ,
    (1100, 200, "up") ,
    (1100, 50, "up") 
    
]
enemy_creator = EnemyFactory()
enemy_type_A = EnemyTypeA(100, 300, 4, 5, patrol_route1, "player.png", (50, 90))
enemy1 = enemy_creator.create_enemy('A', 100, 300, patrol_route1, enemy_type_A)
enemy2 = enemy_creator.create_enemy('A', 50, 600, patrol_route2, enemy_type_A)
enemy3 = enemy_creator.create_enemy('A', 1100, 50, patrol_route3, enemy_type_A)
move_stratagy = MovingStrategyA()
end_hammer = Colision()
enemy1.set_movement_strategy(move_stratagy)
enemy2.set_movement_strategy(move_stratagy)
enemy3.set_movement_strategy(move_stratagy)
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
while game.game == True:
    for e in event.get():
        if e.type == QUIT:                    
            game.end()
    
    game_back_ground.reset()
    player.reset()
    player.move(walls)
    wall1.reset()
    wall2.reset()
    wall3.reset()
    wall4.reset()
    wall5.reset()
    wall6.reset()
    wall7.reset()
    wall8.reset()
    wall9.reset()
    wall10.reset()

    enemy1.reset()
    enemy1.move(move_stratagy)
    enemy2.reset()
    enemy2.move(move_stratagy)
    enemy3.reset()
    enemy3.move(move_stratagy)
    
    end_hammer.check_tank_colision(player, enemies, game)
    game.update()