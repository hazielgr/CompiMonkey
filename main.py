import pygame, sys, math, threading
from pygame.locals import *
from levels import level1
from lvlManager import *
from button import *
from interprete.interpreter import *
import funciones
import config

## CONSTANTES ##

DISPLAYWIDTH = 1600
DISPLAYHEIGHT = 900
FPS = 30
TEXTHEIGHT = 20
STARTX = 800
STARTY = 0
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

## COLORES ##

#      R    G    B
GRAY = (68, 68, 68)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (41, 171, 13)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COMBLUE = (233, 232, 255)
CREAM = (248, 242, 218)
DARKCREAM = (255, 242, 180)
BGCOLOR = GRAY
TEXTCOLOR = WHITE

# icon = pygame.image.load('resources/sprites/monkey_head_icon.png')
##monkeyhead_sprite = pygame.image.load('resources/sprites/monkey_head_icon.png')
banana_sprite = pygame.image.load('resources/sprites/jungle_banana_icon.png')
match_sprite = pygame.image.load('resources/sprites/match.png')
match_sprite = pygame.image.load('resources/sprites/match.png')

buttons = []
buttonx = 0
buttony = 850


def runGame():
    global FPSCLOCK, displaySurf, lvlActors, currentlvl
    move_monkey = False

    lvlActors = []
    grid = []
    changelvl = 0
    currentlvl = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    deltaTime = FPSCLOCK.tick(FPS) / 1000
    running = True

    windowWidth = 1600
    windowHeight = 900
    displaySurf = pygame.display.set_mode((windowWidth, windowHeight), RESIZABLE)

    lineNumber = 0
    newChar = ''
    typeChar = False
    textString = ''

    mainList = []  # Contiene cada linea que se escribio en strings separados por linea dentro de la lista
    mainList.append(textString)
    deleteKey = False  # booleano que revisa si se quiere borrar
    returnKey = False  # booleano que revisa si se quiere cambiar de linea

    # buttons
    lvl1_button = Button(1, CREAM, buttonx, buttony, 100, 50, "lvl1")
    lvl2_button = Button(2, CREAM, buttonx + 110, buttony, 100, 50, "lvl2")
    lvl3_button = Button(3, CREAM, buttonx + 220, buttony, 100, 50, "lvl3")
    lvl4_button = Button(4, CREAM, buttonx + 330, buttony, 100, 50, "lvl4")
    lvl5_button = Button(5, CREAM, buttonx + 440, buttony, 100, 50, "lvl5")
    lvl6_button = Button(6, CREAM, buttonx + 550, buttony, 100, 50, "lvl6")

    run_button = Button(10, GREEN, buttonx + 1200, buttony, 100, 50, "RUN")
    erase_button = Button(11, RED, buttonx + 1310, buttony, 100, 50, "ERASE")

    buttons = [lvl1_button, lvl2_button, lvl3_button, lvl4_button, lvl5_button, lvl6_button, run_button, erase_button]

    insertPoint = 0
    camerax = 0
    cameray = 0

    mouseClicked = False
    mouseX = 0
    mouseY = 0

    # displaySurf.fill(BGCOLOR)

    pygame.display.update()

    pygame.display.set_caption('CompiMonkey')
    ##pygame.display.set_icon(icon)

    mainFont = pygame.font.SysFont('Lucida Console', TEXTHEIGHT)

    cursorRect = getCursorRect(STARTX, STARTY + (TEXTHEIGHT + (TEXTHEIGHT / 4)), mainFont, camerax, cameray)

    # El loop del juego detecta el input del usuario y lo muestra en pantalla
    # coloca el cursor en la pantalla y ajusta la camara de ser necesario

    while running:

        camerax, cameray = adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray,
                                        windowWidth, windowHeight)

        newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked, changelvl, mainList = getInput(
            windowWidth, windowHeight, buttons, changelvl, mainList, lvlActors, deltaTime, displaySurf)

        mainList, lineNumber, insertPoint, cursorRect = displayText(mainFont, newChar, typeChar, mainList, deleteKey,
                                                                    returnKey, lineNumber, insertPoint, directionKey,
                                                                    camerax, cameray, cursorRect, windowWidth,
                                                                    windowHeight, displaySurf, mouseClicked, mouseX,
                                                                    mouseY)

        displayInfo(insertPoint, mainFont, cursorRect, camerax, windowWidth, windowHeight, displaySurf)

        # level manager
        if currentlvl != changelvl:
            lvlActors = levelManager(changelvl)
            currentlvl = changelvl
            changeConfigList(lvlActors, displaySurf, currentlvl)

        blitLevel(lvlActors, displaySurf, grid)

        # dibuja los botones
        for i in range(len(buttons)):
            buttons[i].draw(displaySurf)

        checkCollision(lvlActors, currentlvl)

        score(displaySurf, config.lvlActors)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# FUNCIONES QUE VA A UTILIZAR EL INTERPRETE
