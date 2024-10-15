from pygame import sprite
import moving_strategies_class
import enemy_class
import player as sprites
import patrol_route
import notmoving_class

def create_movement_strategies():
    move_stratagyA = moving_strategies_class.MovingStrategyA()
    move_stratagyB = moving_strategies_class.MovingStrategyB()
    return move_stratagyA, move_stratagyB

def create_player(strategy):
    player = sprites.Player(1100, 600, 100, 0, 5, (50, 90))
    player.set_strategy(strategy)
    return player

def create_enemies(strategy):
    enemy_creator = enemy_class.EnemyFactory()
    enemy_type = enemy_class.Enemy(100, 300, 100, 300, 4, 2, patrol_route.patrol_route1, "pictures_and_sounds/player.png", (50, 90))

    enemy1 = enemy_creator.create_enemy('A', 100, 300, patrol_route.patrol_route1, enemy_type, 100, 300)
    enemy2 = enemy_creator.create_enemy('A', 50, 600, patrol_route.patrol_route2, enemy_type, 50, 600)
    enemy3 = enemy_creator.create_enemy('A', 1100, 50, patrol_route.patrol_route3, enemy_type, 1100, 50)

    enemy1.set_movement_strategy(strategy)
    enemy2.set_movement_strategy(strategy)
    enemy3.set_movement_strategy(strategy)

    enemies = sprite.Group()
    enemies.add(enemy1, enemy2, enemy3)
    
    return enemies

def create_interface_elements():
    pause = notmoving_class.Picture("pictures_and_sounds/pause.png", 1150, 0, (50, 50))
    continue_b = notmoving_class.Picture("pictures_and_sounds/cont.png", 2000, 0, (100, 100))
    retry = notmoving_class.Picture("pictures_and_sounds/retry.png", 2000, 620, (200, 80))
    menu_bar = notmoving_class.Picture("pictures_and_sounds/Menu_bar.png", 2000, 0, (500, 700))
    volum_plus = notmoving_class.Picture("pictures_and_sounds/+.png", 2000, 0, (100, 100))
    volume_minus = notmoving_class.Picture("pictures_and_sounds/-.png", 2000, 0, (100, 100))
    volume_proc = notmoving_class.TextArea(2000, 2000, 90, 40, (0, 0, 0))
    fail = notmoving_class.Picture("pictures_and_sounds/Fail_picture.png", 0, 0, (1200, 700))
    points = notmoving_class.TextArea(0, 0, 0, 0, (0, 0, 0))
    beg_scene = notmoving_class.NotMoving("pictures_and_sounds/Tanks_fon.jpg", 0, 0, (1200, 700))
    game_back_ground = notmoving_class.NotMoving("pictures_and_sounds/background.jpg", 0, 0, (1200, 700))
    return pause, continue_b, retry, menu_bar, volum_plus, volume_minus, volume_proc, fail, points, beg_scene, game_back_ground

    