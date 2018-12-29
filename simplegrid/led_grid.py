#!/usr/bin/env python3
###
# Copyright (c) 2018 James Lu <james@overdrivenetworks.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

from .grid import SerpentineGrid

class LEDGrid(SerpentineGrid):
    """Class to represent a grid of RGB LEDs (like ws281x LED matrices)."""
    def __init__(self, ws281x, pattern, width=16, height=16, **kwargs):
        super().__init__(pattern, width=width, height=height, **kwargs)
        self._ws281x = ws281x

    def set(self, x, y, obj, **kwargs):
        """Sets the contents of the grid point at (x, y)."""
        super().set(x, y, obj, **kwargs)
        idx = self._get_serpentine_point(x, y)

        assert isinstance(obj, tuple), "Only RGB or RGBW tuples can be added to this grid"
        assert len(obj) in (3, 4), "Wrong length of RGB or RGBW tuple"

        self._ws281x.setPixelColorRGB(idx, *obj)
