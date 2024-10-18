from pygame import sprite, transform, image
import entity
class Player(sprite.Sprite, entity.Entity): 
    def __init__(self, x, y, hp, score, speed, size):
        super().__init__()  # Ініціалізація через super
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
        self.strategy = None
        self.allow_rotate = True

    def reset(self, window):
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
        return not sprite.spritecollide(self, walls, False)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def move(self, walls):
        prev_pos = self.rect.copy()
        if self.strategy:
            self.strategy.move(self)
        if not self.allowed_move(walls):
            self.rect = prev_pos
        if self.allow_rotate == True:
            self.rotate_image()

    def take_damage(self, amount, game):
        self.hp -= amount
        if self.hp <= 0:
            game.end()

    def add_score(self, points):
        self.score += points