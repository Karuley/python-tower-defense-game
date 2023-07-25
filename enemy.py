import pygame as pg
import math
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
import configs as c


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)

        self.target = None
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.health = ENEMY_DATA.get(enemy_type)['hp']
        self.speed = ENEMY_DATA.get(enemy_type)['spe']
        self.damage = ENEMY_DATA.get(enemy_type)['dmg']
        self.gold_dropped = ENEMY_DATA.get(enemy_type)['gold']
        self.target_waypoint = 1
        self.angle = 0

        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        # define target waypoint

        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemy has reached end of path
            self.kill()
            world.health -= self.damage
            world.missed_enemies += 1

        #calculate distance to target
        dist = self.movement.length()
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1


    def rotate(self):
        #calculate dist to next waypoint
        dist = self.target - self.pos
        #use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate and update rect
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += self.gold_dropped
            self.kill()