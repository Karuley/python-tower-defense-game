import pygame as pg

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pg.image.load(filename).convert()



    def get_sprite(self, x, y, w, h):
        sprite = pg.Surface((w, h))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))