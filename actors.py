import pygame
import time
import config

monkeyright_sprite = pygame.image.load('resources/sprites/Mona/MonaDer.png')
monkeyright_sprite = pygame.transform.scale(monkeyright_sprite, (100, 100))
rat_sprite = pygame.image.load('resources/sprites/rat.png')
#rat_sprite = pygame.transform.scale(rat_sprite, (100, 100))

banana_sprite = pygame.image.load('resources/sprites/jungle_banana_icon.png')
pad_sprite = pygame.image.load('resources/sprites/leaf.png')
banana_sprite = pygame.transform.scale(banana_sprite, (100, 100))
match_sprite = pygame.image.load('resources/sprites/match.png')
match_sprite = pygame.transform.scale(match_sprite, (100, 100))
monkeyright_sprite = pygame.image.load('resources/sprites/Mona/MonaDer.png')
monkeyright_sprite = pygame.transform.scale(monkeyright_sprite, (100, 100))
coco_sprite = pygame.image.load('resources/sprites/coco/cocoL.png')
coco_sprite = pygame.transform.scale(coco_sprite, (300, 100))


class Banana:

    def __init__(self, posx, posy):
        self.sprite = banana_sprite
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx, posy, 100, 100)

class Match:

    def __init__(self, posx, posy):
        self.sprite = match_sprite
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx, posy, 100, 100)
        self.holded = False


class Monkey:
    def __init__(self, posx, posy, sprite):
        self.direction = "up"
        self.health = 100
        self.id = sprite
        #pa saber si tiene match o no
        self.mounted = False
        self.holding= False
        if self.id == "Rat":
            self.sprite = rat_sprite
        else:
            self.sprite = monkeyright_sprite
        self.score = 0
        self.posx = posx
        self.posy = posy
        self.hitbox = (posx + 10, posy + 35, 20, 20)
        self.move = True

    def step(self, num):
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
        if self.id == "Monkey":
            if direction == "right":
                self.sprite = monkeyright_sprite
            elif direction == "left":
                self.sprite = monkeyright_sprite
            elif direction == "up":
                self.sprite = monkeyright_sprite
            elif direction == "down":
                self.sprite = monkeyright_sprite
        elif self.id == "Rat":
            self.sprite = rat_sprite

    def grab(self):
        lvlActors = config.lvlActors
        if config.currentlvl == 4 or config.currentlvl == 5:
            index = 4
            for item in range(len(config.lvlActors[index])):
                if self.posy < lvlActors[index][item].hitbox[1] + lvlActors[index][item].hitbox[3] and self.posy + \
                        self.hitbox[3] > lvlActors[index][item].hitbox[1]:
                    if self.posx + self.hitbox[2] > lvlActors[index][item].hitbox[0] and self.posx < \
                            lvlActors[index][item].hitbox[0] + lvlActors[index][item].hitbox[2]:
                        self.holding = True

        #cambiar sprite

    def drop(self):
        lvlActors = config.lvlActors
        if config.currentlvl == 4 or config.currentlvl == 5:
            if self.posy < lvlActors[-2][0].hitbox[1] + lvlActors[-2][0].hitbox[3] and self.posy + \
                    self.hitbox[3] > lvlActors[-2][0].hitbox[1]:
                if self.posx + self.hitbox[2] > lvlActors[-2][0].hitbox[0] and self.posx < \
                        lvlActors[-2][0].hitbox[0] + lvlActors[-2][0].hitbox[2]:
                    if self.holding:
                        config.lvlActors[-2][1] += 1
                        config.lvlActors[2] += 1
                        config.lvlActors[0].holding = False

        # cambiar sprite


class Coco:
    def __init__(self, posx, posy):
        self.sprite = coco_sprite
        self.posx = posx
        self.posy = posy
        #Centro del cuerpo
        self.posxC = posx+100
        self.posyC = posy+100
        self.dir = "left"
        self.hitbox = (posx, posy, 300, 100)
        self.mounted = False

    def rotateCoco (self, monkeX, monkeY):
        if monkeX<self.posxC and monkeY <self.posyC:
            #mono arriba a la izq
            self.dir = "up"
        elif monkeX>self.posxC and monkeY <self.posyC:
            #mono arriba a la der
            self.dir = "up"
        elif monkeX==self.posxC and monkeY <self.posyC:
            #mono arriba
            self.dir = "up"
        elif monkeX<self.posxC and monkeY == self.posyC:
            #mono a la izq
            self.dir = "left"
        elif monkeX>self.posxC and monkeY ==self.posyC:
            #mono a la der
            self.dir = "right"
        elif monkeX<self.posxC and monkeY > self.posyC:
            #mono abajo a la izq
            self.dir = "down"
        elif monkeX>self.posxC and monkeY >self.posyC:
            #mono abajo a la der
            self.dir = "down"
        elif monkeX == self.posxC and monkeY > self.posyC:
            # mono abajo
            self.dir = "down"
        else:
            #mono en el centro del mop
            self.dir = self.dir
    def rotateDir (self):
        if self.dir == "left" or self == "right":
            self.posx -=100
            self.posy +=100
            self.hitbox = (self.posx,self.posy, 300, 100)
        elif self.dir =="up" or self.dir == "down":
            self.posx +=100
            self.posy -=100
            self.hitbox = (self.posx,self.posy, 100, 300)
            self.sprite = pygame.transform.scale(coco_sprite, (100, 300))

class Pad:
    def __init__(self, posx, posy):
        self.sprite = pad_sprite
        self.posx = posx
        self.posy = posy
        self.dir = "right"
        self.hitbox = (posx, posy, 100, 100)
        self.mounted = False

    def movingPad(self, num):
        if self.dir == "right":
            if self.posx < 700:
                self.posx += num*100
                self.hitbox = (self.posx, self.posy, 100, 100)
            else:
                self.dir = "left"
                self.movingPad(num)
        elif self.dir == "left":
            if self.posx > 99:
                self.posx -= num*100
                self.hitbox = (self.posx, self.posy, 100, 100)
            else:
                self.dir = "right"
                self.movingPad(num)

    def changeDirPad(self,dir):
        if dir == "right":
            self.dir = dir
        elif dir == "left":
            self.dir = dir

class beaver:
    def __init__ (self,posx, posy, dir):
        self.sprite = pad_sprite
        self.posx = posx
        self.posy = posy
        self.dir = dir
        self.hitbox = (posx, posy, 100, 100)
        self.mounted = False

    def movingPad(self, num):
        if self.dir == "right":
            self.posx += num*100
            self.hitbox = (self.posx, self.posy, 100, 100)
        elif self.dir == "left":
            self.posx -= num*100
            self.hitbox = (self.posx, self.posy, 100, 100)
        elif self.dir == "up":
            self.posy -= num*100
            self.hitbox = (self.posx, self.posy, 100, 100)
        elif self.dir == "down":
            self.posy += num*100
            self.hitbox = (self.posx, self.posy, 100, 100)



