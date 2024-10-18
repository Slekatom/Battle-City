import pygame
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, explosion_frames):
        super().__init__()
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_rate = 5  # Скільки циклів має пройти до зміни кадру
        self.current_frame = 0
    
    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.frame_rate:
            self.current_frame = 0
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()