# -*- coding: utf-8 -*-

from random import randint
import pygame
import sys
import math


def Random(a, b):
    rnd = randint(a, b)
    return rnd


def Ethage():
    global labyrint_list
    ethage = []
    for i in range(-2, vertical_sise+1):
        if i>=0:
            ethage.append(i)
    ethage.append(-1)
    ethage.append(-2)
    for eth in ethage:
        labyrint_list.append(Labyrint_line(eth))


def Labyrint_line(line):
    global labyrint_list, horizontal_sise
    
    # Выход из лабиринта    
    if int(line) == 0:
        Labyrint_0 = []
        ext = Random(1, horizontal_sise-1+2)
        for i in range(horizontal_sise+1+2):
            if i != ext:
                Labyrint_0.append("X")
            else:
                Labyrint_0.append("O")
        return Labyrint_0
    
    # финишная линия
    if int(line) == 1:
        Labyrint_1 = []
        ext = labyrint_list[0].index("O")
        for i in range(horizontal_sise+1+2):
            if (i==0 or i==horizontal_sise+2):
                Labyrint_1.append("X")
            elif i==ext:
                Labyrint_1.append("O")
            else:
                a = Random(0, 1)
                if a == 0:
                    Labyrint_1.append("O")
                else:
                    Labyrint_1.append("X")
        return Labyrint_1

    # Вход в лабиринт
    if int(line) == -2:
        Labyrint_open = []
        ext = Random(1, horizontal_sise-1+2)
        for i in range(horizontal_sise+1+2):
            if i != ext:
                Labyrint_open.append("X")
            else:
                Labyrint_open.append("O")
        return Labyrint_open

    # линия старта
    if int(line) == -1:
        Labyrint_start = []
        for i in range(horizontal_sise+1+2):
            if (i==0 or i==horizontal_sise+2):
                Labyrint_start.append("X")
            else:                
                Labyrint_start.append("O")
        return Labyrint_start
    
    # прочие линии
    else:
        labyrint_line = []
        k=0
        ln = labyrint_list[len(labyrint_list)-1]
        
        for i in range(horizontal_sise+1+2):
            rnd = Random(0, 2)
            if rnd==0:
                rnd = "O"
            else:
                rnd = "X"
            labyrint_line.append(rnd)
            if ln[i]=="O":
                k+=1
            if ln[i]=="X":
                if k>=1:
                    ret = Random(i-k, i-1)
                    del labyrint_line[ret]
                    labyrint_line.insert(ret, "O")
                    k=0
        labyrint_line[0] = "X" 
        labyrint_line[horizontal_sise+2] = "X"
        return labyrint_line
    
    
def Labyrint_koordinate():
    global labyrint_list, start, finish
    start = vertical_sise+2
    # print(start)
    labyrint_wall = []
    Ethage()
    x = 0
    y = 0
    for n, k in enumerate(labyrint_list):
        y+=STEP
        x=0
        for j in k:
            x+=STEP
            if n==0:
                if j == "O":
                    finish = [x, y]
                    
            if n==start:
                if j == "O":
                    start = [x, y]
                    
            if j!="O":
                labyrint_wall.append([x ,y])
    # print(f"start {start}")
    # print(f"finish {finish}")
    return labyrint_wall


def Size_TILE():
    horizontal_sise_max = horizontal_sise + 5
    vertical_sise_max = vertical_sise + 5
    horizontal_tile = int(WIDTH / horizontal_sise_max)
    vertical_tile = int(HEIGHT / vertical_sise_max)
    if (vertical_tile < horizontal_tile):
        return vertical_tile
    else:
        return horizontal_tile


