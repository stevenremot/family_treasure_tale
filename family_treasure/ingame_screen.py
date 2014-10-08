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
from graphics import Renderable, Colorable
from ecs import Activable
from mouse import Clickable, Button
from animation import TileMoveAnimation, SpriteAnimation, Animable, ColorAnimation


def create_ingame_screen(world, scheduler):
    """ Create entities for the ingame screen """
    create_room(world)

    banimable = Animable()

    boy = world.entity()
    boy.add_components(
        Positionable(0, 0, 40, 80),
        Renderable(
            lambda brush: brush.draw_image("boy.png"),
            2
        ),
        TilePositionable("ground", (3, 2), 4),
        banimable,
        Clickable(
            lambda: banimable.add_animations(
                TileMoveAnimation((0,5), 5),
                SpriteAnimation(5, 3, ["move_1.png", "move_2.png"])
            ),
            Button.LEFT
        )
    )

    animable = Animable()

    clicked = [False]

    def on_red_click():
        animable.add_animation(TileMoveAnimation((5, 0), 5))
        clicked[0] = True

    rect = world.entity()
    rect.add_components(
        Positionable(0, 0, 50, 50),
        Renderable(lambda brush: brush.draw_rect((255, 0, 0), (0, 0), (50, 50)), 1),
        TilePositionable("ground", (3, 3), 1),
        Activable(False),
        animable,
        Clickable(
            on_red_click,
            Button.LEFT
        )
    )

    char_rect = world.entity()
    char_rect.add_components(
        Positionable(0, 0, 40, 80),
        Colorable((0, 0, 255, 128)),
        Renderable(lambda brush, color: brush.draw_rect(
            color, (0, 0), (40, 80)
        ), 1),
        TilePositionable("ground", (5, 3), 1),
        Activable(False),
        Animable()
    )

    scheduler.at(0.5).animate(char_rect, TileMoveAnimation((2.5, 3), 2))
    scheduler.at(2.5).animate(char_rect, TileMoveAnimation((0, -2), 0.5))
    scheduler.at(2.5).when(lambda: clicked[0]).animate(
        char_rect,
        ColorAnimation((0, 255, 0), 1)
    )

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
