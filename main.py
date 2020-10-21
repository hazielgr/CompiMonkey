import pygame, sys, math
from pygame.locals import *
from levels import level1
from lvlManager import *
from button import *

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

icon = pygame.image.load('resources/sprites/monkey_head_icon.png')
monkeyhead_sprite = pygame.image.load('resources/sprites/monkey_head_icon.png')
banana_sprite = pygame.image.load('resources/sprites/jungle_banana_icon.png')

buttons = []
buttonx = 0
buttony = 850


def main():
    global FPSCLOCK
    lvlActors = []
    grid = []
    changelvl = 0
    currentlvl = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
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

    insertPoint = 0
    camerax = 0
    cameray = 0

    mouseClicked = False
    mouseX = 0
    mouseY = 0

    # displaySurf.fill(BGCOLOR)

    pygame.display.update()

    pygame.display.set_caption('CompiMonkey')
    pygame.display.set_icon(icon)

    mainFont = pygame.font.SysFont('Lucida Console', TEXTHEIGHT)

    cursorRect = getCursorRect(STARTX, STARTY + (TEXTHEIGHT + (TEXTHEIGHT / 4)), mainFont, camerax, cameray)

    # El loop del juego detecta el input del usuario y lo muestra en pantalla
    # coloca el cursor en la pantalla y ajusta la camara de ser necesario

    while running:

        camerax, cameray = adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray,
                                        windowWidth, windowHeight)

        newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked = getInput(
            windowWidth, windowHeight)

        mainList, lineNumber, insertPoint, cursorRect = displayText(mainFont, newChar, typeChar, mainList, deleteKey,
                                                                    returnKey, lineNumber, insertPoint, directionKey,
                                                                    camerax, cameray, cursorRect, windowWidth,
                                                                    windowHeight, displaySurf, mouseClicked, mouseX,
                                                                    mouseY)

        displayInfo(insertPoint, mainFont, cursorRect, camerax, windowWidth, windowHeight, displaySurf)

        # buttons
        lvl1_button = Button(1, CREAM, buttonx, buttony, 100, 50, "lvl1")
        lvl2_button = Button(2, CREAM, buttonx + 110, buttony, 100, 50, "lvl2")
        lvl3_button = Button(3, CREAM, buttonx + 220, buttony, 100, 50, "lvl3")
        lvl4_button = Button(4, CREAM, buttonx + 330, buttony, 100, 50, "lvl4")
        lvl5_button = Button(5, CREAM, buttonx + 440, buttony, 100, 50, "lvl5")
        lvl6_button = Button(6, CREAM, buttonx + 550, buttony, 100, 50, "lvl6")

        buttons = [lvl1_button, lvl2_button, lvl3_button, lvl4_button, lvl5_button, lvl6_button]

        # level manager
        if currentlvl != changelvl:
            lvlActors = levelManager(changelvl)
            currentlvl = changelvl
            

        blitLevel(lvlActors, displaySurf, grid)

        # dibuja los botones
        for i in range(len(buttons)):
            buttons[i].draw(displaySurf)

        # revisa si el mouse fue clickeado
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].isOver(mousePos):
                        changelvl = buttons[i].lvl

        checkCollision(lvlActors)

        # mov mono
        if len(lvlActors) != 0:
            lvlActors[0].posy += 1

        score(displaySurf, lvlActors)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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
        printmainList(mainList)

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


def score(displaySurf, lvlActors):
    banana_aux = pygame.transform.scale(banana_sprite, (92, 64))

    displaySurf.blit(banana_aux, (0, 0))
    scoreFont = pygame.font.SysFont('Lucida Console', 60)
    if len(lvlActors) != 0:
        text = scoreFont.render("x" + str(lvlActors[2]), True, WHITE)
    else:
        text = scoreFont.render("x" + str(0), True, WHITE)
    displaySurf.blit(text, (100, 7))


def checkCollision(lvlActors):
    if len(lvlActors) != 0:
        monkey = lvlActors[0]
        for banana in range(len(lvlActors[1])):
            if monkey.posy < lvlActors[1][banana].hitbox[1] + lvlActors[1][banana].hitbox[3] and monkey.posy + \
                    monkey.hitbox[3] > lvlActors[1][banana].hitbox[1]:
                if monkey.posx + monkey.hitbox[2] > lvlActors[1][banana].hitbox[0] and monkey.posx < \
                        lvlActors[1][banana].hitbox[0] + lvlActors[1][banana].hitbox[2]:
                    lvlActors[2] += 1
                    lvlActors[1].pop(banana)


def blitLevel(lvlActors, displaySurf, grid):
    if len(lvlActors) != 0:
        # Dibujando la superficie del nivel
        mapsurface = lvlActors[8:]

        for i in range(len(mapsurface)):
            pygame.draw.rect(displaySurf, mapsurface[i][0], mapsurface[i][1])

        # monkey y su hitbox
        displaySurf.blit(lvlActors[0].sprite, (lvlActors[0].posx, lvlActors[0].posy))
        pygame.draw.rect(displaySurf, BLACK, lvlActors[0].hitbox, 2)
        lvlActors[0].hitbox = (lvlActors[0].posx + 11, lvlActors[0].posy + 35, 375, 305)

        # bananas y sus hitboxes
        for banana in range(len(lvlActors[1])):
            displaySurf.blit(lvlActors[1][banana].sprite, (lvlActors[1][banana].posx, lvlActors[1][banana].posy))
            pygame.draw.rect(displaySurf, BLACK, lvlActors[1][banana].hitbox, 2)

        # grid
        counterx = 0
        countery = 0
        height = 50
        width = 50
        posx = 0
        posy = 0



        while counterx < 16:
            while countery < 18:
                rect = (posx, posy, width, height)
                grid += [rect]
                pygame.draw.rect(displaySurf, WHITE, rect, 1)
                countery += 1
                posy += 50
            posy = 0
            posx += 50
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


def getInput(windowWidth, windowHeight):
    newChar = False
    typeChar = False
    deleteKey = False
    returnKey = False
    directionKey = False
    mouseX = 0
    mouseY = 0
    mouseClicked = False
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
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
            elif event.key == K_RIGHT:
                directionKey = RIGHT
            elif event.key == K_UP:
                directionKey = UP
            elif event.key == K_DOWN:
                directionKey = DOWN
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
            mouseX, mouseY = event.pos
            mouseClicked = True

    return newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked

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


def printmainList(mainList):
    for item in mainList[:-1]:
        print(item)


if __name__ == '__main__':
    main()
