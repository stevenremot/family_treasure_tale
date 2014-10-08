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

def create_room(
        world,
        outer_positionable = Positionable(0, 0, 600, 500),
        inner_positionable = Positionable(100, 100, 500, 400),
        outer_resolution = (50, 50),
        inner_resolution = (50, 50),
        ground_sprite = "basic_ground_tile.png",
        wall_sprite = "wall_tile",
        corner_sprite = "corner_tile"
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

    for i in range(inner_positionable.width / w):
        for j in range(inner_positionable.height / h):
            e = world.entity()
            e.add_components(
                Positionable(0, 0, w, h),
                Renderable(
                    lambda brush: brush.draw_image(ground_sprite),
                    0
                ),
                TilePositionable("ground", (i,j), 0)
                )
            
    #wall
    tile_wall = world.entity()
    tile_wall.add_components(
        outer_positionable,
        TileSpace("wall", outer_resolution)
    )
    w, h = outer_resolution
    w_max = outer_positionable.width / w
    h_max = outer_positionable.height / h
    #corners
    tl = world.entity()
    tl.add_components(
        Positionable(0, 0, 2*w, 2*h),
        Renderable(
            lambda brush: brush.draw_image(corner_sprite+"_tl.png"),
            0
        ),
        TilePositionable("wall", (0,0), 0)
    )
    tr = world.entity()
    tr.add_components(
        Positionable(0, 0, 2*w, 2*h),
        Renderable(
            lambda brush: brush.draw_image(corner_sprite+"_tr.png"),
            0
        ),
        TilePositionable("wall", (w_max,0), 0)
    )
    bl = world.entity()
    bl.add_components(
        Positionable(0, 0, 2*w, 2*h),
        Renderable(
            lambda brush: brush.draw_image(corner_sprite+"_bl.png"),
            0
        ),
        TilePositionable("wall", (0,h_max), 0)
    )
    br = world.entity()
    br.add_components(
        Positionable(0, 0, 2*w, 2*h),
        Renderable(
            lambda brush: brush.draw_image(corner_sprite+"_br.png"),
            0
        ),
        TilePositionable("wall", (w_max,h_max), 0)
    )

    #walls
    for i in range(2, w_max):
        t = world.entity()
        t.add_components(
            Positionable(0, 0, w, 2*h),
            Renderable(
                lambda brush: brush.draw_image(wall_sprite+"_t.png"),
                0
            ),
            TilePositionable("wall", (i,0), 0)
        )
        b = world.entity()
        b.add_components(
            Positionable(0, 0, w, 2*h),
            Renderable(
                lambda brush: brush.draw_image(wall_sprite+"_b.png"),
                0
            ),
            TilePositionable("wall", (i,h_max), 0)
        )
         
    for j in range(2, h_max):
        l = world.entity()
        l.add_components(
            Positionable(0, 0, 2*w, h),
            Renderable(
                lambda brush: brush.draw_image(wall_sprite+"_l.png"),
                0
            ),
            TilePositionable("wall", (0,j), 0)
        )
        r = world.entity()
        r.add_components(
            Positionable(0, 0, 2*w, h),
            Renderable(
                lambda brush: brush.draw_image(wall_sprite+"_r.png"),
                0
            ),
            TilePositionable("wall", (w_max,j), 0)
        )

        #furniture
        table = world.entity()
        table.add_components(
            Positionable(0, 0, 150, 100),
            Renderable(
                lambda brush: brush.draw_image("table_textured.png"),
                1
            ),
            TilePositionable("ground", (1, 4), 1)
        )

        stool = world.entity()
        stool.add_components(
            Positionable(0, 0, 40, 40),
            Renderable(
                lambda brush: brush.draw_image("stool.png"),
                1
            ),
            TilePositionable("ground", (2,6), 1)
        )

        bookshelf = world.entity()
        bookshelf.add_components(
            Positionable(0, 0, 50, 100),
            Renderable(
                lambda brush: brush.draw_image("bookshelf.png"),
                1
            ),
            TilePositionable("ground", (3,-1.5), 1)
        )
