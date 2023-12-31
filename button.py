import pygame as pg

class Button():
    def __init__(self, x, y, image, single_click):
        self.image =image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw_getclicked(self, surface):
        action = False

        #get mouse
        pos = pg.mouse.get_pos()
        #check click cond
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0] == 1 and not self.clicked:
            action = True
            if self.single_click:
                self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw
        surface.blit(self.image, self.rect)

        return action