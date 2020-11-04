from actors import *

# pygame.draw.rect(displaySurf, GREEN, (0, 0, 800, 900))
BLUE = (0, 0, 255)
GREEN = (41, 171, 13)
DARKGREEN = (0, 100, 0)
DESERT = (235, 226, 209)

# nivel 1

# superficies
river_lvl1 = [BLUE, (0, 300, 800, 100), "river"]
grass1_lvl1 = [GREEN, (0, 0, 800, 300), "grass"]
grass2_lvl1 = [GREEN, (0, 400, 800, 500), "grass"]
bush1_lvl1 = [DARKGREEN, (300, 400, 100, 500), "bush"]
# actores
monkey_lvl1 = Monkey(200, 100,"Monkey")

# nivel2

# superficies
grass1_lvl2 = [GREEN, (0, 0, 800, 900), "grass"]
# actores
monkey_lvl2 = Monkey(600, 400, "Monkey")
# nivel3
# superficies
river1_lvl3 = [BLUE, (0, 300, 800, 100), "river"]
river2_lvl3 = [BLUE, (0, 500, 800, 100), "river"]
grass1_lvl3 = [GREEN, (0, 0, 800, 300), "grass"]
grass2_lvl3 = [GREEN, (0, 400, 800, 100), "grass"]
grass3_lvl3 = [GREEN, (0, 600, 800, 300), "grass"]
bush1_lvl3 = [DARKGREEN, (300, 0, 100, 300), "bush"]
bush2_lvl3 = [DARKGREEN, (400, 600, 100, 900), "bush"]
# actores
monkey_lvl3 = Monkey(100, 0, "Monkey")
# nivel4
# superficies
desert = grass = [DESERT, (0, 0, 800, 900), "desert"]
# actores
rata_lvl4 = Monkey(200, 400, "Rat")
# nivel5
# superficies
# actores
rata_lvl5 = Monkey(200, 400, "Rat")
# nivel6
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
monkey_lvl6 = Monkey(100, 100,"Monkey")


def level1():
    banana2 = Banana(200, 500)
    pad = Pad(200, 300)
    bananas = [banana2]
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
    banana2 = Banana(300, 100)
    bananas = [banana2]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey_lvl2, bananas, monkey_lvl2.score, turtles, matches, alligators, rats, beavers, grass1_lvl2]
    return actors

# tortuga y arbustos
def level3():
    banana1 = Banana(100, 100)
    bananas = [banana1]
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
    banana1 = Banana(100, 100)
    cocofunka = Coco (200,300)
    bananas = [banana1]
    turtles = []
    matches = []
    alligators = [cocofunka]
    rats = []
    beavers = []
    actors = [monkey_lvl6, bananas, monkey_lvl6.score, turtles, matches, alligators, rats, beavers, river1_lvl6,river2_lvl6,river3_lvl6,river4_lvl6,river5_lvl6, island1, island2,
              island3, island4]
    return actors
