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


class RC():
    def __init__(self, nr, nc):
        self.nr = nr
        self.nc = nc

    def inc_r(self, ind):
        r, c = self.row_col(ind)
        r += 1
        if r == self.nr:
            r = 0
        if r == (self.nr - 1) and c == (self.nc - 1):
            r = 0
        return self.indx(r, c)

    def dec_r(self, ind):
        r, c = self.row_col(ind)
        r -= 1
        if r < 0:
            r = self.nr - 1
        if r == (self.nr - 1) and c == (self.nc - 1):
            r = self.nr - 2
        return self.indx(r, c)

    def inc_c(self, ind):
        r, c = self.row_col(ind)
        c += 1
        if c == self.nc:
            c = 0
        if r == (self.nr - 1) and c == (self.nc - 1):
            c = 0
        return self.indx(r, c)

    def dec_c(self, ind):
        r, c = self.row_col(ind)
        c -= 1
        if c < 0:
            c = self.nc - 1
        if r == (self.nr - 1) and c == (self.nc - 1):
            c = self.nc - 2
        return self.indx(r, c)

    def row_col(self, ind):
        i = 0
        for r in range(self.nr):
            for c in range(self.nc):
                if i == ind:
                    return r, c
                i += 1

    def indx(self, r, c):
        return r * self.nc + c
