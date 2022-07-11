#!/usr/bin/python
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

from gi.repository import Gtk
import sys
import pygame

import g
import utils
import simon
import buttons
import slider
import load_save
import rc_skip_last


class FollowMe:

    def __init__(self, colors, sugar=False):
        self.colors = colors
        self.sugar = sugar
        self.journal = True  # set to False if we come in via main()
        self.canvas = None

    def display(self):
        g.screen.fill(self.colors[1])
        if self.aim.running or self.aim.glow_active:
            pass
        for img in g.imgs:  # img from ImgClick (centred)
            img.draw(g.screen)
        if g.wrong:
            img = g.imgs[g.wrong_ind]
            utils.centre_blit(g.screen, g.wrong_img, (img.cx, img.cy))
            img = g.imgs[g.right_ind]
            utils.centre_blit(g.screen, g.glowy[g.right_ind], (img.cx, img.cy))
        if not self.sugar:
            buttons.draw()
            self.slider.draw()
        self.ladder()
        self.aim.glow()
        self.player.glow(True)

    def do_click(self):
        self.glow_off()
        if self.click():
            return
        if not self.sugar:
            bu = buttons.check()
            if bu != '':
                self.do_button(bu)
                return
            if self.slider.mouse():
                self.set_delay()

    def set_buttons(self, green, back):
        ''' Called from Sugar: associate toolbar buttons with app '''
        self.green_button = green
        self.back_button = back

    def do_button(self, bu):
        if bu == 'green':  # start
            self.aim.new1()
            g.player_n = 0
            g.wrong = False
            g.score = 0
            if self.sugar:
                self.green_button.set_sensitive(True)
                self.back_button.set_sensitive(False)
            else:
                buttons.off('green')
                buttons.on('back')
        elif bu == 'back':
            self.aim.start()  # show again

    def do_key(self, key):
        if key in g.TICK:
            self.change_level()
            self.set_delay()
            return
        if key == pygame.K_v:
            g.version_display = not g.version_display
            return
        if self.aim.running or self.aim.glow_active:
            return
        if key in g.CROSS:
            self.do_click()
            return
        if key in g.SQUARE:
            if self.sugar:
                if self.green_button.get_sensitive():
                    self.do_button('green')
                    return
                elif self.back_button.get_sensitive():
                    self.do_button('back')
                    return
            else:
                if buttons.active('green'):
                    self.do_button('green')
                    return
                if buttons.active('back'):
                    self.do_button('back')
                    return
        if key in g.RIGHT:
            g.green = self.rc.inc_c(g.green)
            g.imgs[g.green].mouse_set()
        if key in g.LEFT:
            g.green = self.rc.dec_c(g.green)
            g.imgs[g.green].mouse_set()
        if key in g.UP:
            g.green = self.rc.dec_r(g.green)
            g.imgs[g.green].mouse_set()
        if key in g.DOWN:
            g.green = self.rc.inc_r(g.green)
            g.imgs[g.green].mouse_set()

    def mouse_set(self):
        ind = 0
        for imgc in g.imgs:
            if imgc.mouse_on():
                g.green = ind
                return
            ind += 1

    def change_level(self):
        g.level += 1
        if not self.sugar:
            if g.level > self.slider.steps:
                g.level = 1

    def ladder(self):
        if g.score > g.best:
            g.best = g.score
        if g.best > 11:
            cx = g.sx(30.55)
            cy = g.sy(13.25)
            utils.centre_blit(g.screen, g.star, (cx, cy))
            utils.display_number(g.best, (cx, cy), g.font2)
        if g.score > 0:
            n = g.score - 1
            if n > 11:
                n = 11
            g.screen.blit(g.ladder, (g.sx(26.95), g.sy(13.7)))
            x = g.man_x0 + n * g.man_dx
            y = g.man_y0 + n * g.man_dy
            g.screen.blit(g.man, (x, y))
            cx = x + g.man_sc_dx
            cy = y + g.man_sc_dy
            if g.score < g.best or g.best < 12:
                utils.centre_blit(g.screen, g.star, (cx, cy))
                utils.display_number(g.score, (cx, cy), g.font2)

    def which(self):
        ind = 0
        for img in g.imgs:
            if img.mouse_on():
                return ind
            ind += 1
        return -1  # none clicked

    def click(self):
        if self.aim.running:
            return False
        if g.wrong:
            return False
        ind = self.which()
        if ind == -1:
            return False
        if len(self.aim.list1) == 0:
            return False
        self.player.glow_start(ind)
        if self.sugar:
            self.back_button.set_sensitive(False)
        else:
            buttons.off('back')
        if ind == self.aim.list1[g.player_n]:
            g.player_n += 1
            if g.player_n > g.score:
                g.score = g.player_n
            if g.player_n == len(self.aim.list1):  # all correct - add another
                self.aim.inc()
                g.player_n = 0
        else:
            g.wrong = True
            g.wrong_ind = ind
            g.right_ind = self.aim.list1[g.player_n]
            if self.sugar:
                self.green_button.set_sensitive(True)
            else:
                buttons.on('green')
        return True  # click processed

    def glow_off(self):
        self.aim.glow_off()
        self.player.glow_off()

    def set_delay(self, value=None):
        if value is None:
            self.aim.glow_time = (4 - g.level) * 500 - 300
            self.aim.delay = (4 - g.level) * 330
        else:
            self.aim.glow_time = value
            self.aim.delay = int(value * 1.5)

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def g_init(self):
        g.init()

    def save_pattern(self):
        self.pattern = self.aim.list1[:]

    def restore_pattern(self):
        self.aim.list1 = self.pattern[:]

    def run(self, restore=False):
        self.g_init()
        if not self.journal:
            utils.load()
        load_save.retrieve()
        self.aim = simon.Simon(1200)  # arg is glow time
        if self.sugar:
            self.set_delay(800)
        else:
            self.set_delay()
        self.player = simon.Simon(200)
        if restore:
            self.restore_pattern()
            self.aim.started = True
        if self.sugar:
            self.green_button.set_sensitive(True)
            self.back_button.set_sensitive(False)
        else:
            bx = g.sx(22.42)
            by = g.sy(20.8)
            buttons.Button('green', bx, by, True)
            buttons.Button('back', bx, by, True)
            buttons.off('back')
            self.slider = slider.Slider(g.sx(9), g.sy(20.8), 3, utils.BLUE)
        self.rc = rc_skip_last.RC(3, 5)
        if self.canvas is not None:
            self.canvas.grab_focus()
        ctrl = False
        pygame.key.set_repeat(600, 120)
        key_ms = pygame.time.get_ticks()
        going = True
        while going:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.journal:
                        utils.save()
                    going = False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()
                    self.mouse_set()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw = True
                    if event.button == 1:
                        self.do_click()
                        self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks() - key_ms > 110:
                        key_ms = pygame.time.get_ticks()
                        if ctrl:
                            if event.key == pygame.K_q:
                                if not self.journal:
                                    utils.save()
                                going = False
                                break
                            else:
                                ctrl = False
                        if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                            ctrl = True
                            break
                        self.do_key(event.key)
                        g.redraw = True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl = False
            if not going:
                break
            if self.sugar:
                if g.player_n == 0 and not self.green_button.get_sensitive():
                    self.back_button.set_sensitive(True)
            else:
                if g.player_n == 0 and not buttons.active('green'):
                    buttons.on('back')
            self.player.do()
            self.aim.do()
            if g.redraw:
                self.display()
                if g.version_display:
                    utils.version_display()
                if self.aim.running or self.aim.glow_active:
                    pass
                else:
                    g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False
            g.clock.tick(40)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
    global colors
    game = FollowMe(([0, 255, 255], [0, 255, 0]))
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
