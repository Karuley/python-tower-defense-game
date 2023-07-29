import pygame as pg
import random
from enemy_data import ENEMY_SPAWN_DATA
import configs as c


class World:
    def __init__(self, data, map_image):
        self.level = 1
        self.game_speed = 1
        self.health = c.PlayerConstants.HEALTH
        self.money = c.PlayerConstants.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.img = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0


    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "Tile Layer 1":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    """GRASS = 0
    GROUND = 1
    #Word.is_tile(tile[x], World.GRASS
    @staticmethod
    def is_tile(search, who):
        if search == World.GRASS:
            return search in (124, 111)"""


    def process_waypoints(self, data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
                #random enemy order
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        return self.killed_enemies + self.missed_enemies == len(self.enemy_list)
        """if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True"""

    def reset_wave(self):
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0


    def draw(self, surface):
        surface.blit(self.img, (0,0))