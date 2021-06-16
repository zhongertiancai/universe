import info
import pygame
import sys
import levels
import math


def draw_arrow(r, mx, my, clean_arrow):
    arrow_angle = 0
    if mx == r.xxPos:
        return pygame.transform.rotate(clean_arrow, 90)
    k = (my - r.yyPos) / (mx - r.xxPos)
    b = my - k * mx
    #print(k)
    if (mx - r.xxPos < 0):
        arrow_angle = 180 - math.atan(k)/3.14 * 180
    else:
        arrow_angle = - math.atan(k)/3.14 * 180
    #print(arrow_angle)
    arrow = pygame.transform.rotate(clean_arrow, arrow_angle)
    return arrow

def draw_dotted(r, mx, my):
    #求一条直线
    if mx == r.xxPos:
        return
    k = (my - r.yyPos) / (mx - r.xxPos)
    b = my - k * mx
    if mx > r.xxPos:
        pygame.draw.aaline(screen, WHITE, (r.xxPos, r.yyPos), (width, k * width + b), 1)
    else:
        pygame.draw.aaline(screen, WHITE, (r.xxPos, r.yyPos), (0, b), 1)

def control_angle(rocket):
    if r.xxVel != 0:
        if (r.xxVel < 0):
            angle = 180 - math.atan(r.yyVel / r.xxVel)/3.14 * 180
        else:
            angle = - math.atan(r.yyVel / r.xxVel)/3.14 * 180
        rocket = pygame.transform.rotate(rocket_clean, angle)
    return rocket

def OutOfBound(p1, width, height):
    if (p1[0] > width or p1[0] < 0):
        return True
    if (p1[1] > height or p1[1] < 0):
        return True
    return False

#游戏的初始设置
BLACK = 0, 0, 0
WHITE = 255, 255, 255
PURPLE = 30, 0, 30
PPURPLE = 25, 0, 25
fps = 300
level = 0
fclock = pygame.time.Clock()
hasShoot = False
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 1250, 625
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("back to earth")

bg = pygame.image.load("001.jpg")
bg = pygame.transform.smoothscale(bg, (width, height))
arrow_clean = pygame.image.load("arrow.png")
arrow_clean = pygame.transform.smoothscale(arrow_clean, (400, 300))

#物体的初始化
r, p, result = levels.level0()
rocket = pygame.image.load(r.img)
rocket_clean = pygame.transform.smoothscale(rocket, (r.width, r.height))
rocketrect = rocket_clean.get_rect()
rocketrect = rocketrect.move(r.xxPos, r.yyPos)

rocket = pygame.transform.rotate(rocket_clean, 270)
rocket_clean = pygame.transform.rotate(rocket_clean, 270)
planet = []
for pp in p:
    planet.append(pygame.image.load(pp.img))
for i in range(len(p)):
    planet[i] = pygame.transform.scale(planet[i], (p[i].radius*2, p[i].radius*2))
#planet = pygame.image.load(p[0].img)
#planet = pygame.transform.scale(planet,(p[0].radius * 2,p[0].radius * 2))
resultp = pygame.image.load(result.img)
resultp = pygame.transform.scale(resultp, (result.width, result.height))
screen.blit(bg, (0, 0))
slow = False

