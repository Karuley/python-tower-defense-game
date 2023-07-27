import pygame as pg
import json
import random

import configs
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
Icon = pg.image.load('assets/imgs/castle.png')
pg.display.set_icon(Icon)

# =======================
# GAME VARIABLES (to be moved?)
# =======================

game_over = False
game_win = True
level_started = False
last_enemy_spawn = pg.time.get_ticks()
can_place_turrets = False
selected_turret = None


# =======================
# LOAD IMAGES (to be moved?)
# =======================

#map
map_image = pg.image.load('assets/imgs/map.png').convert_alpha()
# turrets
turret_spritesheets = []
for sprite in range(1, c.TurretConstants.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'assets/imgs/sheets/sheet{sprite}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)



cursor_turret = pg.image.load('assets/imgs/archer2.png').convert_alpha()
#enemies
enemy_images = {
    "slime": pg.image.load('assets/imgs/enemies/slime1.png').convert_alpha(),
    "goblin": pg.image.load('assets/imgs/enemies/slime2.png').convert_alpha(),
    "orc": pg.image.load('assets/imgs/enemies/slime3.png').convert_alpha(),
    "wyvern": pg.image.load('assets/imgs/enemies/slime4.png').convert_alpha()
}
#enemy_image = pg.image.load('assets/imgs/enemies/slime1.png').convert_alpha()
#buttons
buy_turret_image = pg.image.load('assets/imgs/button/buy_button.png').convert_alpha()
cancel_turret_image = pg.image.load('assets/imgs/button/cancel_button.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/imgs/button/upgrade_button.png').convert_alpha()
start_image = pg.image.load('assets/imgs/button/start_button.png').convert_alpha()
restart_image = pg.image.load('assets/imgs/button/restart_button.png').convert_alpha()
fast_image = pg.image.load('assets/imgs/button/fast_button.png').convert_alpha()

#load world assets
castle_big = pg.image.load('assets/imgs/castlebig.png').convert_alpha()
castle = pg.image.load('assets/imgs/castle.png').convert_alpha()
gold = pg.image.load('assets/imgs/gold.png').convert_alpha()
logo = pg.image.load('assets/imgs/logo.png').convert_alpha()





#json data for level
with open('assets/waypoints/waypoints1.tmj') as file:
    world_data = json.load(file)

    # =======================
    # LOAD FONTS
    # =======================
text_font = pg.font.SysFont('Upheaval TT (BRK)', 24)
large_font = pg.font.SysFont('Upheaval TT (BRK)', 36)

# =======================
# DRAW TEXT
# =======================
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    pg.draw.rect(screen, 'maroon', (c.Window.WIDTH, 0, c.Window.SIDE_PANEL, c.Window.HEIGHT))
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
            world.money -= c.TurretConstants.BUY_COST


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.Window.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.Window.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False
    # =======================
    # CREATE WORLD
    # =======================
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# =======================
# CREATE GROUPS
# =======================
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()



# =======================
# CREATE BUTTONS
# =======================
turret_button = Button(c.Window.WIDTH + 30, 240, buy_turret_image, True)
cancel_button = Button(c.Window.WIDTH + 30, 340, cancel_turret_image, True)
upgrade_button = Button(c.Window.WIDTH + 30, 240, upgrade_turret_image, True)
start_button = Button(c.Window.WIDTH + 30, 140, start_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_button = Button(c.Window.WIDTH + 30, 140, fast_image, False)



#game loop
run = True
while run:

    clock.tick(c.Window.FPS)

    # =======================
    # SCREEN UPDATE
    # =======================

    if not game_over:
        if world.health <= 0:
            game_win = False
            game_over = True

        #check for all levels completed
        if world.level > c.PlayerConstants.TOTAL_LEVELS:
            game_win = True
            game_over = True


    #update groups
        enemy_group.update(world)
        turret_group.update(enemy_group, world)
        if selected_turret:
            selected_turret.selected = True

    # =======================
    # SCREEN DRAW
    # =======================


    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    display_data()
    screen.blit(logo, (c.Window.WIDTH + 7, 20))
    screen.blit(castle_big, (17, (c.Window.HEIGHT - 100)))
    screen.blit(castle, (c.Window.WIDTH + 20, 440))
    screen.blit(gold, (c.Window.WIDTH + 20, 520))
    draw_text(str(f'Health: {world.health}'), text_font, 'grey100', c.Window.WIDTH + 90, 470)
    draw_text(str(f'Gold: {world.money}'), text_font, 'grey100', c.Window.WIDTH + 90, 540)
    draw_text(str(f'Wave: {world.level}'), text_font, 'grey100', c.Window.WIDTH + 90, 620)
    draw_text(str(f'Enemies: {len(world.enemy_list) - world.spawned_enemies}'), text_font, 'grey100', c.Window.WIDTH + 90, 700)

    if not game_over:
        #spawn enemies
        #check for start button press
        if not level_started:
            if start_button.draw(screen):
                level_started = True
        else:
            world.game_speed = 1
            if fast_button.draw(screen):
                world.game_speed = 2
            if pg.time.get_ticks() - last_enemy_spawn > c.EnemyConstants.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    c.EnemyConstants.SPAWN_COOLDOWN = random.randint(800, 1800)
                    last_enemy_spawn = pg.time.get_ticks()

        #check for wave end
        if world.check_level_complete():
            world.money += c.EnemyConstants.WAVE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_wave()
            world.process_enemies()

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
            if selected_turret.upgrade_level < c.TurretConstants.TURRET_LEVELS:
                if upgrade_button.draw(screen):
                    if world.money >= c.TurretConstants.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.TurretConstants.UPGRADE_COST
    else:

        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
        if game_win:
            draw_text("GAME OVER", text_font, 'grey0', 0, 0)
        elif not game_win:
            draw_text("CONGRATULATIONS", text_font, 'grey0', 0, 0)
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            can_place_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            enemy_group.empty()
            turret_group.empty()



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
                    #check for money
                    if world.money >= c.TurretConstants.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    pg.display.flip()

pg.quit()
