import pygame
import sys
import math


class Gate:
    xxPos = 0.0
    yyPos = 0.0
    img = ""
    radius = 0.0
    width = 0.0
    length = 0.0

    def __init__(self, x, y, img, width, height, radius):
        self.xxPos = x
        self.yyPos = y
        self.img = img
        self.width = width
        self.height = height
        self.radius = radius
    def calcDistance(self, x, y):
        return math.sqrt((self.xxPos + self.radius - x) * (self.xxPos + self.radius - x)
                         + (self.yyPos + self.radius - y) * (self.yyPos + self.radius - y))


class Rocket:
    xxPos = 0.0
    yyPos = 0.0
    xxVel = 0.0
    yyVel = 0.0
    mass = 0.0
    width = 0.0
    height = 0.0
    img = ""
    G = 6.67e-11

    def __init__(self, xP, yP, xV, yV, m, img, width, height):
        self.mass = m
        self.xxVel = xV
        self.yyVel = yV
        self.yyPos = yP
        self.xxPos = xP
        self.img = img
        self.width = width
        self.height = height

#    def isOver(self, allplanets):

#        for planet in allplanets:
#            if

    def hasdrop(self, rocinate):
        dis = self.calcDistance(rocinate)
        #dis1 = self.calcDistanceOffset(rocinate, )
        if (dis <= rocinate.radius):
            return True
        else:
            return False
    def hasWin(self, result):
        if ((self.xxPos <= result[0] - 25) or (self.xxPos <= result[0] + 25)) and ((self.xxPos <= result[0] - 25) or (self.xxPos <= result[0] + 25)):
            return True
        else:
            return False

    def calcDistance(self, rocinate):
        return math.sqrt((rocinate.xxPos + rocinate.radius - self.xxPos) * (rocinate.xxPos + rocinate.radius - self.xxPos)
                         + (rocinate.yyPos + rocinate.radius - self.yyPos) * (rocinate.yyPos + rocinate.radius - self.yyPos))

    def calcDistanceOffset(self, rocinate, offsetx, offsety):
        return math.sqrt((rocinate.xxPos + rocinate.radius - self.xxPos - offsetx) * (rocinate.xxPos + rocinate.radius - self.xxPos - offsetx)
                         + (rocinate.yyPos + rocinate.radius - self.yyPos - offsety) * (rocinate.yyPos + rocinate.radius - self.yyPos - offsety))

    def calcForceExertedBy(self, rocinate):
        return self.G * self.mass * rocinate.mass / self.calcDistance(rocinate) / self.calcDistance(rocinate);

    def calcForceExertedByX(self, rocinate):
        return self.calcForceExertedBy(rocinate) * (rocinate.xxPos + rocinate.radius - self.xxPos) / self.calcDistance(rocinate);

    def calcForceExertedByY(self, rocinate):
        return self.calcForceExertedBy(rocinate) * (rocinate.yyPos + rocinate.radius - self.yyPos) / self.calcDistance(rocinate);

    def calcNetForceExertedByX(self, allPlanets):
        xsum = 0.0
        for planet in allPlanets:
            if self.calcDistance(planet) < planet.radius * 3:
                xsum += self.calcForceExertedByX(planet)
        return xsum

    def calcNetForceExertedByY(self, allPlanets):
        xsum = 0.0
        for planet in allPlanets:
            if planet.isBlack == False and self.calcDistance(planet) < planet.radius * 3:
                xsum += self.calcForceExertedByY(planet)
            if planet.isBlack == True and self.calcDistance(planet) < planet.radius * 5:
                xsum += self.calcForceExertedByY(planet)
        return xsum

    def update(self, dt, xforce, yforce):
        self.xxVel += xforce / self.mass * dt
        self.yyVel += yforce / self.mass * dt
        self.xxPos += dt * self.xxVel
        self.yyPos += dt * self.yyVel

class Planet():
    xxPos = 0.0
    yyPos = 0.0
    xxVel = 0.0
    yyVel = 0.0
    fix_mass = 0.0
    mass = 0.0
    radius = 0.0
    img = ""
    G=6.67e-11
    isBlack = True

    def __init__(self, xP, yP, xV, yV, m, img, r, Black):
        self.fix_mass = m
        self.mass = m
        self.xxVel = xV
        self.yyVel = yV
        self.yyPos = yP
        self.xxPos = xP
        self.img = img
        self.radius = r
        self.isBlack = Black

    def calcDistance(self, x, y):
        return math.sqrt((self.xxPos + self.radius - x) * (self.xxPos + self.radius - x)
                         + (self.yyPos + self.radius - y) * (self.yyPos + self.radius - y))

    def calcDistancep(self, p):
        return math.sqrt((self.xxPos + self.radius - p.xxPos - p.radius) * (self.xxPos + self.radius - p.xxPos - p.radius)
                         + (self.yyPos + self.radius - p.yyPos - p.radius) * (self.yyPos + self.radius - p.yyPos - p.radius))

    def calcForceExertedBy(self, rocinate):
        return self.G * self.mass * rocinate.mass / self.calcDistancep(rocinate) / self.calcDistancep(rocinate);

    def calcForceExertedByX(self, rocinate):
        return self.calcForceExertedBy(rocinate) * (rocinate.xxPos + rocinate.radius - self.xxPos - self.radius) / self.calcDistancep(rocinate);

    def calcForceExertedByY(self, rocinate):
        return self.calcForceExertedBy(rocinate) * (rocinate.yyPos + rocinate.radius - self.yyPos - self.radius) / self.calcDistancep(rocinate);

    def calcNetForceExertedByX(self, allPlanets):
        xsum = 0.0
        for planet in allPlanets:
            if (self.xxPos != planet.xxPos or self.yyPos != planet.yyPos) and self.calcDistancep(planet) > self.radius:
                xsum += self.calcForceExertedByX(planet)
        return xsum

    def calcNetForceExertedByY(self, allPlanets):
        xsum = 0.0
        for planet in allPlanets:
            if (self.xxPos != planet.xxPos or self.yyPos != planet.yyPos) and self.calcDistancep(planet) > self.radius:
                xsum += self.calcForceExertedByY(planet)
        return xsum

    def update(self, dt, xforce, yforce):
        self.xxVel += xforce / self.mass * dt
        self.yyVel += yforce / self.mass * dt
        self.xxPos += dt * self.xxVel
        self.yyPos += dt * self.yyVel