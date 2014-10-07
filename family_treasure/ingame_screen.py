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

def create_ingame_screen(world):
    """ Create entities for the ingame screen """
    create_room(world)

    building = Building(
        [
            Room((0, 0), []),
            Room((0, 30), []),
            Room((30, 0), []),
            Room((30, 30), [])
        ],
        (30, 30)
    )

    create_minimap(world, (700, 50), building)
