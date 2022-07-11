"""
    Follow Me activity for Sugar
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# imgClick.py
# eg click_img=ImgClickClass(img,(x,y)) (x,y)=top left
#   if click_img.mouse_on():
#   click_img.draw(gscreen)

import pygame

import g


class ImgClick:  # for clickable images
    def __init__(self, img, x1, y1, centre=False):
        w = img.get_width()
        h = img.get_height()
        x = x1
        y = y1
        if centre:
            x = x - w / 2
            y = y - h / 2
            self.cx = x1
            self.cy = y1
        else:
            self.cx = x + w / 2
            self.cy = y + h / 2
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.img = img
        self.w = w
        self.h = h

    def mouse_on(self):
        return self.rect.collidepoint(g.pos)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def mouse_set(self):
        pygame.mouse.set_pos((self.cx, self.cy))
        g.pos = (self.cx, self.cy)
