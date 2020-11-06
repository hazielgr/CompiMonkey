from actors import *
import random

# pygame.draw.rect(displaySurf, GREEN, (0, 0, 800, 900))
BLUE = (0, 0, 255)
GREEN = (41, 171, 13)
DARKGREEN = (0, 100, 0)
DESERT = (235, 226, 209)


# nivel 1


# nivel2


# nivel3


# nivel4


# nivel5
# superficies

# nivel6


def level1():
    # posiciones random del mono
    randomposx = [200, 0, 600, 500, 400]
    randomposy = [100, 600, 500, 100, 100]

    # superficies
    river_lvl1 = [BLUE, (0, 300, 800, 100), "river"]
    grass1_lvl1 = [GREEN, (0, 0, 800, 300), "grass"]
    grass2_lvl1 = [GREEN, (0, 400, 800, 500), "grass"]
    bush1_lvl1 = [DARKGREEN, (300, 400, 100, 500), "bush"]

    # actores
    pos = random.randint(0, 4)
    monkey_lvl1 = Monkey(randomposx[pos], randomposy[pos], "Monkey")
    banana2 = Banana(200, 400)
    banan = Banana(500,700)
    ban = Banana(600,200)
    pad = Pad(200, 300)
    bananas = [banana2, banan, ban]
    turtles = [pad]
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey_lvl1, bananas, monkey_lvl1.score, turtles, matches, alligators, rats, beavers, river_lvl1,
              grass1_lvl1, grass2_lvl1, bush1_lvl1]
    return actors


# muchas bananas
def level2():
    # posiciones random del mono
    randomposx = [200, 0, 600, 500, 400, 400, 500, 300]
    randomposy = [100, 600, 500, 100, 100, 0, 500, 500]

    # superficies
    grass1_lvl2 = [GREEN, (0, 0, 800, 900), "grass"]

    # actores
    pos = random.randint(0, 7)
    monkey_lvl2 = Monkey(randomposx[pos], randomposy[pos], "Monkey")
    banana = Banana(300, 300)
    banan = Banana(100, 100)
    bana = Banana(0, 400)
    ban = Banana(700, 0)
    ba = Banana(100, 600)
    b = Banana(600, 200)
    an = Banana(700, 500)
    ana = Banana(300, 800)
    banana2 = Banana(500, 700)
    bananas = [banana2,ana,an,b,ba,ban,bana,banan,banana]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey_lvl2, bananas, monkey_lvl2.score, turtles, matches, alligators, rats, beavers, grass1_lvl2]
    return actors


# tortuga y arbustos
def level3():
    # posiciones random del mono
    randomposx = [100, 0, 0, 500, 0, 0, 0, 600, 500]
    randomposy = [0, 100, 0, 100, 200, 400, 400, 700, 600]

    # superficies
    river1_lvl3 = [BLUE, (0, 300, 800, 100), "river"]
    river2_lvl3 = [BLUE, (0, 500, 800, 100), "river"]
    grass1_lvl3 = [GREEN, (0, 0, 800, 300), "grass"]
    grass2_lvl3 = [GREEN, (0, 400, 800, 100), "grass"]
    grass3_lvl3 = [GREEN, (0, 600, 800, 300), "grass"]
    bush1_lvl3 = [DARKGREEN, (300, 0, 100, 300), "bush"]
    bush2_lvl3 = [DARKGREEN, (400, 600, 100, 900), "bush"]
    # actores
    pos = random.randint(0, 8)
    monkey_lvl3 = Monkey(randomposx[pos], randomposy[pos], "Monkey")

    banana = Banana(200, 0)
    banan = Banana(700, 100)
    bana = Banana(300, 400)
    ban = Banana(700, 400)
    ba = Banana(700, 600)
    b = Banana(100, 800)
    bananas = [b, ba, ban, bana, banan, banana]

    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey_lvl3, bananas, monkey_lvl3.score, turtles, matches, alligators, rats, beavers, river1_lvl3,
              river2_lvl3, grass1_lvl3,
              grass2_lvl3, grass3_lvl3, bush1_lvl3, bush2_lvl3]
    return actors


# Raton y fosforos
def level4():
    # posiciones random de la rata
    randomposx = [200, 0, 600, 500, 400, 400, 500, 300]
    randomposy = [100, 600, 500, 100, 100, 0, 500, 500]

    # superficies
    desert = [DESERT, (0, 0, 800, 900), "desert"]

    # actores
    pos = random.randint(0, 7)
    rata_lvl4 = Monkey(randomposx[pos], randomposy[pos], "Rat")
    match1 = Match(100, 100)
    bananas = []
    turtles = []
    matches = [match1]
    alligators = []
    rats = []
    beavers = []
    actors = [rata_lvl4, bananas, rata_lvl4.score, turtles, matches, alligators, rats, beavers, desert]
    return actors


# raton y fosforos usando until
def level5():
    # posiciones random de la rata
    randomposx = [200, 0, 600, 500, 400, 400, 500, 300]
    randomposy = [100, 600, 500, 100, 100, 0, 500, 500]

    # superficies
    desert = [DESERT, (0, 0, 800, 900), "desert"]

    # actores
    pos = random.randint(0, 7)
    rata_lvl5 = Monkey(randomposx[pos], randomposy[pos], "Rat")
    match1 = Match(100, 100)
    bananas = []
    turtles = []
    matches = [match1]
    alligators = []
    rats = []
    beavers = []
    actors = [rata_lvl5, bananas, rata_lvl5.score, turtles, matches, alligators, rats, beavers, desert]
    return actors


# cocodrilos
def level6():
    # posiciones random del mono
    randomposx = [100, 200, 200, 700, 700, 600, 600]
    randomposy = [200, 600, 700, 700, 700, 100, 200]

    # superficies
    river1_lvl6 = [BLUE, (0, 0, 800, 100), "river"]
    river2_lvl6 = [BLUE, (0, 100, 100, 800), "river"]
    river3_lvl6 = [BLUE, (100, 800, 700, 100), "river"]
    river4_lvl6 = [BLUE, (300, 100, 300, 700), "river"]
    river5_lvl6 = [BLUE, (100, 300, 700, 300), "river"]
    island1 = [GREEN, (100, 100, 200, 200), "island"]
    island2 = [GREEN, (100, 600, 200, 200), "island"]
    island3 = [GREEN, (600, 100, 200, 200), "island"]
    island4 = [GREEN, (600, 600, 200, 200), "island"]

    # actores
    pos = random.randint(0, 6)
    monkey_lvl6 = Monkey(randomposx[pos], randomposy[pos], "Monkey")

    banana = Banana(400, 200)
    banan = Banana(200, 400)
    bana = Banana(600, 400)
    ban = Banana(400, 600)
    bananas = [ban, bana, banan, banana]

    cocofunka = Coco(200, 300)
    turtles = []
    matches = []
    cocofunka = Coco(100, 400)
    cokofunka = Coco(300, 200)
    cocofunca = Coco(500, 400)
    alligators = [cocofunka,cokofunka,cocofunca]
    rats = []
    beavers = []
    actors = [monkey_lvl6, bananas, monkey_lvl6.score, turtles, matches, alligators, rats, beavers, river1_lvl6,
              river2_lvl6, river3_lvl6, river4_lvl6, river5_lvl6, island1, island2,
              island3, island4]
    return actors
