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
        target_x, target_y, diraction = self.patrol_route[self.current_target]

        # Рух по горизонталі
        self.diraction = diraction
        if self.rect.x < target_x:
            self.rect.x += self.speed
            
        elif self.rect.x > target_x:
            self.rect.x -= self.speed
            

        # Рух по вертикалі, тільки якщо x досяг цільового
        if abs(self.rect.x - target_x) <= self.speed:
            if self.rect.y < target_y:
                self.rect.y += self.speed
                
            elif self.rect.y > target_y:
                self.rect.y -= self.speed
        self.rotate_image()
        print(self.rect.x, self.rect.y)
    # Якщо досягнуто ціль, переходимо до наступної точки
        if abs(self.rect.x - target_x) <= self.speed and abs(self.rect.y - target_y) <= self.speed:
            self.current_target = (self.current_target + 1) % len(self.patrol_route)
            print("Я досяг цілі ", self.rect.x, self.rect.y)
            
        # Після руху оновлюємо зображення
        
        # Після руху оновлюємо зображення в залежності від напрямку

class EnemyFactory(): 
    def create_enemy(self, enemy_type, x, y, enemy: EnemyTypeA):
        if enemy_type == 'A':
            enemy.rect.x = x
            enemy.rect.y = y
            return EnemyTypeA(enemy.rect.x, enemy.rect.y, enemy.damage, enemy.speed, enemy.patrol_route, enemy.enemy_image, enemy.size)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")

class Shoot():  # Класс для шмаляння
    pass


game = Game(1, 2, 3, 4)
game.start()

game_back_ground = NotMoving("background.jpg", 0, 0, (1200, 700))

player = Player(100, 100, 100, 0, 5, (50, 90))

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

patrol_route = [
    (100, 100, "up"),  # Початкова точка
    (300, 100, "right"),  # Перша ціль (рух праворуч)
    (300, 180, "down"),  # Друга ціль (рух вниз)
    (800, 200, "right"),  # Третя ціль (рух ліворуч)
    (800, 455, "down"),   # Повернення до початкової точки
    (1000, 455, "right"), 
    (1000, 650, "down"), 
    (550, 650, "left"),
    (550, 300, "up") ,
    (300, 300, "left") ,
    (300, 100, "up") ,
    (100, 100, "left") ,
    (100, 300, "down") 
    
]
enemy_creator = EnemyFactory()
enemy_type_A = EnemyTypeA(100, 300, 4, 5, patrol_route , "player.png", (50, 90))
enemy1 = enemy_creator.create_enemy('A', 100, 300, enemy_type_A)
enemy2 = enemy_creator.create_enemy('A', 100, 100, enemy_type_A)


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
    enemy1.move()
    enemy2.reset()
    enemy2.move()
    
    
    game.update()