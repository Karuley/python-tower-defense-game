import pygame as pg
import json

from configs import Window as c
from enemy import Enemy
from world import World
from turret import Turret

pg.init()

#clock
clock = pg.time.Clock()

#game window
screen = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption(c.TITLE)

#load images
#map
map_image = pg.image.load('assets/imgs/map.png').convert_alpha()

#enemies
enemy_image = pg.image.load('assets/imgs/slime.png').convert_alpha()

#json data for level
with open('assets/waypoints/waypoints1.tmj') as file:
    world_data = json.load(file)


#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pg.sprite.Group()


enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)
print(enemy)


#game loop
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")
    world.draw(screen)

    #draw enemy path
    #pg.draw.lines(screen, "grey0", False, world.waypoints)

    #update groups
    enemy_group.update()

    #draw groups

    enemy_group.draw(screen)

    #event handler
    for event in pg.event.get():

        #quit game
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()
