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

from ecs import Activable

class MiniMapRenderable:

    """Component for entities that can be rendered on the minimap.
    """
    def __init__(self, render_func):
        """Initialization

        render_func is a function that takes as input a brush and use
        it to draw on the screen.
        """
        self.render_func = render_func

class Room:
    """Room definition.

    This contains its position in the building, and its activated
    windows and doors.
    """

    def __init__(self, position, activated_entities):
        """Initialization.

        position: (x, y)
        activated_entities: List of entities to activate on this room
        (windows, doors).
        """
        self.position = position
        self.activated_entities = activated_entities

class Building:
    """Building definition.
    """
    def __init__(self, rooms, room_size):
        """Initialization

        rooms: a list of Room objects composing the building.
        room_size: the size of all rooms.
        """
        self.rooms = rooms
        self.room_size = room_size

def toggle_room(world, room):
    """Toggle activation of all the activated entities of the room.
    """
    for entity in room.activated_entities:
        entity.get_component(Activable).toggle()
