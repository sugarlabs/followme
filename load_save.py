# load_save.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import logging

import g

loaded = []  # list of strings


def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except Exception as e:
        logging.error('Could not readlines: %s' % (e))


def save(f):
    f.write(str(g.best) + '\n')
    f.write(str(g.level) + '\n')


def retrieve():
    global loaded
    if len(loaded) > 1:
        g.best = int(float(loaded[0].strip()))
        g.level = int(float(loaded[1].strip()))
