from pygame import *
width = 1200
height = 700
window = display.set_mode((width, height))
class NotMoving(sprite.Sprite):  
    def __init__(self, b_image, x, y, size):
        super().__init__()
        self.image = transform.scale(image.load(b_image), size)    
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
