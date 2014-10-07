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

class Minimap:
    """Object in charge of drawing a minimap on the screen.
    """
    def __init__(self, building):
        self.building = building

    def draw(self, brush):
        """Render the minimap on the screen using a brush.
        """
        for room in self.building.rooms:
            brush.draw_rect(
                (255, 255, 255),
                room.position,
                self.building.room_size,
                True
            )

def create_minimap(world, pos, building):
    """Create a new minimap entity based on the building and return it.
    """
    minimap = Minimap(building)
    minimap_entity = world.entity()
    minimap_entity.add_components(
        Positionable(pos[0], pos[1], 0, 0),
        Renderable(minimap.draw, 200)
    )
    return minimap_entity
