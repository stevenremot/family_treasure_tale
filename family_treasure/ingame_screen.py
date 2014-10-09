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
from sky import create_sky_effect

# -----
from geometry import Positionable
from tile import TilePositionable
from graphics import Renderable, Colorable
from ecs import Activable
from mouse import Clickable, Button
from animation import TileMoveAnimation, SpriteAnimation, Animable, ColorAnimation

def create_building(world, scenario_state):
    up_door = world.entity()
    up_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2.png"),
            3
        ),
        TilePositionable("wall", (3, 1), 3),
        Activable(False)
    )

    left_door = world.entity()
    left_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_l.png"),
            3
        ),
        TilePositionable("wall", (0, 6), 3),
        Activable(False)
    )

    down_door = world.entity()
    down_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_b.png"),
            3
        ),
        TilePositionable("wall", (5, 10), 3),
        Activable(False)
    )

    right_door = world.entity()
    right_door.add_components(
        Positionable(0, 0, 100, 50),
        Renderable(
            lambda brush: brush.draw_image("door2_r.png"),
            3
        ),
        TilePositionable("wall", (12, 6), 3),
        Activable(False)
    )

    window = world.entity()
    window.add_components(
        Positionable(0, 0, 100, 100),
        Renderable(
            lambda brush: brush.draw_image("window.png"),
            1
        ),
        TilePositionable("wall", (7, 1), 1),
        Activable(False)
    )

    building = Building(
        [
            Room((0, 0), [left_door, right_door, down_door, window]),
            Room((0, 30), [up_door]),
            Room((30, 0), [left_door, down_door]),
            Room((30, 30), [up_door])
        ],
        (30, 30)
    )

    create_minimap(world, (700, 50), building)

def create_ingame_screen(world, scheduler):
    """ Create entities for the ingame screen """
    create_room(world)
    scenario_state = {}

    banimable = Animable()
    anim_list = ["boy_l_idle.png","boy_l_move_1.png", "boy_l_move_2.png"]

    boy = world.entity()
    boy.add_components(
        Positionable(0, 0, 40, 80),
        Renderable(
            lambda brush: brush.draw_image("boy_l_idle.png"),
            2
        ),
        TilePositionable("ground", (0, 7), 2),
        banimable,
        Clickable(
            lambda: banimable.add_animations(
                TileMoveAnimation((5,0), 5),
                SpriteAnimation(5, 2.5, anim_list)
            ),
            Button.LEFT
        )
    )

    create_building(world, scenario_state)

    sky = create_sky_effect(
        world,
        (0, 0),
        (700, 550),
        300
    )

    scheduler.at(3).call(sky.to_night)
