import pygame as pg
import json

import configs as c
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from turret_data import TURRET_DATA

pg.init()

#clock
clock = pg.time.Clock()

#game window
screen = pg.display.set_mode((c.Window.WIDTH + c.Window.SIDE_PANEL, c.Window.HEIGHT))
pg.display.set_caption(c.Window.TITLE)

# =======================
# GAME VARIABLES (to be moved)
# =======================
can_place_turrets = False
selected_turret = None


# =======================
# LOAD IMAGES (to be moved)
# =======================

#map
map_image = pg.image.load('assets/imgs/map.png').convert_alpha()
# turrets
turret_spritesheets = []
for sprite in range(1, c.Turret_Constants.TURRET_LEVELS + 1 ):
    turret_sheet = pg.image.load(f'assets/imgs/sheets/sheet{sprite}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)



cursor_turret = pg.image.load('assets/imgs/archer.png').convert_alpha()
#enemies
enemy_image = pg.image.load('assets/imgs/slime.png').convert_alpha()
#buttons
buy_turret_image = pg.image.load('assets/imgs/button/buy_button.png').convert_alpha()
cancel_turret_image = pg.image.load('assets/imgs/button/cancel_button.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/imgs/button/upgrade_button.png').convert_alpha()



#json data for level
with open('assets/waypoints/waypoints1.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.Window.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.Window.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.Window.COLS) + mouse_tile_x
    #check for grass
    if world.tile_map[mouse_tile_num] == 25 or world.tile_map[mouse_tile_num] == 163:
        #check for duplicate turrets
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        #if free then create
        if space_is_free:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.Window.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.Window.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()


enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)
print(enemy)

#create buttons
turret_button = Button(c.Window.WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.Window.WIDTH + 30, 220, cancel_turret_image, True)
upgrade_button = Button(c.Window.WIDTH + 30, 220, upgrade_turret_image, True)


#game loop
run = True
while run:

    clock.tick(c.Window.FPS)

    # =======================
    # SCREEN UPDATE
    # =======================

    #update groups
    enemy_group.update()
    turret_group.update(enemy_group)
    if selected_turret:
        selected_turret.selected = True

    # =======================
    # SCREEN DRAW
    # =======================

    screen.fill("grey100")
    world.draw(screen)


    #draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)
    #turret_group.draw(screen)

    #draw buttons
    if turret_button.draw(screen):
        can_place_turrets = True
    if can_place_turrets:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.Window.WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            can_place_turrets = False
    #show upgrade buttom
    if selected_turret:
        if selected_turret.upgrade_level < c.Turret_Constants.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()


    # =======================
    # HANDLE EVENTS
    # =======================

    for event in pg.event.get():

        #quit game
        if event.type == pg.QUIT:
            run = False
         #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check map boudaries
            if mouse_pos[0] < c.Window.WIDTH and mouse_pos[1] < c.Window.HEIGHT:
                #clear turret range
                selected_turret = None
                clear_selection()
                if can_place_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    pg.display.flip()

pg.quit()
