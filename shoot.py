from pygame import *
width = 1200
height = 700
class Shoot(sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = Surface((5, 5))
        self.image.fill((148, 98, 18))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 50
        self.direction = direction

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        if self.rect.right < 0 or self.rect.left > width or \
           self.rect.bottom < 0 or self.rect.top > height:
            self.kill()