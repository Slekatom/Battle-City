from pygame import * #Імпорти
import patrol_route
import notmoving
import enemy
import shoot
import moving_strategies

width = 1200
height = 700
window = display.set_mode((width, height))
display.set_caption("Battle City")
clock = time.Clock()
FPS = 60
mixer.init()

class Game: #Клас головного контрллера
    def __init__(self):
        self.game = False
        self.intro = True
        self.ending = False
        self.bullet_timer = 100
        self.volume = 1
        self.proc = 100
    def mp3player(self, music, volume):#Програвач музики
        mixer.init()
        mixer.music.load(music)
        mixer.music.set_volume(volume)
        mixer.music.play(1)
    def start(self):#початок ігрового циклу
        self.game = True
        self.mp3player("pictures_and_sounds/War.mp3", self.volume)
    def end(self):#кіцень ігрового циклу
        self.game = False
    def stop_all(self, player, enemies, bullets, bullets_enemy):#зупинення всіх об'єктів
        player.speed = 0
        for i in enemies:
            i.speed = 0
        for i in bullets:
            i.speed = 0
        for i in bullets_enemy:
            i.speed = 0
    
    def player_shoot(self): #стрільба гравця в циклі
        bullet = shoot.Shoot(player.rect.centerx, player.rect.centery, player.diraction)
        bullets.add(bullet)
        self.mp3player("pictures_and_sounds/bach.mp3", self.volume)
        
    def reseting(self): #поява спрайтів на екран у циклі
        game_back_ground.reset()
        
        player.reset()
        player.move(walls)
          
        for wall in walls:
            wall.reset()
        
        for i in enemies:
            i.reset()
            i.move()
            if self.bullet_timer == 0:# затримка при стрільбі ворога
                bullet = shoot.Shoot(i.rect.centerx, i.rect.centery, i.diraction)
                bullets_enemy.add(bullet)
                self.bullet_timer = 100 
            else:
                self.bullet_timer -= 1

        bullets.update()  
        bullets.draw(window)
        bullets_enemy.update()  
        bullets_enemy.draw(window)
        pause.reset()
        menu_bar.reset()
        continue_b.reset()  
        volum_plus.reset()
        volume_minus.reset()
        volume_proc.set_text(str(self.proc)+"%", (250, 250, 250))
        volume_proc.draw(window)
        points.set_text("Очок набито: "+str(player.score), (250, 250, 250))
        points.draw(window)
    def buttons(self):   
        if e.type == MOUSEBUTTONDOWN: #при нажиманні на кнопки
            x, y = e.pos
            if pause.rect.collidepoint(x, y):
                self.stop_all(player, enemies, bullets, bullets_enemy)
                menu_bar.rect.x = 700 #повертання на позицію. яку бачить гравець
                menu_bar.rect.y = 0
                continue_b.rect.x = 900
                continue_b.rect.y = 500
                volume_minus.rect.x = 750
                volume_minus.rect.y = 350
                volum_plus.rect.x = 1050
                volum_plus.rect.y = 350
                volume_proc.rect.x = 890
                volume_proc.rect.y = 350
                
            if continue_b.rect.collidepoint(x, y):
                self.stop_all(player, enemies, bullets, bullets_enemy)   
                menu_bar.rect.x = 2000 #повертання на позицію. яку бачить гравець
                menu_bar.rect.y = 0
                continue_b.rect.x = 2000
                continue_b.rect.y = 500
                volume_minus.rect.x = 2000
                volume_minus.rect.y = 500
                volum_plus.rect.y = 2000
                volum_plus.rect.x = 2000
                volume_proc.rect.x = 2000
                volume_proc.rect.y = 2000
                player.speed = 5
                for i in enemies:
                    i.speed = 2
                for i in bullets:
                    i.speed = 50
                for i in bullets_enemy:
                    i.speed = 50
            if volume_minus.rect.collidepoint(x, y):
                if self.volume > 0:  
                    self.volume -= 0.05
                    self.volume = max(0, self.volume)  
                    self.proc = int(self.volume * 100)  
                    mixer.music.set_volume(self.volume) 
            if volum_plus.rect.collidepoint(x, y):
                if self.volume < 1: 
                    self.volume += 0.05
                    self.volume = min(1, self.volume) 
                    self.proc = int(self.volume * 100)  
                    mixer.music.set_volume(self.volume)
            if retry.rect.collidepoint(x, y): #спробувати ще раз
                for i in enemies:
                    i.moved_home()
                    i.speed = 2
                for i in bullets:
                    i.speed = 50
                for i in bullets_enemy:
                    i.speed = 50
                player.rect.x = 1100
                player.rect.y = 600
                fail.rect.x = 2000
                retry.rect.x = 2000
                player.speed = 5
                player.score = 0
    def bullets_collision(self):#перевірка для колізії
        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    player.add_score(100)                
                    enemy.moved_home()  
                    enemy.speed += 0.25
                    mixer.init()
                    mixer.music.load('pictures_and_sounds/babach.mp3')
                    mixer.music.set_volume(self.volume)
                    mixer.music.play(0)
                    explosion = notmoving.Picture("pictures_and_sounds/Buch.png", bullet.rect.x, bullet.rect.y, (100, 150))
                    explosion.reset()
                    bullet.kill()
            for wall in walls:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()
        for bullet2 in bullets_enemy:  
            for wall in walls:
                if bullet2.rect.colliderect(wall.rect):
                    bullet2.kill()
        end_hammer.check_tank_colision(player, enemies, game)
        end_hammer.check_tank_colision(player, bullets_enemy, game)   
    def update(self):
        clock.tick(FPS)
        display.update()        




