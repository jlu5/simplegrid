#!/usr/bin/env python3
###
# Copyright (c) 2015-2018 James Lu <james@overdrivenetworks.com>

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

"""Grid system using nested lists (version 2)."""

from __future__ import print_function
import itertools
import sys
import enum

if sys.version_info[0] >= 3:
    raw_input = input
    xrange = range

class GridItemFilledError(ValueError):
    # Raised when a grid point we requested is already filled.
    pass

class CartesianDirection(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Grid():
    """Grid system using nested lists."""
    def __init__(self, width=3, height=3, data=None):
        """
        Initialize the grid. For the Cartesian grid, the backend is a list of lists:
        each row is a list element inside the outside list, and its elements refer
        to individual grid positions.

        Unless data is given, grid positions are initialized to empty strings.
        e.g. a 3x3 grid defaults to:
            [['', '', ''], ['', '', ''], ['', '', '']]

        The origin point (0, 0) is assumed to be the top left. The coordinates for a 3x3
        grid would thus be the following:
           [[(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)]]
        """
        if data is None:
            self._grid = [['' for _ in xrange(width)] for _ in xrange(height)]
        else:
            self._grid = data
        self.width = width
        self.height = height

        # Store the length of the largest item that's ever been added to the
        # grid, so that grid cells are formatted with the right widths.
        # 3 is a good default since it gives the grid ample space to start,
        # but it will grow if bigger strings are stored.
        self.largestlength = 3

    def _get_coordinate(self, x, y):
        """
        Fetches the value of the point at (x, y) using a Cartesian grid system.
        """
        return self._grid[y][x]

    def get(self, x, y):
        """Returns the contents of the grid item at (x, y)."""
        if x < 0 or x >= self.width:
            raise IndexError("Width out of grid range")
        elif y < 0 or y >= self.height:
            raise IndexError("Height out of grid range")
        return self._get_coordinate(x, y)

    def _set_coordinate(self, x, y, obj):
        """
        Sets the point at (x, y) to the given object.
        """
        self._grid[y][x] = obj

    def set(self, x, y, obj, allowOverwrite=False):
        """Sets the contents of the grid item at (x, y)."""
        if x < 0 or x >= self.width:
            raise IndexError("Width out of grid range")
        elif y < 0 or y >= self.height:
            raise IndexError("Height out of grid range")

        if (not allowOverwrite) and self._get_coordinate(x, y):
            raise GridItemFilledError("Coordinates requested have already been filled.")

        objectlength = len(str(obj))
        # If the length of the object is greater than the largest length we've
        # seen so far, update the length. This is used for grid formatting
        # purposes, so that each cell has the right width.
        if objectlength > self.largestlength:
            self.largestlength = objectlength

        self._set_coordinate(x, y, obj)

    def show(self):
        """
        Prints the current grid to screen.

        For unused squares, show the number of the coordinate instead.
        This way, a blank 3 by 3 grid gets shown as:
        |---|---|---|
        | 1 | 2 | 3 |
        |---|---|---|
        | 4 | 5 | 6 |
        |---|---|---|
        | 7 | 8 | 9 |
        |---|---|---|, instead of each item being empty.
        """
        # Print the dividing bar with the right cell width between every row:
        #    |---|---|---|
        print('|%s' % ('-' * self.largestlength) * self.width + '|')

        for rowpos in range(self.height):
            for colpos in range(self.width):
                print('|', end='')
                value = self.get(colpos, rowpos)

                # Show the grid position if no value is set
                # Note: show numerical 0 values as is
                place = "%s,%s" % (colpos, rowpos)
                if value is None or value == '':
                    output = place
                else:
                    output = str(value)
                #output = place

                output = output.center(max(len(place), self.largestlength), ' ')
                print(output, end='')
            print('|')
            print('|%s' % ('-' * self.largestlength) * self.width + '|')

    def __repr__(self):
        """Overrides string conversion to show the Grid's elements."""
        return "Grid(%s)" % self._grid

    def all_items(self):
        """Returns all the items in the grid, reduced into one list."""
        return list(itertools.chain.from_iterable(self._grid))

    def by_rows(self):
        """Returns the items in the grid as a list of lists, with each inner list
        representing a row."""
        return self._grid

    def next_in_direction(self, x, y, direction):
        """Returns the grid point one in the specified direction, or raise
        IndexError if that is out of the grid."""
        new_x, new_y = x, y
        if direction == CartesianDirection.LEFT:
            new_x -= 1
        elif direction == CartesianDirection.RIGHT:
            new_x += 1
        elif direction == CartesianDirection.UP:
            new_y -= 1
        elif direction == CartesianDirection.DOWN:
            new_y += 1

        if new_x < 0 or new_x >= self.width:
            raise IndexError("Width out of grid range")
        elif new_y < 0 or new_y >= self.height:
            raise IndexError("Height out of grid range")

        return (new_x, new_y)

class SerpentinePattern(enum.Enum):
    """Enum referring to serpentine pattern start points common in LED matrix boards."""
    #top left
    #  0  1  2  3  4  5  6  7
    # 15 14 13 12 11 10  9  8
    # 16 17 18 19 20 21 22 23
    # 31 30 29 28 27 26 25 24
    # 32 33 34 35 36 37 38 39
    #                  bottom right
    TOP_LEFT = 1

    #top left
    #  7  6  5  4  3  2  1  0
    #  8  9 10 11 12 13 14 15
    # 23 22 21 20 19 18 17 16
    # 24 25 26 27 28 29 30 31
    # 39 38 37 36 35 34 33 32
    #                  bottom right
    TOP_RIGHT = 2

class SerpentineGrid(Grid):
    def __init__(self, pattern, width=3, height=3, data=None):
        super().__init__(width=width, height=height)
        # Our backend in this case will just be one long array.
        if data is None:
            self._grid = ['' for _ in xrange(width*height)]
        else:
            self._grid = data

        self.pattern = pattern

    def _get_serpentine_point(self, x, y):
        """
        Fetches the array index of the point (x, y) using a Serpentine grid system.
        """
        coord = (y * self.height)

        # In TOP_RIGHT mode, even rows go in reverse and odd ones go forwards
        if self.pattern == SerpentinePattern.TOP_RIGHT:
            if (y % 2 == 0):
                coord += (self.width - x - 1)
            else:
                coord += x
        # In TOP_LEFT mode, even rows go forwards and odd ones are in reverse
        elif self.pattern == SerpentinePattern.TOP_LEFT:
            if (y % 2 == 0):
                coord += x
            else:
                coord += (self.width - x - 1)

        return coord

    def _get_coordinate(self, x, y):
        """
        Fetches the value of the point at (x, y) using a Serpentine grid system.
        """
        coord = self._get_serpentine_point(x, y)
        return self._grid[coord]

    def _set_coordinate(self, x, y, obj):
        """
        Sets the point at (x, y) to the given object.
        """
        coord = self._get_serpentine_point(x, y)
        self._grid[coord] = obj

    def all_items(self):
        """Returns all the items in the grid."""
        return self._grid

    def by_rows(self):
        """Returns the items in the grid as a list of lists, with each inner list
        representing a row."""
        resultgrid = []
        for y in range(self.height):
            resultgrid.append([self.get(x, y) for x in range(self.width)])
        return resultgrid

if __name__ == '__main__':
    print("This module provides no command line functions.")
