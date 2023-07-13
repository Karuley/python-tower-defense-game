import pygame
from pygame.locals import *



class Window:
    ROWS = 15
    COLS = 24
    TILE_SIZE = 64
    WIDTH = TILE_SIZE * COLS#1536
    HEIGHT = TILE_SIZE * ROWS#960
    FPS = 60
    TITLE = "Tower Defense"
    #ICON = pygame.image.load("imgs/icon.png")