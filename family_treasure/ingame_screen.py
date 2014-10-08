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

from room import create_room
from building import Room, Building
from minimap import create_minimap

# -----
from geometry import Positionable
from tile import TilePositionable
from graphics import Renderable
from ecs import Activable
from animation import Animable

def create_ingame_screen(world):
    """ Create entities for the ingame screen """
    create_room(world)

    rect = world.entity()
    rect.add_components(
        Positionable(0, 0, 0, 0),
        Renderable(lambda brush: brush.draw_rect((255, 0, 0), (0, 0), (50, 50)), 1),
        TilePositionable("ground", (3, 3), 1),
        Activable(False)
    )

    char_rect = world.entity()
    char_rect.add_components(
        Positionable(0, 0, 0, 0),
        Renderable(lambda brush: brush.draw_rect((0, 0, 255), (0, 0), (40, 80)), 1),
        TilePositionable("ground", (5, 3), 1),
        Activable(False)
    )
    animable = Animable()
    char_rect.add_component(animable)
    animable.add_animation(TileMoveAnimation((2.5, 3), 2))
    

    building = Building(
        [
            Room((0, 0), [rect, char_rect]),
            Room((0, 30), []),
            Room((30, 0), []),
            Room((30, 30), [])
        ],
        (30, 30)
    )

    create_minimap(world, (700, 50), building)
