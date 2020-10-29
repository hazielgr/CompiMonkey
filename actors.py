import pygame

banana_sprite = pygame.image.load('resources/sprites/jungle_banana_icon.png')
monkeyhead_sprite = pygame.image.load('resources/sprites/monkey_head_icon.png')

class Banana:

    def __init__(self, posx, posy):
        self.sprite = banana_sprite
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx + 7, posy + 5, 170, 120)



class Monkey:

    def __init__(self, posx, posy):
        self.sprite = monkeyhead_sprite
        self.score = 0
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx + 10, posy + 35, 375, 305)