##########

def step(num, lvlActors, displaySurf, currentlvl):
    contador = 1
    step = 1
    # loop que hace al mono moverse la cantidad de veces indicadas por el usuario
    while contador <= num:
        if (currentlvl == 4 or currentlvl == 5):
            pygame.draw.rect(displaySurf, DESERT, (lvlActors[0].posx, lvlActors[0].posy, 99, 99))
        else:
            pygame.draw.rect(displaySurf, GREEN, (lvlActors[0].posx, lvlActors[0].posy, 99, 99))
        # cambia las posiciones posx y posy del mono
        lvlActors[0].step(step)
        # actualiza el hitbox y dibuja el mono en sus nuevas posiciones

        lvlActors[0].hitbox = (lvlActors[0].posx, lvlActors[0].posy, 100, 100)
        displaySurf.blit(lvlActors[0].sprite, (lvlActors[0].posx, lvlActors[0].posy - 10))
        if config.lvlActors[0].holding:
            match_spritex = pygame.transform.scale(match_sprite, (130, 130))
            displaySurf.blit(match_spritex, (lvlActors[0].posx, lvlActors[0].posy - 10))
        # se cambia el valor del booleano por efectos de colisiones
        lvlActors[0].move = True
        contador += 1
        pygame.time.wait(350)
        checkCollision(lvlActors, currentlvl)
        if lvlActors[0].move == False:
            contador = num
        pygame.display.update()


def distanceToX(actor, lvlActors):
    distanceX = abs(lvlActors[0].posx - actor.posx)
    return int(distanceX / 100)


def distanceToY(actor, lvlActors):
    distanceY = abs(lvlActors[0].posy - actor.posy)
    return int(distanceY / 100)


def cerca(actor, lvlActors):
    if actor.posx == lvlActors[0].posx and actor.posy == lvlActors[0].posy:
        return True
    else:
        return False


def health(lvlActors):
    return lvlActors[0].health


###########

def moveleaf(lvlActors):
    if lvlActors[3][0].mounted:
        lvlActors[0].posx = lvlActors[3][0].posx


def changeConfigList(lvlActors, displaySurf, currentelvl):
    config.lvlActors.clear()
    for i in range(len(lvlActors)):
        config.lvlActors.append(lvlActors[i])
    config.displaySurf = displaySurf
    config.currentlvl = currentlvl


# Interpreta el input y cambia el mainList, lineNumber, insertPoint y el cursorRect.

def displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey,
                camerax, cameray, cursorRect, windowWidth, windowHeight, displaySurf, mouseClicked, mouseX, mouseY):
    if returnKey:
        firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
        secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
        mainList[lineNumber] = firstString
        mainList.insert(lineNumber + 1, secondString)
        lineNumber += 1
        returnKey = False
        insertPoint = 0
        cursorRect.x = STARTX
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
        cursorRect.y = stringRect.top


    elif mouseClicked:
        insertPoint, lineNumber, cursorRect = setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX,
                                                               mouseY)

    elif directionKey:
        if directionKey == LEFT:
            if lineNumber == 0:
                if insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = STARTY

            elif lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

                elif insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)

                    if insertPoint == 0:
                        cursorRect.x = STARTX
                        cursorRect.y = stringRect.top
                    else:
                        cursorRect.x = stringRect.right
                        cursorRect.y = stringRect.top

        elif directionKey == RIGHT:
            if insertPoint < len(mainList[lineNumber]):
                insertPoint += 1
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

            elif insertPoint >= len(mainList[lineNumber]):
                if len(mainList) > (lineNumber + 1):
                    lineNumber += 1
                    insertPoint = 0
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

        elif directionKey == UP:
            if lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top

                elif insertPoint > len(mainList[lineNumber - 1]):
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

                elif insertPoint <= len(mainList[lineNumber - 1]):
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

        elif directionKey == DOWN:
            if lineNumber + 1 < len(mainList):
                if insertPoint == 0:
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top

                elif insertPoint > len(mainList[lineNumber + 1]):
                    lineNumber += 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                elif insertPoint <= len(mainList[lineNumber + 1]):
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax,
                                                            cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

    elif typeChar:
        string = mainList[lineNumber]
        stringList = list(string)
        stringList.insert(insertPoint, newChar)
        newString = ''.join(stringList)
        mainList[lineNumber] = newString

        typeChar = False

        if len(newString) > len(
                string) and newChar != '    ':  ## Prevents alteration keys like shifts from affecting the insertPoint ##
            insertPoint += 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

        elif newChar == '    ':
            insertPoint += 4
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

    elif deleteKey:

        if insertPoint > 0:
            firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
            secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
            stringList = list(firstString)
            del stringList[insertPoint - 1]
            string = ''.join(stringList)
            string += secondString
            mainList[lineNumber] = string

            deleteKey = False
            insertPoint -= 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

        elif insertPoint <= 0:
            if lineNumber > 0:
                string = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
                del mainList[lineNumber]
                lineNumber -= 1
                mainList[lineNumber] += string

                deleteKey = False
                insertPoint = len(mainList[lineNumber]) - len(string)
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

    else:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

        if insertPoint == 0:
            cursorRect.x = STARTX
        elif insertPoint > 0:
            cursorRect.x = stringRect.right
        if lineNumber == 0:
            cursorRect.y = STARTY
        elif lineNumber > 0:
            cursorRect.y = stringRect.top
        else:
            cursorRect.x = stringRect.right

    if cursorRect.left >= STARTX:
        if cursorRect.right <= windowWidth:
            if cursorRect.top >= STARTY:
                if cursorRect.bottom <= (windowHeight - STARTY):
                    blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf)

    return mainList, lineNumber, insertPoint, cursorRect


def distanceTo(actor, lvlActors):
    return math.sqrt(pow((lvlActors[0].posx - actor.posx), 2) + pow((lvlActors[0].posy - actor.posy), 2))


def score(displaySurf, lvlActors):
    banana_aux = pygame.transform.scale(banana_sprite, (92, 64))
    match_aux = pygame.transform.scale(match_sprite, (185, 150))
    if currentlvl == 4 or currentlvl == 5:
        displaySurf.blit(match_aux, (-45, -25))
    else:
        displaySurf.blit(banana_aux, (0, 0))

    scoreFont = pygame.font.SysFont('Lucida Console', 60)
    if len(lvlActors) != 0:
        text = scoreFont.render("x" + str(lvlActors[2]), True, WHITE)
    else:
        text = scoreFont.render("x" + str(0), True, WHITE)
    displaySurf.blit(text, (100, 7))


