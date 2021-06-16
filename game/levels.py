import info
import pygame
#store the infomation in level1
def level0():
    p = []
    r = info.Rocket(100, 450, 0, 0, 1, "rocket1.png", 50, 100)
    result = info.Gate(800, 200, "exit.png", 100, 200, 100)
    return r, p, result


def level1():
    p = []
    p.append(info.Planet(500, 235, 0, 0, 5.974e13, "planet.png", 80, False))
    r = info.Rocket(100, 350, 0, 0, 1, "rocket1.png", 50, 100)
    result = info.Gate(1000, 215, "exit.png", 100, 200, 100)
    return r, p, result

def level2():
    p = []
    p.append(info.Planet(500, 220, 0, 0, 5.974e13, "planet.png", 80, False))
    r = info.Rocket(100, 350, 0, 0, 1, "rocket1.png", 50, 100)
    result = info.Gate(1000, 100, "exit.png", 100, 200, 100)
    return r, p, result

def level3():
    p = []
    p.append(info.Planet(600, 300, 0, 0, 5.974e13, "planet.png", 80, False))
    p.append(info.Planet(400, 100, 0, 0, 5.974e13, "blackhole.png", 20, True))
    r = info.Rocket(100, 450, 0, 0, 1, "rocket1.png", 40, 80)
    result = info.Gate(1000, 100, "exit.png", 100, 200, 100)
    return r, p, result

def level4():
    p = []
    p.append(info.Planet(400, 300, 0, 0, 5.974e13, "planet.png", 80, False))
    p.append(info.Planet(700, 100, 0, 0, 5.974e13, "planet.png", 80, False))
    r = info.Rocket(100, 350, 0, 0, 1, "rocket1.png", 40, 80)
    result = info.Gate(1000, 300, "exit.png", 100, 200, 100)
    return r, p, result

def level5():
    p = []
    p.append(info.Planet(400, 100, -3, 3, 1.7922e7, "planet.png", 80, False))
    p.append(info.Planet(600, 200, 0, 0, 5.967e13, "planet.png", 80, False))
    r = info.Rocket(100, 350, 0, 0, 1, "rocket1.png", 40, 80)
    result = info.Gate(1000, 250, "exit.png", 100, 200, 100)
    return r, p, result