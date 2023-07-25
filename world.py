import pygame as pg

class World():
    def __init__(self, data, map_image):
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.img = map_image


    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "Tile Layer 1":
                self.tile_map = layer["data"]
                print(self.tile_map)
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


    def draw(self, surface):
        surface.blit(self.img, (0,0))