def checkCollision(lvlActors, currentlvl):
    index = 1
    if currentlvl == 4 or currentlvl == 5:
        mapsurface = lvlActors[9:]
    else:
        mapsurface = lvlActors[8:]
    if len(lvlActors) != 0:
        monkey = lvlActors[0]

        if currentlvl == 4 or currentlvl == 5:
            index = 4

        # colisiones bananas y matches
        for item in range(len(config.lvlActors[index])):

            if monkey.posy < lvlActors[index][item].hitbox[1] + lvlActors[index][item].hitbox[3] and monkey.posy + \
                    monkey.hitbox[3] > lvlActors[index][item].hitbox[1]:
                if monkey.posx + monkey.hitbox[2] > lvlActors[index][item].hitbox[0] and monkey.posx < \
                        lvlActors[index][item].hitbox[0] + lvlActors[index][item].hitbox[2]:
                    if currentlvl == 4 or currentlvl == 5:
                        if config.lvlActors[0].holding != True:
                            config.lvlActors[0].holding = True
                            config.lvlActors[index].pop(item)

                    else:
                        config.lvlActors[2] += 1
                        config.lvlActors[index].pop(item)

                    break
        if currentlvl == 4 or currentlvl == 5:
            if monkey.posy < lvlActors[-2][0].hitbox[1] + lvlActors[-2][0].hitbox[3] and monkey.posy + \
                    monkey.hitbox[3] > lvlActors[-2][0].hitbox[1]:
                if monkey.posx + monkey.hitbox[2] > lvlActors[-2][0].hitbox[0] and monkey.posx < \
                        lvlActors[-2][0].hitbox[0] + lvlActors[-2][0].hitbox[2]:
                    if config.lvlActors[0].holding:
                        x = random.randint(-10, 10)
                        y = random.randint(-10, 10)
                        config.lvlActors[-2][1] += 1
                        config.lvlActors[2] += 1
                        config.lvlActors[0].holding = False

        # colision con lilypad
        for pad in range(len(lvlActors[3])):
            if monkey.posy < lvlActors[3][pad].hitbox[1] + lvlActors[3][pad].hitbox[3] and monkey.posy + \
                    monkey.hitbox[3] > lvlActors[3][pad].hitbox[1]:
                if monkey.posx + monkey.hitbox[2] > lvlActors[3][pad].hitbox[0] and monkey.posx < \
                        lvlActors[3][pad].hitbox[0] + lvlActors[3][pad].hitbox[2]:
                    lvlActors[3][pad].mounted = True
                    lvlActors[0].mounted = True
            else:
                lvlActors[3][pad].mounted = False
                lvlActors[0].mounted = False

        # colision cocodrilo
        for cocodrilo in range(len(lvlActors[5])):
            if monkey.posy < lvlActors[5][cocodrilo].hitbox[1] + lvlActors[5][cocodrilo].hitbox[3] and monkey.posy + \
                    monkey.hitbox[3] > lvlActors[5][cocodrilo].hitbox[1]:
                if monkey.posx + monkey.hitbox[2] > lvlActors[5][cocodrilo].hitbox[0] and monkey.posx < \
                        lvlActors[5][cocodrilo].hitbox[0] + lvlActors[5][cocodrilo].hitbox[2]:
                    lvlActors[5][cocodrilo].mounted = True
                    lvlActors[0].mounted = True
                    break
            else:
                lvlActors[5][cocodrilo].mounted = False
                lvlActors[0].mounted = False

        # colision rio y bushes
        for i in range(len(mapsurface)):
            if mapsurface[i][2] == "bush":
                if monkey.posy < mapsurface[i][1][1] + mapsurface[i][1][3] and monkey.posy + \
                        monkey.hitbox[3] > mapsurface[i][1][1]:
                    if monkey.posx + monkey.hitbox[2] > mapsurface[i][1][0] and monkey.posx < \
                            mapsurface[i][1][0] + mapsurface[i][1][2]:
                        monkey.move = False
                        collisionDetected(monkey)

            if mapsurface[i][2] == "river":
                if monkey.posy < mapsurface[i][1][1] + mapsurface[i][1][3] and monkey.posy + \
                        monkey.hitbox[3] > mapsurface[i][1][1]:
                    if monkey.posx + monkey.hitbox[2] > mapsurface[i][1][0] and monkey.posx < \
                            mapsurface[i][1][0] + mapsurface[i][1][2]:
                        if lvlActors[0].mounted:
                            print("me monte")
                            if lvlActors[3] != []:
                                moveleaf(lvlActors)
                        else:
                            monkey.move = False
                            collisionDetected(monkey)


