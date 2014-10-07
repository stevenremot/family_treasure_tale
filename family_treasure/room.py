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
from ecs import World

def create_room(
        world,
        outer_positionable = Positionable(50, 50, 600, 500),
        inner_positionable = Positionable(100, 100, 500, 400),
        outer_resolution = (50, 50),
        inner_resolution = (50, 50),
        ground_sprite = "basic_ground_tile.png"
):
    """ Create the entities of the room
    outer_positionable: describes the area of the room, walls included
    inner_positionable: describes the area of the ground
    outer_resolution: tile resolution of the walls
    inner_resolution: tile resolution of the ground
    """

    #ground
    tile_ground = world.entity()
    tile_ground.add_components(
        inner_positionable,
        TileSpace("ground", inner_resolution)
    )

    w, h = inner_resolution

    for i in range(inner_positionable.width / inner_resolution[0]):
        for j in range(inner_positionable.height / inner_resolution[1]):
            e = world.entity()
            e.add_components(
                Positionable(0, 0, w, h),
                Renderable(
                    lambda brush: brush.draw_image(ground_sprite),
                    0
                ),
                TilePositionable("ground", (i,j), 0)
                )
    
    print "Todo!"
