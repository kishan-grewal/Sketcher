from inspect import modulesbyfile
import math
from os import path
from tkinter import Grid
from turtle import update 
import pygame as pg 
from pygame.locals import * 
from math import exp, sqrt 
import heapq

P = 2 # p goes from 2 -> 3
N = 4**P
W = 1280 // N # equals 80 when P = 2

pg.init()
screen_width = W*N
screen_height = W*N
screen = pg.display.set_mode(size = (screen_width, screen_height))
pg.display.set_caption("Sketcher")
line_width = 3
font_obj = pg.font.Font('freesansbold.ttf', 32)


def draw_grid(grid):
    global N

    background = (250, 255, 250)
    screen.fill(background)
    filled = (0, 0, 0)
    for row in range(N):
        for col in range(N):
            if grid[row][col] == 1:
                box = pg.Rect(col*W, row*W, W, W)
                pg.draw.rect(screen, filled, box)

def scale_grid(grid, up):
    global P
    global N
    global W
    if up:
        if P+1 > 3:
            return grid
        P += 1
    else:
        if P-1 < 2:
            return grid
        P -= 1
    N = 4**P
    W = 1280 // N

    new_grid = []
    for _row in range(N):
        row = []
        for col in range(N):
            row.append(0)
        new_grid.append(row)
    if up:
        for row in range(N // 4):
            for col in range(N // 4):
                current = grid[row][col]
                for r in range(0, N // 4, 2):
                    for c in range(0, N // 4, 2):
                        new_grid[r][c] = current
                        new_grid[r][c+1] = current
                        new_grid[r+1][c] = current
                        new_grid[r+1][c+1] = current
    else:
        current = 0
        for r in range(0, N // 4, 2):
            for c in range(0, N // 4, 2):
                current += grid[r][c]
                current += grid[r][c+1]
                current += grid[r+1][c]
                current += grid[r+1][c+1]

                current /= 4
                current = round(current)
                for row in range(N):
                    for col in range(N):
                        new_grid[row][col] = current

    return new_grid


def main():
    global P
    global N
    global W

    grid = []
    for _row in range(N):
        row = []
        for col in range(N):
            row.append(0)
        grid.append(row)

    mouse_down = False
    running = True
    while running:
        draw_grid(grid)

        mouse_position = (pg.mouse.get_pos()[0] // W, pg.mouse.get_pos()[1] // W)
        row = mouse_position[1] # row equals y
        col = mouse_position[0] # col equals x
        if mouse_down == True:
            if pg.key.get_pressed()[K_SPACE] == 0:
                if grid[row][col] == 0:
                    grid[row][col] = 1
            else:
                extra = (4**(P-2)) // 2
                if extra < 1:
                    extra = 1
                for _row in range(row-extra, row+extra):
                    for _col in range(col-extra,col+extra):
                        if -1<_row<N and -1<_col<N:
                            if grid[_row][_col] == 1:
                                grid[_row][_col] = 0
                        else: pass

        pg.event.pump()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[K_2]:
                    grid = scale_grid(grid, True)
                if pg.key.get_pressed()[K_1]:
                    grid = scale_grid(grid, False)
                if pg.key.get_pressed()[K_BACKSPACE] == 1:
                    grid = []
                    for row in range(N):
                        row = []
                        for col in range(N):
                            row.append(0)
                        grid.append(row) 
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pg.MOUSEBUTTONUP:
                mouse_down = False
        
        
        pg.display.update()

    pg.quit()

main()
