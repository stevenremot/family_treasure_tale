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
        size: (w, h)
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

    def draw_text(self, text, color, font_size, font_type=None):
        """Draw a text

        color: (r, g, b)
        """
        font = pygame.font.Font(font_type, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect().move(self.x, self.y)
        self.screen.pygame_screen.blit(text_surface, text_rect)
        
        

class Renderable(object):
    """A component for entities that can be drawn on the screen.

    It encapsulates a render function that contains the draw
    instructions. The render function takes a Brush as parameter.

    As some entities must be rendered on top of others, the Renderable
    component also has a layer number. A higher layer will be drawn on
    top of a lower layer.
    """

    def __init__(self, render_func, layer):
        self.render_func = render_func
        self.layer = layer

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
        entities = self.world.get_entities([Positionable, Renderable])

        layer = self.get_minimal_layer(entities)

        while entities:
            layer_entities = [e for e in entities
                              if e.get_component(Renderable).layer == layer]
            self.draw_entity_layer(layer_entities)
            entities = [e for e in entities if e not in layer_entities]
            layer += 1

        self.screen.flip()

    def draw_entity_layer(self, entities):
        """Draw all the entities in the list, in their index order.
        """
        for entity in entities:
            positionable = entity.get_component(Positionable)
            renderable = entity.get_component(Renderable)

            renderable.render_func(
                Brush(self.screen, (positionable.x, positionable.y))
            )

    def get_minimal_layer(self, entities):
        """Return the minimal layer of the entities' renderable components.
        """
        min_layer = None

        for entity in entities:
            layer = entity.get_component(Renderable).layer
            if min_layer is None or min_layer > layer:
                min_layer = layer

        return layer
