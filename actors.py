import pygame

banana_sprite = pygame.image.load('resources/sprites/jungle_banana_icon.png')
pad_sprite = pygame.image.load('resources/sprites/leaf.png')
banana_sprite = pygame.transform.scale(banana_sprite, (100, 100))
monkeyright_sprite = pygame.image.load('resources/sprites/Mona/MonaDer.png')
monkeyright_sprite = pygame.transform.scale(monkeyright_sprite, (100, 100))


class Banana:

    def __init__(self, posx, posy):
        self.sprite = banana_sprite
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx, posy, 100, 100)


class Monkey:

    def __init__(self, posx, posy):
        self.direction = "up"
        self.sprite = monkeyright_sprite
        self.score = 0
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx + 10, posy + 35, 20, 20)
        self.move = True

    def step(self, num):
        print(self.move)
        if self.move:
            if self.direction == "up":
                self.posy -= num*100
            if self.direction == "down":
                self.posy += num*100
            if self.direction == "right":
                self.posx += num*100
            elif self.direction == "left":
                self.posx -= num*100

    def turn(self, direction):
        self.direction = direction
        if direction == "right":
            self.sprite = monkeyright_sprite
        elif direction == "left":
            self.sprite = monkeyright_sprite
        elif direction == "up":
            self.sprite = monkeyright_sprite
        elif direction == "down":
            self.sprite = monkeyright_sprite


class Pad:
    def __init__(self, posx, posy):
        self.sprite = pad_sprite
        self.posx = posx
        self.posy = posy
        self.dir = "right"
        self.hitbox = (posx, posy, 100, 100)
        self.mounted = False

    def movingpad(self):
        if self.dir == "right":
            if self.posx < 700:
                self.posx += 100
            else:
                self.dir = "left"
        elif self.dir == "left":
            if self.posx > 99:
                self.posx -= 100
            else:
                self.dir = "right"
