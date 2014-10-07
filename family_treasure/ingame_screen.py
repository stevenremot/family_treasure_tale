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
from tile import TileSpace, TilePositionable
from graphics import Renderable
from mouse import Clickable, Button
from game_screen import transition as gamescreen_transition
from gameover_screen import create_gameover_screen
from text import create_text_entity

def create_ingame_screen(world):
    """ Create entities for the ingame screen """

    tile_entity = world.entity()
    tile_entity.add_components(
        Positionable(15, 15, 0, 0),
        TileSpace("space", (15, 15))
    )

    test_entity = world.entity()
    test_entity.add_components(
        Positionable(0, 0, 30, 15),
        Renderable(
            lambda brush: brush.draw_rect((255, 255, 255), (0, 0), (30, 15)),
            1
        ),
        TilePositionable("space", (1, 1), 0),
        Clickable(
            lambda : gamescreen_transition(world, create_gameover_screen),
            Button.LEFT
        )
    )

    test_entity2 = world.entity()
    test_entity2.add_components(
        Positionable(20, 15, 15, 30),
        Renderable(
            lambda brush: brush.draw_rect((255, 0, 0), (0, 0), (15, 30)),
            0
        ),
        TilePositionable("space", (3, 2), 0)
    )

    create_text_entity(
        world,
        "Click the white rectangle to lose :-)",
        (0, 0, 255),
        30,
        50,
        50
    )
