from levels import *
from main import banana_sprite, monkeyhead_sprite


def levelManager(lvl):
    if lvl == 1:
        return level1()
    elif lvl == 2:
        return level2()
    elif lvl == 3:
        return level3()
    elif lvl == 4:
        return level4()
    elif lvl == 5:
        return level5()
    else:
        return level6()





