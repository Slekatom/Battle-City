from pygame import * #Імпорти
import patrol_route
import notmoving_class
import enemy_class
import bullet_class
import moving_strategies_class
import player as player_class
import window as settings
import map
import game_objects as go
import explosion_class
mixer.init()
class Game: #Клас головного контрллера
    def __init__(self) -> None:
        self.game = False
        self.intro = True
        self.ending = False
        self.bullet_timer = 100
        self.volume = 0.1
        self.proc = 10
        self.replay_opened = False
    def mp3player(self, music, volume):#Програвач музики
        mixer.init()
        mixer.music.load(music)
        mixer.music.set_volume(volume)
        mixer.music.play(1)
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
        bullet = bullet_class.Bullet(player.rect.centerx, player.rect.centery, player.diraction)
        bullets.add(bullet)
        self.mp3player("pictures_and_sounds/bach.mp3", self.volume)
        
    def reseting(self): #поява спрайтів на екран у циклі
        game_back_ground.reset()
               
        player.reset(settings.window)
        player.move(map.walls)
          
        for wall in map.walls:
            wall.reset()
        
        for i in enemies:
            i.reset()
            i.move()
            if self.bullet_timer == 0:# затримка при стрільбі ворога
                bullet = bullet_class.Bullet(i.rect.centerx, i.rect.centery, i.diraction)
                bullets_enemy.add(bullet)
                self.bullet_timer = 100 
            else:
                self.bullet_timer -= 1

        bullets.update()  
        bullets.draw(settings.window)
        bullets_enemy.update()  
        bullets_enemy.draw(settings.window)
        explosions.update()  # Оновлюємо всі вибухи
        explosions.draw(settings.window)
        if self.replay_opened == False:
            pause.reset()
        menu_bar.reset()
        continue_b.reset()  
        volum_plus.reset()
        volume_minus.reset()
        volume_proc.set_text(str(self.proc)+"%", (250, 250, 250))
        volume_proc.draw(settings.window)
        points.set_text("Очок набито: "+str(player.score), (250, 250, 250))
        points.draw(settings.window)
    def buttons(self, e):      
        if e.type == MOUSEBUTTONDOWN:  # при натисканні на кнопки
            x, y = e.pos
            if pause.rect.collidepoint(x, y):
                if self.replay_opened == False:
                    self.stop_all(player, enemies, bullets, bullets_enemy)
                    menu_bar.rect.x = 700  # повернення на позицію, яку бачить гравець
                    menu_bar.rect.y = 0
                    continue_b.rect.x = 900
                    continue_b.rect.y = 500
                    volume_minus.rect.x = 750
                    volume_minus.rect.y = 350
                    volum_plus.rect.x = 1050
                    volum_plus.rect.y = 350
                    volume_proc.rect.x = 890
                    volume_proc.rect.y = 350
                    player.allow_rotate = False

            if continue_b.rect.collidepoint(x, y):
                self.stop_all(player, enemies, bullets, bullets_enemy)   
                menu_bar.rect.x = 2000  # повернення на позицію, яку бачить гравець
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
                player.allow_rotate = True
                for i in bullets:
                    i.allowed_shooting = True
                for j in bullets_enemy:
                    j.allowed_shooting = True
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
                self.replay_opened = False
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
                player.allow_rotate = True
    def bullets_collision(self):#перевірка для колізії
        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    player.add_score(100)                
                    enemy.moved_home()  
                    enemy.speed += 0.25
                    game.mp3player("pictures_and_sounds/babach.mp3", self.volume)
                    explosion = explosion_class.Explosion(bullet.rect.x, bullet.rect.y, exp)  # Використовуйте кадри анімації
                    explosions.add(explosion)
                    bullet.kill()
                    self.replay_opened == True
                    for i in bullets:
                        i.allowed_shooting = False
                    for j in bullets_enemy:
                        j.allowed_shooting = False
            for wall in map.walls:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()
        for bullet2 in bullets_enemy:  
            for wall in map.walls:
                if bullet2.rect.colliderect(wall.rect):
                    bullet2.kill()
        end_hammer.check_tank_colision(player, enemies)
        end_hammer.check_tank_colision(player, bullets_enemy)   
    def update(self):
        settings.clock.tick(settings.FPS)
        display.update()   
    def run(self):
        # Ігровий цикл
        while self.intro:  # Початок передумови
            for e in event.get():
                if e.type == QUIT:
                    self.intro = False
                if e.type == KEYDOWN:
                    self.intro = False
                    self.game = True
            beg_scene.reset()
            self.update()

        while self.game:  # Основна гра
            for e in event.get():
                if e.type == QUIT:
                    self.end()
                if e.type == KEYDOWN and e.key == K_SPACE:
                    self.player_shoot()

            self.reseting()
            self.buttons(e)
            self.bullets_collision()
            self.update()

class Collision(): #перевірка колізії для гравця
    def check_tank_colision(self, player: player_class.Player, target_list: list) -> bool:
        if sprite.spritecollide(player, target_list, False):
            game.stop_all(player, enemies, bullets, bullets_enemy)
            if menu_bar.rect.x != 700:
                explosion = explosion_class.Explosion(player.rect.x, player.rect.y, exp)
                explosions.add(explosion)
                game.replay_opened = True
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
            player.allow_rotate = False
            for i in bullets:
                i.allowed_shooting = False
            for j in bullets_enemy:
                j.allowed_shooting = False
            return True
        else:
            return False  
#ініціалізація спрайтів       
game = Game()

end_hammer = Collision()

bullets = sprite.Group()
bullets_enemy = sprite.Group()

move_stratagyA, move_stratagyB = go.create_movement_strategies()

player = go.create_player(move_stratagyB)

enemies = go.create_enemies(move_stratagyA)

pause, continue_b, retry, menu_bar, volum_plus, volume_minus, volume_proc, fail, points, beg_scene, game_back_ground = go.create_interface_elements()

exp, explosions = go.create_explosion_animation()
if __name__ == "__main__":
    game = Game()
    game.mp3player("pictures_and_sounds/War.mp3", game.volume)
    game.run()