def collisionDetected(monkey):
    if monkey.direction == "down":
        monkey.move = True
        monkey.direction = "up"
        monkey.step(1)
        monkey.move = False
    elif monkey.direction == "up":
        monkey.move = True
        monkey.direction = "down"
        monkey.step(1)
        monkey.move = False
    elif monkey.direction == "right":
        monkey.move = True
        monkey.direction = "left"
        monkey.step(1)
        monkey.move = False
    elif monkey.direction == "left":
        monkey.move = True
        monkey.direction = "right"
        monkey.step(1)
        monkey.move = False


def blitLevel(lvlActors, displaySurf, grid):
    if len(lvlActors) != 0:
        # Dibujando la superficie del nivel
        if currentlvl == 4 or currentlvl == 5:
            mapsurface = lvlActors[9:]
        else:
            mapsurface = lvlActors[8:]

        for i in range(len(mapsurface)):
            pygame.draw.rect(displaySurf, mapsurface[i][0], mapsurface[i][1])

        # leaf
        for pad in range(len(lvlActors[3])):
            displaySurf.blit(lvlActors[3][pad].sprite, (lvlActors[3][pad].posx, lvlActors[3][pad].posy))
            pygame.draw.rect(displaySurf, BLACK, lvlActors[3][pad].hitbox, 1)

        # bananas y sus hitboxes
        for coco in range(len(lvlActors[5])):
            displaySurf.blit(lvlActors[5][coco].sprite, (lvlActors[5][coco].posx, lvlActors[5][coco].posy))
            pygame.draw.rect(displaySurf, BLACK, lvlActors[5][coco].hitbox, 1)

        for banana in range(len(lvlActors[1])):
            displaySurf.blit(lvlActors[1][banana].sprite, (lvlActors[1][banana].posx, lvlActors[1][banana].posy))
            pygame.draw.rect(displaySurf, BLACK, lvlActors[1][banana].hitbox, 1)

        for match in range(len(lvlActors[4])):
            displaySurf.blit(lvlActors[4][match].sprite, (lvlActors[4][match].posx, lvlActors[4][match].posy))
            pygame.draw.rect(displaySurf, BLACK, lvlActors[4][match].hitbox, 1)

        # stack
        if currentlvl == 4 or currentlvl == 5:

            if lvlActors[-2][1] == 1:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
            elif lvlActors[-2][1] == 2:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 10, lvlActors[-2][0].posy))
            elif lvlActors[-2][1] == 3:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 10, lvlActors[-2][0].posy))
            elif lvlActors[-2][1] == 4:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 5, lvlActors[-2][0].posy - 10))
            elif lvlActors[-2][1] == 5:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 5, lvlActors[-2][0].posy - 10))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 5, lvlActors[-2][0].posy - 10))
            elif lvlActors[-2][1] == 6:
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx, lvlActors[-2][0].posy - 20))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 10, lvlActors[-2][0].posy))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx - 5, lvlActors[-2][0].posy - 10))
                displaySurf.blit(lvlActors[-2][0].sprite, (lvlActors[-2][0].posx + 5, lvlActors[-2][0].posy - 10))

            lvlActors[-2][0].hitbox = (lvlActors[-2][0].posx + 5, lvlActors[-2][0].posy + 5, 90, 90)
            pygame.draw.rect(displaySurf, BLACK, lvlActors[-2][0].hitbox, 1)

        # monkey y su hitbox
        if lvlActors[0].id == "Rat":
            displaySurf.blit(lvlActors[0].sprite, (lvlActors[0].posx, lvlActors[0].posy))
        else:
            displaySurf.blit(lvlActors[0].sprite, (lvlActors[0].posx, lvlActors[0].posy - 10))
        pygame.draw.rect(displaySurf, BLACK, lvlActors[0].hitbox, 1)
        lvlActors[0].hitbox = (lvlActors[0].posx + 0, lvlActors[0].posy, 100, 100)
        if config.lvlActors[0].holding:
            match_spritex = pygame.transform.scale(match_sprite, (100, 100))
            displaySurf.blit(match_spritex, (lvlActors[0].posx, lvlActors[0].posy - 10))

        # grid
        counterx = 0
        countery = 0
        height = 100
        width = 100
        posx = 0
        posy = 0

        while counterx < 8:
            while countery < 18:
                rect = (posx, posy, width, height)
                grid += [rect]
                pygame.draw.rect(displaySurf, WHITE, rect, 1)
                countery += 1
                posy += 100
            posy = 0
            posx += 100
            countery = 0
            counterx += 1


