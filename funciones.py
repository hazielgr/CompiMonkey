import pygame, sys, math, threading
import config
from main import checkCollision

GREEN = (41, 171, 13)
DESERT = (235, 226, 209)


def step(num):
    lvlActors = config.lvlActors
    displaySurf = config.displaySurf
    contador = 1
    step = 1
    # loop que hace al mono moverse la cantidad de veces indicadas por el usuario
    while contador <= num:
        if lvlActors[8][2] == "desert":
            pygame.draw.rect(displaySurf, DESERT, (lvlActors[0].posx, lvlActors[0].posy, 99, 99))
        else:
            pygame.draw.rect(displaySurf, GREEN, (lvlActors[0].posx, lvlActors[0].posy, 99, 99))
        # cambia las posiciones posx y posy del mono
        lvlActors[0].step(step)
        # actualiza el hitbox y dibuja el mono en sus nuevas posiciones
        lvlActors[0].hitbox = (lvlActors[0].posx, lvlActors[0].posy, 100, 100)
        displaySurf.blit(lvlActors[0].sprite, (lvlActors[0].posx, lvlActors[0].posy))
        # se cambia el valor del booleano por efectos de colisiones
        lvlActors[0].move = True
        contador += 1
        pygame.time.wait(50)
        checkCollision(config.lvlActors)
        if lvlActors[0].move == False:
            contador = num
        pygame.display.update()