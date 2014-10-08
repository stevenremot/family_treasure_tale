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

from geometry import Positionable
from graphics import Renderable

class TileSpace(object):
    """Component for an entity that represents a tile space.

    A tile space is a high-level 3-d coordinate space that represents
    a grid at a macro-level (ex: 1 unit ~= 1 meter)
    """

    def __init__(self, name, ratio):
        """Initialization

        The name is used to refer to this tile space.

        The ratio is a tile pixel / unit ratio. For example, a ratio
        of 2 means 2 pixels for 1 unit. The ratio may not be the same
        for x and y, so it is a tuple (ratio_x, ratio_y)

        """
        self.name = name
        self.ratio = ratio

class TilePositionable(object):
    """Component for entities that have a position in a tile system.
    """

    def __init__(self, tile_space_name, pos, layer):
        """Initialization

        tile_space_name: The name of the tile space to use
        pos : (x, y)
        layer : On the same cell, a higher layer will be drawn on the top
        """
        self.tile_space_name = tile_space_name
        self.pos = pos
        self.layer = layer

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, x):
        self.pos = (x, self.pos[1])

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, y):
        self.pos = (self.pos[0], y)

class TileSystem(object):
    """System in charge of updating on-screen position of tile objects.
    """

    def __init__(self, world, layers_per_cell):
        self.world = world
        self.layers_per_cell = layers_per_cell

    def update_tile_positions(self):
        """Update Positionable and Renderable entities with tile information.
        """
        tile_spaces = self.get_tile_spaces()
        tile_entities = self.get_tile_positionable_entities()

        for entity in tile_entities:
            tile_component = entity.get_component(TilePositionable)
            self.update_entity(
                entity,
                tile_spaces[tile_component.tile_space_name]
            )

    def update_entity(self, entity, tile_space):
        """Update entity's coordinates with tile information.
        """
        tile_component = entity.get_component(TilePositionable)
        positionable = entity.get_component(Positionable)
        renderable = entity.get_component(Renderable)

        left = tile_space["x"] + tile_component.x * tile_space["ratio"][0]
        top = tile_space["y"] + tile_component.y * tile_space["ratio"][1]
        positionable.x = left
        positionable.y = top

        renderable.layer = tile_component.y * self.layers_per_cell + tile_component.layer

    def get_tile_spaces(self):
        """Return a dictionary whose keys are space names, and values are
        tile space data (x, y, and ratio).
        """
        spaces = {}
        for entity in self.world.get_entities([Positionable, TileSpace]):
            component = entity.get_component(TileSpace)
            position = entity.get_component(Positionable)
            spaces[component.name] = {
                "x": position.x,
                "y": position.y,
                "ratio": component.ratio
            }
        return spaces

    def get_tile_positionable_entities(self):
        """Return a list of the entities wich can be updated.
        """
        return self.world.get_entities([
            Positionable,
            Renderable,
            TilePositionable
        ])
