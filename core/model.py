import math
import pygame
import math


class Cable:
    def __init__(self, cordenates, current_player):
        self.cordenates = cordenates
        self.color = (255, 255, 255) if current_player else (0, 0, 0)

    def set_color(self, color):
        self.color = color
    
    def draw(self, surface):
        self.cable = pygame.draw.line(surface, self.color, self.cordenates[0], self.cordenates[1], 2)



class Circle:
    def __init__(self, x, y, indexes):
        self.indexes = indexes
        self.x = x
        self.y = y
        self.color = (11, 46, 89)
        self.radius = 10
        self.clicked = False

    def is_point_in(self, cordenates):
        return self.circle.collidepoint(cordenates)

    def set_color(self, color):
        self.color = color

    def draw(self, screen):
        self.circle = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
    
    def get_cordenates(self):
        return (self.x, self.y)
    
    def get_indexes(self):
        return self.indexes

class House(pygame.sprite.Sprite):
    def __init__(self, cordenates, status=1):
        super().__init__()
        self.image = pygame.image.load("assets/house.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = cordenates[0]
        self.rect.y = cordenates[1]
        self.status = status