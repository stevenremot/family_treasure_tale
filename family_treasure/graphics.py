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

class Screen(object):
    """Represents the game screen.
    """

    def __init__(self, size):
        self.pygame_screen = pygame.display.set_mode(size)

    def fill(self, color):
        """Fill the screen with some color.
        """
        self.pygame_screen.fill(color)

    def do_in_pygame(self, render_func):
        """Apply render_func to the pygame screen.

        render_func is a function that takes a pygame screen as
        parameter.
        """
        render_func(self.pygame_screen)

    def flip(self):
        """Update screen with previously applied draw operations.
        """
        pygame.display.flip()