def Start_player():
    start_player = []
    for s in start:
        s += int((STEP//2))
        start_player.append(s)
    # print(start_player)
    return start_player


labyrint_list = []
rect_wall = []

# размеры лабиринта
horizontal_sise = 50
vertical_sise = 50


WIDTH = 800
HEIGHT = 600
FPS = 10
STEP = Size_TILE()

NUM_RAYS = 120
MAX_DEPTH = 800
player_angle = 0
player_speed = 2
FOV = math.pi / 3
HALF_FOV = FOV / 2
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * STEP
SCALE = WIDTH // NUM_RAYS


start = None
finish = None

labyrint_wall = Labyrint_koordinate()
pos_player = Start_player()
x_1 = pos_player[0]
y_1 = pos_player[1]
# print(x, y)
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

for x, y in labyrint_wall:
    rect_wall.append(pygame.draw.rect(sc, (0, 0, 255), (x, y, STEP, STEP)))
    # print(rect_wall)
# player = pygame.draw.circle(sc, (250, 0, 0), (x, y), int(TILE/2-TILE/20))

pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

print(pos_player)

while True:
    sc.fill((200, 255, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for x, y in labyrint_wall:
        pygame.draw.rect(sc, (0, 0, 255), (x, y, STEP, STEP))
        
    
        
        
    if event.type == pygame.KEYDOWN:
        # sled = pygame.draw.rect(sc, (0, 250, 0), (x_1, y_1, 10, 10))
        # sled.move_ip(x_1, y_1)
        
        if event.key == pygame.K_UP:
            pos_player[1]-=STEP
            if pos_player[1] < (0 + STEP):
                pos_player[1]+=STEP
                print("EXIT")
                pygame.quit()
                sys.exit()
                
            for a in rect_wall:
                wall = a.collidepoint(pos_player)
                if wall == True:
                    pos_player[1]+=STEP
                    break
                
        elif event.key == pygame.K_DOWN:
            pos_player[1]+=STEP
            if pos_player[1] > (HEIGHT - STEP):
                pos_player[1]-=STEP
            for a in rect_wall:
                wall = a.collidepoint(pos_player)
                if wall == True:
                    pos_player[1]-=STEP
                    break
                
        elif event.key == pygame.K_LEFT:
            pos_player[0]-=STEP
            for a in rect_wall:
                wall = a.collidepoint(pos_player)
                if wall == True:
                    pos_player[0]+=STEP
                    break
                
        elif event.key == pygame.K_RIGHT:
            pos_player[0]+=STEP
            for a in rect_wall:
                wall = a.collidepoint(pos_player)
                if wall == True:
                    pos_player[0]-=STEP
                    break
                
    # if sc.mouse.get_focused():
    pos_mous = pygame.mouse.get_pos()
   
    
                
    # cur_angle = player_angle - HALF_FOV
    # for ray in range(NUM_RAYS):
    #     sin_a = math.sin(cur_angle)
    #     cos_a = math.cos(cur_angle)
    #     for depth in range(MAX_DEPTH):
    #         x = pos_player[0] + depth * cos_a
    #         y = pos_player[1] + depth * sin_a
    #         if (x , y) in labyrint_wall:
    #             depth *= math.cos(player_angle - cur_angle)
    #             proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
    #             c = 255 / (1 + depth * depth * 0.0001)
    #             color = (c // 2, c, c // 3)
    #             pygame.draw.rect(sc, color, (ray * SCALE, pos_player[1] - proj_height // 2, SCALE, proj_height))
    #             break
    #     cur_angle += DELTA_ANGLE
    
    # print(pos_player)
    # print(pos_mous) 
    # num = ((pos_player[0]-pos_mous[0])**2 + (pos_player[1]-pos_mous[1])**2)
    # d = round(math.sqrt(num), 1)
    # cos_a = pos_mous[0]/d
    # sin_a = pos_mous[1]/d
    # x_m = cos_a*STEP
    # y_m = sin_a*STEP
    # print(x_m, y_m)
    
    # pygame.draw.line(sc, (0, 250, 0), pos_player, pos_mous, 2)
    
    # print(d)   
    
        
    
    pygame.draw.circle(sc, (250, 0, 0), (pos_player), STEP/2-STEP/5)
    # pygame.draw.circle(sc, (0, 250, 0), (x_1, y_1), 10)
    # print(x_1, y_1)
    pygame.display.flip()
    # pygame.display.update()
    clock.tick(FPS)