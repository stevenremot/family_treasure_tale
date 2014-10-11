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
import data

from geometry import Positionable
from ecs import Activable


class Screen(object):
    """Represents the game screen.
    """

    def __init__(self, size):
        pygame.display.set_icon(
            pygame.image.load(data.filepath("ftt_icon.png"))
        )
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

    def __init__(self, screen, pos, sprite_dict):
        """Initialization

        screen: Object of type Screen
        pos: (x, y)
        sprite_dict: a dicitionary of pygame.Surface indexed by sprite names
        """
        self.screen = screen
        self.pos = pos
        self.sprite_dict = sprite_dict

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def draw_rect(self, color, pos, size, stroked=False):
        """Draw a rectangle

        color: (r, g, b)
        pos: (x, y)
        size: (w, h)
        """
        if stroked:
            pygame.draw.rect(
                self.screen.pygame_screen,
                color,
                pygame.Rect(
                    pos[0] + self.x,
                    pos[1] + self.y,
                    size[0],
                    size[1]
                ),
                1
            )
        else:
            s = pygame.Surface(size, pygame.SRCALPHA)
            s.fill(color)
            self.screen.pygame_screen.blit(
                s,
                (pos[0] + self.x, pos[1] + self.y)
            ) 

    def draw_text(self, text, color, font_size, font_type=None):
        """Draw a text

        color: (r, g, b)
        """
        font = pygame.font.Font(font_type, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect().move(self.x, self.y)
        self.screen.pygame_screen.blit(text_surface, text_rect)

    def draw_image(self, filename, offset=(0, 0)):
        """ Draw an image
        Use pygame.image.load when the sprite has not been loaded
        Then, get the pygame.Surface in the sprite dictionary
        """
        if filename in self.sprite_dict:
            surface = self.sprite_dict[filename]
        else:
            surface = pygame.image.load(data.filepath(filename)).convert_alpha()
            self.sprite_dict[filename] = surface

        rect = surface.get_rect().move(self.x + offset[0], self.y + offset[1])
        self.screen.pygame_screen.blit(surface, rect)

    def blit(self, surface, rect):
        """Do things with the pygame way"""
        self.screen.pygame_screen.blit(surface, rect)

    def get_translated(self, dx, dy):
        """Return a new brush with an offset of dx, dy.
        """
        return Brush(self.screen, (self.x + dx, self.y + dy))


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

    def render_image(self, image, offset=(0, 0)):
        """A helper function to make renderable render an image.
        """
        self.render_func = lambda brush: brush.draw_image(image, offset)


class Colorable(object):
    """A component for monochrome renderable entities.
    It encapsulates their color"""

    def __init__(self, c):
        """ c = (r,g,b[, a])
        """
        self.color = c

    def set_color(self, c):
        self.color = c


class GraphicsSystem(object):
    """System in charge of drawing entities on the screen.
    """

    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.sprite_dict = {}

    def draw_entities(self):
        """Draw the renderable entities on the screen.
        """
        self.screen.fill((0, 0, 0))
        entities = self.world.get_entities([Positionable, Renderable])
        entities.sort(key=lambda e: e.get_component(Renderable).layer)
        for entity in entities:
            if self.is_entity_activated(entity):
                positionable = entity.get_component(Positionable)
                renderable = entity.get_component(Renderable)
                brush = Brush(
                    self.screen,
                    (positionable.x, positionable.y),
                    self.sprite_dict
                )

                if entity.has_component(Colorable):
                    colorable = entity.get_component(Colorable)
                    renderable.render_func(brush, colorable.color)
                else:
                    renderable.render_func(brush)

        self.screen.flip()

    def is_entity_activated(self, entity):
        """Return true if the entity is activated.
        """
        return not entity.has_component(Activable) or entity.get_component(Activable).activated

    def get_minimal_layer(self, entities):
        """Return the minimal layer of the entities' renderable components.
        """
        min_layer = None

        for entity in entities:
            layer = entity.get_component(Renderable).layer
            if min_layer is None or min_layer > layer:
                min_layer = layer

        return layer

    def load_charset_row(
            self,
            row_number,
            row_name,
            filename,
            charset_surface,
            sprite_size,
            sprites_per_row
    ):
        w,h = sprite_size
        partition = filename.partition('.')
        base_name = partition[0] + "_" + row_name + "_"
        extension = partition[1] + partition[2]

        rect = pygame.Rect(0, row_number*h, w, h)
        surface_idle = charset_surface.subsurface(rect)
        self.sprite_dict[base_name+"idle"+extension] = surface_idle

        for n in range(1, sprites_per_row):
            rect = pygame.Rect(n*w, row_number*h, w, h)
            surface = charset_surface.subsurface(rect)
            name = base_name + "move_" + str(n) + extension
            self.sprite_dict[name] = surface

    def load_charset(self, filename, sprite_size, row_names = ["t","b","l","r"]):
        """
        Create entries in sprite_dict for the different sprites of the
        charset
        The fake filenames are named:
        filename_t_idle.png: idle sprite for top->bottom orientation
        filename_t_move_n.png: nth move sprite for top->bottom orientation

        The charset is supposed to be organised like this:
        first row: top -> bottom orientation
        second row: bottom -> top orientation
        third row: left -> right orientation
        fourth rom: right -> left orientation
        Each row contains first an idle sprite, then several movement sprites
        sprite_size is the size of a single sprite of the charset
        """
        charset_surface = pygame.image.load(data.filepath(filename)).convert_alpha()
        sprites_per_row = charset_surface.get_rect().width / sprite_size[0]

        for i in range(len(row_names)):
            self.load_charset_row(
                i,
                row_names[i],
                filename,
                charset_surface,
                sprite_size,
                sprites_per_row
            )

    def load_four_orientations(self, filename):
        """ Create entries in sprite_dict corresponding to the four
        orientations of the input image.
        The image is supposed to be some object that is bound
        to the walls (door, window, etc) and correspond to the
        top wall version of the sprite.
        Four pygame.Surface are created and labelled:
        filename_t.png, filename_b.png, filename_l.png, filename_r.png
        """
        partition = filename.partition('.')
        base_name = partition[0]
        extension = partition[1] + partition[2]

        top_surface = pygame.image.load(data.filepath(filename)).convert_alpha()
        self.sprite_dict[base_name + "_t" + extension] = top_surface

        left_surface = pygame.transform.rotate(top_surface, 90)
        self.sprite_dict[base_name + "_l" + extension] = left_surface

        bottom_surface = pygame.transform.rotate(left_surface, 90)
        self.sprite_dict[base_name + "_b" + extension] = bottom_surface

        right_surface = pygame.transform.rotate(bottom_surface, 90)
        self.sprite_dict[base_name + "_r" + extension] = right_surface
