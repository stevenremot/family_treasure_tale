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

import pygame, sys
from geometry import Positionable
from graphics import Screen, Renderable, GraphicsSystem
from tile import TileSpace, TilePositionable, TileSystem
from ecs import World

class Game:
    """Basic game launcher class
    Usage:
    >> game = Game(fps, (width, height))
    >> game.run()
    """

    def __init__(self, fps, window_size):
        self.fps = fps
        self.window_size = window_size

    def run(self):
        """Execute the game loop
        """
        pygame.init()
        screen = Screen(self.window_size)
        clock = pygame.time.Clock()

        world = World()
        tile_space = world.entity()
        tile_space.add_components(
            Positionable(10, 10, 0, 0),
            TileSpace("space", (15, 15))
        )
        test_entity = world.entity()
        test_entity.add_components(
            Positionable(0, 0, 30, 15),
            Renderable(
                lambda brush: brush.draw_rect((255, 255, 255), (0, 0), (30, 15)),
                1
            ),
            TilePositionable("space", (1, 1), 0)
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

        graphics_system = GraphicsSystem(world, screen)
        tile_system = TileSystem(world, 1)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #TODO: call ClickSystem
                    print("Someone clicked")

            tile_system.update_tile_positions()
            graphics_system.draw_entities()

            clock.tick(self.fps)
