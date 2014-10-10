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

import sys
from text import create_text_entity, create_hoverable_text_entity
from mouse import Clickable, Button
from game_screen import transition as gamescreen_transition
from data import filepath

def create_title_screen(world, scheduler):
    from ingame_screen import create_ingame_screen

    create_text_entity(
        world,
        "The Family's Treasure Tale",
        (255, 255, 255),
        70,
        50,
        150,
        0,
        filepath("bilbo/BilboSwashCaps-Regular.otf")
    )
    start = create_hoverable_text_entity(
        world,
        "Start",
        (160, 160, 160),
        (255, 255, 255),
        40,
        200,
        300,
        0,
        filepath("bilbo/Bilbo-Regular.otf")
    )
    start.add_component(
        Clickable(
            lambda: gamescreen_transition(world, scheduler, create_ingame_screen),
            Button.LEFT
        )
    )
    exit = create_hoverable_text_entity(
        world,
        "Exit",
        (160, 160, 160),
        (255, 255, 255),
        40,
        200,
        400,
        0,
        filepath("bilbo/Bilbo-Regular.otf")
    )
    exit.add_component(Clickable(lambda: sys.exit(), Button.LEFT))
