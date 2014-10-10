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
from graphics import Colorable, Renderable
from mouse import Hoverable
from geometry import Positionable

def create_text_entity(
        world,
        text,
        color,
        font_size,
        x=0,
        y=0,
        layer=0,
        font_type=None
):
    """ Create a text entity and returns it """
    entity = world.entity()
    entity.add_components(
        get_text_positionable(text, font_size, x, y, font_type),
        Colorable(color),
        Renderable(
            lambda brush, color: brush.draw_text(text, color, font_size, font_type),
            layer
        )
    )
    return entity

def create_hoverable_text_entity(
        world,
        text,
        color1,
        color2,
        font_size,
        x=0,
        y=0,
        layer=0,
        font_type=None
):
    """ Create a text entity with color2 when hovered and color1 elsewhere
    Return the created entity
    """
    entity = create_text_entity(
        world, text, color1, font_size, x, y, layer, font_type)
    entity.add_component(
        Hoverable(
            lambda: entity.get_component(Colorable).set_color(color2),
            lambda: entity.get_component(Colorable).set_color(color1)
        )
    )
    return entity

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

def center_horizontally(entity):
    entity.get_component(Positionable).center_horizontally()
