from pygame import *
width = 1200
height = 700
window = display.set_mode((width, height))
font.init()
font1 = font.Font(None, 50)
class NotMoving(sprite.Sprite):  
    def __init__(self, b_image, x, y, size):
        super().__init__()
        self.image = transform.scale(image.load(b_image), size)    
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class TextArea:
    def __init__(self, x=0, y=0, width=10, height=10, color=(255, 255, 255)):
        self.rect = Rect(x, y, width, height)
        self.fill_color = color
        self.text = ""
        self.image = None 

    def set_text(self, text, text_color=(255, 255, 255)):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        self.text = text
        self.image = font1.render(self.text, True, text_color)

    def draw(self, window):
        draw.rect(window, self.fill_color, self.rect)
        if self.image:
            window.blit(self.image, (self.rect.x, self.rect.y))
