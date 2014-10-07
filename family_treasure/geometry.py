# This file is part of The Family's treasure tale.

# The Family's treasure tale is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# The Family's treasure tale is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with The Family's treasure tale.  If not, see
# <http://www.gnu.org/licenses/>.

import pygame

class Positionable(object):
    """Component for entities that have a position at screen.
    """

    def __init__(self, x, y, w, h):
        """Initialization

        x: left
        y: top
        w: width
        h: height
        """
        self.rect = pygame.Rect(x, y, w, h)

    @property
    def x(self):
        return self.rect.left

    @x.setter
    def x(self, x):
        self.rect.left = x

    @property
    def y(self):
        return self.rect.top

    @y.setter
    def y(self, y):
        self.rect.top = y

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height):
        self.rect.height = height

    @property
    def pygame_rect(self):
        return self.rect

    def contains(self, x, y):
        return self.rect.collidepoint(x, y)

    def contains(self, pos):
        return self.rect.collidepoint(pos)

def get_text_positionable(text, font_size, x=0, y=0, font_type=None):
    """ Use pygame to compute the width and height of a text entity """
    font = pygame.font.Font(font_type, font_size)
    pygame_rect = font.render(text, False, (255, 0, 0)).get_rect().move(x, y)
    return Positionable(
        pygame_rect.left,
        pygame_rect.top,
        pygame_rect.width, 
        pygame_rect.height
    )