while True:
    screen.fill(PURPLE)
    #画箭头以辅助射击
    rocketrect.center = (r.xxPos, r.yyPos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            hasShoot = True
            if abs(mx - r.xxPos) > 1e-6:
                k = (my - r.yyPos) / (mx - r.xxPos)
                r.xxVel = 10 / math.sqrt(1 + k * k)
                r.yyVel = 10 / math.sqrt(1 + k * k) * k
                if (mx - r.xxPos) < 0:
                    r.xxVel = -r.xxVel
                    r.yyVel = -r.yyVel

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                for pp in p:
                    pp.mass = 0.5 * pp.fix_mass
            if event.key == pygame.K_2:
                for pp in p:
                    pp.mass = 1 * pp.fix_mass
            if event.key == pygame.K_3:
                for pp in p:
                    pp.mass = 2 * pp.fix_mass
            if event.key == pygame.K_4:
                for pp in p:
                    pp.mass = 3 * pp.fix_mass
            if event.key == pygame.K_5:
                for pp in p:
                    pp.mass = 5 * pp.fix_mass
            if event.key == pygame.K_6:
                for pp in p:
                    pp.mass = 10 * pp.fix_mass
    #更新当前的画面，并且可以控制更新的速度
    if (r.calcNetForceExertedByX(p) == 0.0) and (r.calcNetForceExertedByY(p) == 0.0):
        fps = 300
        if level == 5:
            for pp in p:
                pp.update(0.15, pp.calcNetForceExertedByX(p), pp.calcNetForceExertedByY(p))
        r.update(0.15, r.calcNetForceExertedByX(p), r.calcNetForceExertedByY(p))
    else:
        fps = 100
        if level == 5:
            for pp in p:
                pp.update(0.15, pp.calcNetForceExertedByX(p), pp.calcNetForceExertedByY(p))
        r.update(0.075, r.calcNetForceExertedByX(p), r.calcNetForceExertedByY(p))

    rocketrect = rocketrect.move(r.xxVel, r.xxVel)
    newrocket = control_angle(rocket_clean)
    newRect = newrocket.get_rect()
    newRect.top = rocketrect.top
    newRect.left = rocketrect.left
    #pygame.draw.rect(screen, WHITE, newRect, 1)
    screen.blit(newrocket, rocketrect)
    rocket = control_angle(rocket)
    if r.xxVel != 0:
        angle = math.atan(r.yyVel / r.xxVel)
    else:
        angle = 0
    middle = (newRect.left + newRect.right) / 2,(newRect.top + newRect.bottom) / 2
    p1 = (middle[0] + r.height / 2 * math.cos(angle)), (middle[1] + r.height / 2 * math.sin(angle))
    p2 = middle[0] - r.height / 2 * math.cos(angle), middle[1] - r.height / 2 * math.sin(angle)
    angle += 3.14/2
    p3 = middle[0] + r.width / 2 * math.cos(angle), middle[1] + r.width / 2 * math.sin(angle)
    p4 = middle[0] - r.width / 2 * math.cos(angle), middle[1] - r.width / 2 * math.sin(angle)


    screen.blit(newrocket, rocketrect)
    for i in range(len(p)):
        if level != 5:
            if p[i].isBlack == False:
                pygame.draw.circle(screen, PPURPLE, [p[i].xxPos + p[i].radius, p[i].yyPos + p[i].radius], p[i].radius * 3)
            else:
                pygame.draw.circle(screen, PPURPLE, [p[i].xxPos + p[i].radius, p[i].yyPos + p[i].radius], p[i].radius * 10)
        screen.blit(planet[i], (p[i].xxPos, p[i].yyPos))
    screen.blit(resultp, (result.xxPos, result.yyPos))
    screen.blit(newrocket, rocketrect)
    mx, my = pygame.mouse.get_pos()
    if hasShoot == False:
        arrow = draw_arrow(r, mx, my, arrow_clean)
        arrow_rect = arrow.get_rect()
        arrow_rect.center = (mx, my)
        screen.blit(arrow, arrow_rect)
    #pygame.draw.circle(screen, WHITE, [middle[0], middle[1]], 10, 5)
    #pygame.draw.circle(screen, WHITE, [p1[0], p1[1]], 10, 5)
    #pygame.draw.circle(screen, WHITE, [p2[0], p2[1]], 10, 5)
    #pygame.draw.circle(screen, WHITE, [p3[0], p3[1]], 10, 5)
    #pygame.draw.circle(screen, WHITE, [p4[0], p4[1]], 10, 5)
    #pygame.draw.circle(screen, WHITE, [result.xxPos + result.radius, result.yyPos+result.radius], result.radius, 5)
    pygame.display.update()
    if OutOfBound(p1, width, height):
        if level == 0:
            r, p, result = levels.level0()
        elif level == 1:
            r, p, result = levels.level1()
        elif level == 2:
            r, p, result = levels.level2()
        elif level == 3:
            r, p, result = levels.level3()
        elif level == 4:
            r, p, result = levels.level4()
        elif level == 5:
            r, p, result = levels.level5()
        hasShoot = False
        rocket = pygame.transform.rotate(rocket_clean, 0)
    for pp in p:
        if (pp.calcDistance(p1[0], p1[1]) < pp.radius or pp.calcDistance(p3[0], p3[1]) < pp.radius
                or pp.calcDistance(p2[0], p2[1]) < pp.radius or pp.calcDistance(p4[0], p4[1]) < pp.radius):
            if level == 0:
                r, p, result = levels.level0()
            elif level == 1:
                r, p, result = levels.level1()
            elif level == 2:
                r, p, result = levels.level2()
            elif level == 3:
                r, p, result = levels.level3()
            elif level == 4:
                r, p, result = levels.level4()
            elif level == 5:
                r, p, result = levels.level5()
            hasShoot = False
            rocket = pygame.transform.rotate(rocket_clean, 0)

    if (result.calcDistance(p1[0], p1[1]) < result.radius or result.calcDistance(p3[0], p3[1]) < result.radius
            or result.calcDistance(p2[0], p2[1]) < result.radius or result.calcDistance(p4[0], p4[1]) < result.radius):
        if (p1[0] < result.xxPos + result.radius or p2[0] < result.xxPos + result.radius
            or p3[0] < result.xxPos + result.radius or p3[0] < result.xxPos + result.radius):
            level += 1
            hasShoot = False
            rocket = pygame.transform.rotate(rocket_clean, 0)
            if level == 0:
                r, p, result = levels.level0()
            elif level == 1:
                r, p, result = levels.level1()
            elif level == 2:
                r, p, result = levels.level2()
            elif level == 3:
                r, p, result = levels.level3()
            elif level == 4:
                r, p, result = levels.level4()
            elif level == 5:
                r, p, result = levels.level5()

    rocket = pygame.image.load(r.img)
    rocket_clean = pygame.transform.smoothscale(rocket, (r.width, r.height))
    #rocketrect = rocket_clean.get_rect()
    #rocketrect = rocketrect.move(r.xxPos, r.yyPos)
    rocket = pygame.transform.rotate(rocket_clean, 270)
    rocket_clean = pygame.transform.rotate(rocket_clean, 270)
    planet = []
    for pp in p:
        planet.append(pygame.image.load(pp.img))
    for i in range(len(p)):
        planet[i] = pygame.transform.scale(planet[i], (p[i].radius*2, p[i].radius*2))
    fclock.tick(fps)