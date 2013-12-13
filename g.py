# g.py - globals
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import logging
import random
import pygame

import utils
import imgClick

app = 'Follow Me'
ver = '1.0'
ver = '1.1'
# new bgd
# ladder
ver = '1.2'
# scaled font @ imgf
# man on ladder
# green bgd -> new buttons
ver = '1.3'
# star separate & left @ top
ver = '1.4'  # <<<< Release 3
# added magician pic
ver = '1.5'
# magician -> object
# speed slider
# change green button colour
ver = '1.5'
# rationalised g.py
# no Esc on XO
# simon.py - delay also controlled by slider
# save level
ver = '2.0'
# sugar coated
# got this to work ok BUT cursor flickers
ver = '2.1'
# added journal switch
# swapped me & grapes
# added version display for right click
ver = '2.2'
# cf Boxes
ver = '2.3'
# app title
ver = '2.4'
# yellow glow for player & longer
# increased glow size
# random seed
ver = '3.0'
# redraw implemented
ver = '4.0'
# new sugar cursor etc
ver = '21'
# bigger white glow
# no pointer or rectangle while leading
ver = '22'
# flush_queue() doesn't use gtk on non-XO
ver = '24'
# sugar stylelized (broken in gnome)

UP = (264, 273)
DOWN = (258, 274)
LEFT = (260, 276)
RIGHT = (262, 275)
CROSS = (259, 120)
CIRCLE = (265, 111)
SQUARE = (263, 32)
TICK = (257, 13)


def init():  # called by main()
    random.seed()
    global redraw
    global screen, w, h, font1, font2, clock, click_snd
    global factor, offset, imgf, message, version_display
    global pos, pointer
    redraw = True
    version_display = False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70, 0, 70))
    pygame.display.flip()
    w, h = screen.get_size()
    logging.debug('%d,  %d' % (w, h))
    if float(w) / float(h) > 1.5:  # widescreen
        offset = (w - 4 * h / 3) / 2  # we assume 4:3 - centre on widescreen
    else:
        h = int(.75 * w)  # allow for toolbar - works to 4:3
        offset = 0
    clock = pygame.time.Clock()
    factor = float(h) / 24  # measurement scaling factor (32x24 =
                            # design units)
    offset = (w - 4 * h / 3) / 2  # we assume 4:3 - centre on widescreen
    imgf = float(h) / 900  # image scaling factor - images built for 1200x900
    if pygame.font:
        t = int(54 * imgf)
        font1 = pygame.font.Font(None, t)
        t = int(48 * imgf)
        font2 = pygame.font.Font(None, t)
    message = ''
    pos = pygame.mouse.get_pos()
    pointer = utils.load_image('pointer.png', True)
    pygame.mouse.set_visible(False)

    # this activity only
    global imgs, glow, glowy, wrong_img, man, ladder, star, score
    global man_x0, man_y0, man_dx, man_dy, man_sc_dx, man_sc_dy
    global wrong, player_n, best, level
    global max_w, max_h, green
    wrong_img = utils.load_image('wrong.png', True)
    man = utils.load_image('man.png', True)
    man_x0 = sx(25.5)
    man_y0 = sy(18.31)
    man_dx = (sx(27.87) - man_x0) / 11.0
    man_dy = (sy(12.15) - man_y0) / 11.0
    man_sc_dx = sx(25.38) - man_x0
    man_sc_dy = sy(18.61) - man_y0
    ladder = utils.load_image('ladder.png', True)
    star = utils.load_image('star.png', True)
    cy = sy(3.2)
    dx = sy(6.4)
    dy = sy(6.2)
    i = 1
    score = 0
    best = 0
    level = 1
    imgs = []
    glow = []
    glowy = []
    max_w = 0
    max_h = 0
    for r in range(1, 4):
        cx = sx(3.2)
        for c in range(1, 6):
            img = utils.load_image(str(i) + '.png', True)
            imgC = imgClick.ImgClick(img, (cx, cy), True)
            if imgC.w > max_w:
                max_w = imgC.w
            if imgC.h > max_h:
                max_h = imgC.h
            imgs.append(imgC)
            glow.append(utils.load_image(str(i) + '.png', True, 'glow'))
            glowy.append(utils.load_image(str(i) + '.png', True, 'glowy'))
            cx += dx
            i += 1
            if i == 15:
                break
        cy += dy
    player_n = 0  # player click counter
    wrong = False
    green = 0
    imgs[green].mouse_set()


def sx(f):  # scale x function
    return int(f * factor + offset + .5)


def sy(f):  # scale y function
    return int(f * factor + .5)
