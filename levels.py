from actors import *

# pygame.draw.rect(displaySurf, GREEN, (0, 0, 800, 900))
BLUE = (0, 0, 255)
GREEN = (41, 171, 13)
DARKGREEN = (0, 100, 0)
DESERT = (235, 226, 209)


# bananas, castores y arbustos
def level1():
    # superficie
    river = [BLUE, (0, 300, 800, 100), "river"]
    grass1 = [GREEN, (0, 0, 800, 300), "grass"]
    grass2 = [GREEN, (0, 400, 800, 500), "grass"]
    bush = [DARKGREEN, (300, 400, 100, 500), "bush"]
    # actores dentro del mapa
    banana2 = Banana(200, 500)
    monkey = Monkey(200, 200)
    pad = Pad(200,300)
    bananas = [banana2]
    turtles = [pad]
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, river, grass1, grass2, bush]
    return actors


# muchas bananas
def level2():
    # superficie
    grass = [GREEN, (0, 0, 800, 900), "grass"]
    # actores dentro del mapa
    banana2 = Banana(300, 100)
    monkey = Monkey(600, 400)
    bananas = [banana2]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, grass]

    return actors


# tortuga y arbustos
def level3():
    # superficie
    river1 = [BLUE, (0, 300, 800, 100), "river"]
    river2 = [BLUE, (0, 500, 800, 100), "river"]
    grass1 = [GREEN, (0, 0, 800, 300), "grass"]
    grass2 = [GREEN, (0, 400, 800, 100), "grass"]
    grass3 = [GREEN, (0, 600, 800, 300), "grass"]
    bush1 = [DARKGREEN, (300, 0, 100, 300), "bush"]
    bush2 = [DARKGREEN, (400, 600, 100, 900), "bush"]
    # actores dentro del mapa
    banana1 = Banana(100, 100)
    monkey = Monkey(100, 0)
    bananas = [banana1]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, river1, river2, grass1,
              grass2, grass3, bush1, bush2]

    return actors


# Raton y fosforos
def level4():
    # superficie
    desert = grass = [DESERT, (0, 0, 800, 900), "desert"]
    # actores dentro del mapa
    banana1 = Banana(100, 100)
    monkey = Monkey(250, 400)
    bananas = [banana1]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, desert]
    return actors


# raton y fosforos usando until
def level5():
    #superficie
    desert = grass = [DESERT, (0, 0, 800, 900), "desert"]
    # actores dentro del mapa
    banana1 = Banana(100, 100)
    monkey = Monkey(250, 400)
    bananas = [banana1]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, desert]
    return actors


# cocodrilos
def level6():
    #superficie
    lake = [BLUE, (0, 0, 800, 900), "lake"]
    island1 = [GREEN, (100, 100, 200, 200), "island"]
    island2 = [GREEN, (100, 500, 200, 200), "island"]
    island3 = [GREEN, (500, 100, 200, 200), "island"]
    island4 = [GREEN, (500, 500, 200, 200), "island"]
    # actores dentro del mapa
    banana1 = Banana(100, 100)
    monkey = Monkey(250, 400)
    bananas = [banana1]
    turtles = []
    matches = []
    alligators = []
    rats = []
    beavers = []
    actors = [monkey, bananas, monkey.score, turtles, matches, alligators, rats, beavers, lake, island1, island2, island3, island4]
    return actors