class Player(enemy.Enity, sprite.Sprite): #клас гравця
    def __init__(self, x, y, hp, score, speed, size):
        sprite.Sprite.__init__(self)  
        self.hp = hp  
        self.score = score   
        self.original_image = transform.scale(image.load("pictures_and_sounds/player.png"), size)  
        self.image = self.original_image.copy() 
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.diraction = None
        self.size = size

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
        prev_pos = self.rect.copy()
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

class Colision(): #перевірка колізії для гравця
    def check_tank_colision(self, player: Player, target_list, game: Game):
        if sprite.spritecollide(player, target_list, False):
            game.stop_all(player, enemies, bullets, bullets_enemy)
            if menu_bar.rect.x != 700:
                mixer.init()
                mixer.music.load('pictures_and_sounds/babach.mp3')
                mixer.music.set_volume(game.volume)
                mixer.music.play(0)
                explosion = notmoving.Picture("pictures_and_sounds/Buch.png", player.rect.x, player.rect.y, (100, 150))
                explosion.reset()
                for bullet in bullets:
                    bullet.speed = 0
                    bullet.kill()
            for bullet in bullets:  
                bullet.kill()
            game.ending = True
            game.stop_all(player, enemies, bullets, bullets_enemy)
            retry.rect.x = 1000
            fail.rect.x = 0
            fail.reset()
            retry.reset()
            return True
        else:
            return False
#ініціалізація спрайтів       
game = Game()


game_back_ground = notmoving.NotMoving("pictures_and_sounds/background.jpg", 0, 0, (1200, 700))

move_stratagyA = moving_strategies.MovingStrategyA()
move_stratagyB = moving_strategies.MovingStrategyB()

player = Player(1100, 600, 100, 0, 5, (50, 90))
player.set_strategy(move_stratagyB)

wall1 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 200, 600, (50, 250))
wall2 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 0, 450, (300, 50))
wall3 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 150, 450-200, (50, 200))
wall4 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 450, 400, (50, 300))
wall5 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 650, 550, (250, 50))
wall6 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 650, 550-300, (50, 300))
wall7 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 550-100, 250, (200, 50))
wall8 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 550-100, 0, (50, 150))
wall9 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 950, 0, (50, 150))
wall10 = notmoving.NotMoving("pictures_and_sounds/wall.jpg", 1200-300, 350, (300, 50))

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

enemy_type_A = enemy.EnemyTypeA(100, 300, 100, 300, 4, 2 , patrol_route.patrol_route1, "pictures_and_sounds/player.png", (50, 90))
enemy1 = enemy_creator.create_enemy('A', 100, 300, patrol_route.patrol_route1, enemy_type_A, 100, 300)
enemy2 = enemy_creator.create_enemy('A', 50, 600, patrol_route.patrol_route2, enemy_type_A, 50, 600)
enemy3 = enemy_creator.create_enemy('A', 1100, 50, patrol_route.patrol_route3, enemy_type_A, 1100, 50)


enemy1.set_movement_strategy(move_stratagyA)     
enemy2.set_movement_strategy(move_stratagyA)
enemy3.set_movement_strategy(move_stratagyA)
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)


end_hammer = Colision()

bullets = sprite.Group()
bullets_enemy = sprite.Group()

pause = notmoving.Picture("pictures_and_sounds/pause.png", 1150, 0, (50, 50))
continue_b = notmoving.Picture("pictures_and_sounds/cont.png", 2000, 0, (100, 100))
retry = notmoving.Picture("pictures_and_sounds/retry.png", 2000, 620, (200, 80))
menu_bar = notmoving.Picture("pictures_and_sounds/Menu_bar.png", 2000, 0, (500, 700))
volum_plus = notmoving.Picture("pictures_and_sounds/+.png", 2000, 0, (100, 100))
volume_minus = notmoving.Picture("pictures_and_sounds/-.png", 2000, 0, (100, 100))
volume_proc = notmoving.TextArea(2000, 2000, 90, 40, (0, 0, 0))
fail = notmoving.Picture("pictures_and_sounds/Fail_picture.png", 0, 0, (1200, 700))
points = notmoving.TextArea(0, 0, 0, 0, (0, 0, 0))
beg_scene = notmoving.NotMoving("pictures_and_sounds/Tanks_fon.jpg", 0, 0, (1200, 700))
game.mp3player("pictures_and_sounds/War.mp3", game.volume)
while game.intro != False:#початок передумови
    for e in event.get():
        if e.type == QUIT:                    
            game.intro = False
        if e.type == KEYDOWN:
            game.intro = False
            game.game = True
    beg_scene.reset()
    
    game.update()
    
        
while game.game == True:#початок самої гри

    for e in event.get():
        if e.type == QUIT:
            game.end()
        if e.type == KEYDOWN and e.key == K_SPACE:
            game.player_shoot()       
    game.reseting()
    game.buttons()
    game.bullets_collision()


    
    game.update()
