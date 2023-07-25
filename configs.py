import pygame
from pygame.locals import *
import random

class Window:
    ROWS = 15
    COLS = 24
    TILE_SIZE = 64
    SIDE_PANEL = 300
    WIDTH = TILE_SIZE * COLS#1536
    HEIGHT = TILE_SIZE * ROWS#960
    FPS = 60
    TITLE = "Tower Defense"
    #ICON = pygame.image.load("imgs/icon.png")

class TurretConstants:
    ANIMATION_STEPS = 8
    ANIMATION_DELAY = 150
    TURRET_LEVELS = 4
    BUY_COST = 200
    UPGRADE_COST = 100
    DAMAGE = 5
class EnemyConstants:
    SPAWN_COOLDOWN = 1600
    KILL_REWARD = 1
    WAVE_REWARD = 200

class PlayerConstants:
    HEALTH = 100
    MONEY = 650
    TOTAL_LEVELS = 6