# le hace blit a todas las string en mainList al surface object
def blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf):
    displaySurf.fill(BGCOLOR)
    i = 0

    for string in mainList:
        stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
        stringRect = stringRender.get_rect()
        stringRect.x = STARTX - camerax
        stringRect.y = round(STARTY + (i * (TEXTHEIGHT + (TEXTHEIGHT / 4))) - cameray)
        displaySurf.blit(stringRender, stringRect)
        i += 1

    drawCursor(mainFont, cursorRect, displaySurf)


def adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray, windowWidth, windowHeight):
    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

    if (stringRect.right + cursorRect.width) > windowWidth:
        camerax += (stringRect.right + cursorRect.width) - windowWidth
    elif cursorRect.left < STARTX:
        camerax -= (-1) * (cursorRect.left)

    if stringRect.bottom > windowHeight:
        cameray += stringRect.bottom - windowHeight
    elif stringRect.top < 0:
        cameray -= (-1) * (stringRect.top)

    if insertPoint == 0:
        camerax = 0
    if lineNumber == 0:
        cameray = 0

    return camerax, cameray


def drawCursor(mainFont, cursorRect, displaySurf):
    cursor = mainFont.render('l', True, WHITE, WHITE)
    displaySurf.blit(cursor, cursorRect)


def getInput(windowWidth, windowHeight, buttons, changelvl, mainList, lvlActors, deltaTime, displaySurf):
    newChar = False
    typeChar = False
    deleteKey = False
    returnKey = False
    directionKey = False
    mouseX = 0
    mouseY = 0
    mouseClicked = False

    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if (lvlActors[3] != []):
                    lvlActors[3][0].movingPad(1)
                deleteKey = True
            elif event.key == K_ESCAPE:
                newChar = 'escape'
            elif event.key == K_RETURN:
                returnKey = True
            elif event.key == K_TAB:
                newChar = '    '
                typeChar = True
            elif event.key == K_LEFT:
                directionKey = LEFT
                lvlActors[0].direction = "left"
            elif event.key == K_RIGHT:
                directionKey = RIGHT
                lvlActors[0].direction = "right"
            elif event.key == K_UP:
                directionKey = UP
                lvlActors[0].direction = "up"
            elif event.key == K_DOWN:
                directionKey = DOWN
                lvlActors[0].direction = "down"
            else:
                newChar = event.unicode
                typeChar = True

        elif event.type == VIDEORESIZE:
            displaySurf = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            windowWidth = event.dict['w']
            windowHeight = event.dict['h']
            displaySurf.fill(WHITE)
            displaySurf.convert()
            pygame.display.update()

        elif event.type == MOUSEBUTTONDOWN:

            for i in range(len(buttons)):
                if buttons[i].isOver(mousePos):
                    if buttons[i].lvl == 10:
                        mainListaux = []
                        mainListString = ""
                        if mainList[0] != "":
                            for i in range(len(mainList)):
                                mainListaux.append(mainList[i])
                            for i in range(len(mainListaux)):
                                mainListaux[i] += ";"
                            for i in range(len(mainList)):
                                mainListString += mainListaux[i]

                        #########################
                        text = mainListString
                        if text.strip() == "": continue
                        result, error = run('<stdin>', text)
                        if error:
                            print(error.as_string())
                        elif result:
                            if len(result.elements) == 1:
                                print(repr(result.elements[0]))
                            else:
                                print(repr(result))
                        #########################
                    elif buttons[i].lvl == 11:
                        mainList = [""]
                    else:
                        changelvl = buttons[i].lvl

            mouseX, mouseY = event.pos
            mouseClicked = True

    return newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked, changelvl, mainList

    # Estas funciones basicamente envuelven lo que es el cursor


