from abc import ABC, abstractmethod
class Entity(ABC): # Абстрактний клас забов'язує прилеглі класи рухатися
    @abstractmethod 
    def move(self):
        pass