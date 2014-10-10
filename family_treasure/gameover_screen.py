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

from text import create_text_entity, center_horizontally
from mouse import Clickable, Button
from game_screen import transition as gamescreen_transition
from title_screen import create_title_screen
from data import filepath


def create_gameover_screen(world, scheduler):
    gameover = create_text_entity(
        world,
        "Game Over",
        (255, 0, 0),
        100,
        250,
        250,
        0,
        filepath("bilbo/Bilbo-Regular.otf")
    )
    gameover.add_component(
        Clickable(
            lambda: gamescreen_transition(world, scheduler, create_title_screen),
            Button.LEFT)
    )
    center_horizontally(gameover)
