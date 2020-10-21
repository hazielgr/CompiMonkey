from actors import *


def level1():

    banana1 = Banana(100, 100)
    banana2 = Banana(300, 500)
    banana3 = Banana(500, 100)
    monkey = Monkey(250, 0)
    bananas = [banana2]
    actors = [monkey,bananas, monkey.score]
    return actors

def level2():

    banana1 = Banana(100, 100)
    banana2 = Banana(300, 100)
    banana3 = Banana(500, 100)
    banana4 = Banana(600, 400)
    monkey = Monkey(600, 400)
    bananas = [banana1, banana2, banana3, banana4]
    actors = [monkey, bananas, monkey.score]

    return actors

def level3():

    banana1 = Banana(100, 100)
    banana2 = Banana(300, 100)
    banana3 = Banana(500, 100)
    banana4 = Banana(400, 100)
    monkey = Monkey(250, 400)
    bananas = [banana1, banana2, banana3, banana4]
    actors = [monkey, bananas, monkey.score]

    return actors