def getStringRect(string, lineNumber, camerax, cameray):
    stringRect = string.get_rect()
    stringRect.x = STARTX - camerax
    stringRect.y = round(STARTY + (lineNumber * (TEXTHEIGHT + (TEXTHEIGHT / 4))) - cameray)

    return stringRect


def getStringAtInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[0:insertPoint]
    newString = ''.join(newStringList)

    return newString


def getStringAfterInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[insertPoint:]
    newString = ''.join(newStringList)

    return newString


def getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray):
    string = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
    stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
    stringRect = getStringRect(stringRender, lineNumber, camerax, cameray)

    return stringRect

    # funciones de utilidad


def getCursorRect(cursorX, cursorY, mainFont, camerax, cameray):
    cursor = mainFont.render('L', True, RED)
    cursorRect = cursor.get_rect()
    cursorRect.x = cursorX - camerax
    cursorRect.y = round(cursorY - cameray)

    return cursorRect


def displayInfo(insertPoint, mainFont, cursorRect, camerax, windowWidth, windowHeight, displaySurf):
    number = mainFont.render(str(insertPoint), True, TEXTCOLOR, BGCOLOR)
    numbRect = number.get_rect()
    numbRect.bottom = windowHeight
    numbRect.right = windowWidth
    displaySurf.blit(number, numbRect)

    cursor = mainFont.render(str(cursorRect.x) + '  ', True, TEXTCOLOR, BGCOLOR)
    cursorNewRect = cursor.get_rect()
    cursorNewRect.bottom = windowHeight
    cursorNewRect.right = numbRect.left
    displaySurf.blit(cursor, cursorNewRect)

    cameraxRender = mainFont.render(str(camerax) + '    ', True, TEXTCOLOR, BGCOLOR)
    cameraRect = cameraxRender.get_rect()
    cameraRect.bottom = windowHeight
    cameraRect.right = cursorNewRect.left
    displaySurf.blit(cameraxRender, cameraRect)

    windowWidthRender = mainFont.render(str(windowWidth) + '    ', True, TEXTCOLOR, BGCOLOR)
    windowRect = windowWidthRender.get_rect()
    windowRect.bottom = windowHeight
    windowRect.right = cameraRect.left
    displaySurf.blit(windowWidthRender, windowRect)

    # Estas tres funciones permiten colocar el cursor donde se clickea el mous


def setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY):
    lineNumber = getLineNumberOfClick(mouseY, cameray, mainList)
    insertPoint = getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray)
    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

    if insertPoint == 0:
        cursorRect.x = STARTX
    elif insertPoint > 0:
        cursorRect.x = stringRect.right

    cursorRect.y = stringRect.top

    return insertPoint, lineNumber, cursorRect


def getLineNumberOfClick(mouseY, cameray, mainList):
    clickLineNumber = (mouseY + cameray) / float(TEXTHEIGHT + (TEXTHEIGHT / 4))
    if clickLineNumber > len(mainList):
        lineNumber = (len(mainList)) - 1
    elif clickLineNumber <= len(mainList):
        floorLineNumber = math.floor(clickLineNumber)
        lineNumber = int(floorLineNumber)

    return lineNumber


def getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray):
    string = mainList[lineNumber]
    newInsertPoint = 0

    if (mouseY + cameray) > ((lineNumber + 1) * (TEXTHEIGHT + TEXTHEIGHT / 4)):
        insertPoint = len(mainList[lineNumber])
        return insertPoint

    for insertPoint in string:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, newInsertPoint, mainFont, camerax, cameray)
        if mouseX >= stringRect.left:
            if mouseX < stringRect.right:
                if newInsertPoint > 0:
                    return newInsertPoint - 1

        newInsertPoint += 1

    else:
        return newInsertPoint


def getStringRenderAndRect(string, mainFont):
    stringRender = mainFont.render(string, True, TEXTCOLOR, WHITE)
    stringRect = stringRender.get_rect()

    return stringRender, stringRect


if __name__ == '__main__':
    runGame()
