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
from tile import TileSpace, TilePositionable
from building import toggle_room
from mouse import Hoverable, Clickable, Button

class RoomSwitcher:
    """In charge of switching from a room to another room.
    """
    def __init__(self, world, initial_room):
        self.world = world
        self.current_room = initial_room
        toggle_room(self.world, initial_room)

    def toggle_to_room(self, room):
        toggle_room(self.world, self.current_room)
        toggle_room(self.world, room)
        self.current_room = room

class RoomWidget:
    """In charge of rendering a room in the minimap an handling its
    inputs.
    """
    def __init__(self, room, room_size, switcher):
        self.room = room
        self.room_size = room_size
        self.switcher = switcher
        self.hovered = False

    def draw(self, brush):
        if self.switcher.current_room is self.room:
            brush.draw_rect(
                (192, 192, 0),
                (0, 0),
                self.room_size
            )
        elif self.hovered:
            brush.draw_rect(
                (128, 128, 128),
                (0, 0),
                self.room_size
            )

        brush.draw_rect(
            (255, 255, 255),
            (0, 0),
            self.room_size,
            1
        )

    def toggle_hover(self):
        self.hovered = not self.hovered

    def activate(self):
        self.switcher.toggle_to_room(self.room)

def create_minimap(world, pos, building):
    """Create a new minimap based on the building.
    """
    minimap_tileset = world.entity()
    minimap_tileset.add_components(
        Positionable(pos[0], pos[1], 0, 0),
        TileSpace("minimap", (1, 1))
    )

    switcher = RoomSwitcher(world, building.rooms[0])

    for room in building.rooms:
        room_widget = RoomWidget(room, building.room_size, switcher)
        room_entity = world.entity()
        room_entity.add_components(
            Positionable(0, 0, building.room_size[0], building.room_size[1]),
            Renderable(room_widget.draw, 1),
            TilePositionable("minimap", room.position, 1),
            Hoverable(room_widget.toggle_hover, room_widget.toggle_hover),
            Clickable(room_widget.activate, Button.LEFT)
        )
