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
from mouse import Clickable, Button
from animation import TileMoveAnimation, SpriteAnimation, Animable


def create_ingame_screen(world):
    """ Create entities for the ingame screen """
    create_room(world)

    animable = Animable()
    
    boy = world.entity()
    boy.add_components(
        Positionable(0, 0, 40, 80),
        Renderable(
            lambda brush: brush.draw_image("boy.png"),
            2
        ),
        TilePositionable("ground", (3, 1), 2),
        animable,
        Clickable(
            lambda: animable.add_animations(
                TileMoveAnimation((0,5), 5),
                SpriteAnimation(5, 3, ["move_1.png", "move_2.png"])
            ),
            Button.LEFT
        )
    )

    char_rect = world.entity()
    char_rect.add_components(
        Positionable(0, 0, 0, 0),
        Renderable(lambda brush: brush.draw_rect((0, 0, 255), (0, 0), (40, 80)), 1),
        TilePositionable("ground", (5, 3), 1),
        Activable(False)
    )
    animable2 = Animable()
    char_rect.add_component(animable2)
    animable2.add_animation(TileMoveAnimation((2.5, 3), 2))
    

    building = Building(
        [
            Room((0, 0), [char_rect]),
            Room((0, 30), []),
            Room((30, 0), []),
            Room((30, 30), [])
        ],
        (30, 30)
    )

    create_minimap(world, (700, 50), building)
