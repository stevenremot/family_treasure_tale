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
from geometry import Positionable

class Screen(object):
    """Represents the game screen.
    """

    def __init__(self, size):
        self.pygame_screen = pygame.display.set_mode(size)

    def fill(self, color):
        """Fill the screen with some color.
        """
        self.pygame_screen.fill(color)

    def flip(self):

        """Update screen with previously applied draw operations.
        """
        pygame.display.flip()

class Brush(object):
    """A helper class to draw things on screen.
    """

    def __init__(self, screen, pos):
        """Initialization

        screen: Object of type Screen
        pos: (x, y)
        """
        self.screen = screen
        self.pos = pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def draw_rect(self, color, pos, size):
        """Draw a rectangle

        color: (r, g, b)
        pos: (x, y)
        size: (x, h)
        """
        pygame.draw.rect(
            self.screen.pygame_screen,
            color,
            pygame.Rect(
                pos[0] + self.x,
                pos[1] + self.y,
                size[0],
                size[1]
            )
        )

class Renderable(object):
    """A component for entities that can be drawn on the screen.

    It encapsulates a render function that contains the draw
    instructions. The render function takes a Brush as parameter.

    """

    def __init__(self, render_func):
        self.render_func = render_func

class GraphicsSystem(object):
    """System in charge of drawing entities on the screen.
    """

    def __init__(self, world, screen):
        self.world = world
        self.screen = screen

    def draw_entities(self):
        """Draw the renderable entities on the screen.
        """
        self.screen.fill((0, 0, 0))
        for entity in self.world.get_entities([Positionable, Renderable]):
            positionable = entity.get_component(Positionable)
            renderable = entity.get_component(Renderable)

            renderable.render_func(
                Brush(self.screen, (positionable.x, positionable.y))
            )
        self.screen.flip()
