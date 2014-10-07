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

from tile import TileSystem
from graphics import Screen, GraphicsSystem
from ecs import World
from mouse import MouseSystem, to_mouse_button
from title_screen import create_title_screen

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
        create_title_screen(world)

        graphics_system = GraphicsSystem(world, screen)
        tile_system = TileSystem(world, 1)
        mouse_system = MouseSystem(world)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_system.on_mouse_down(
                        event.pos,
                        to_mouse_button(event.button)
                    )
                elif event.type == pygame.MOUSEMOTION:
                    mouse_system.on_mouse_motion(event.pos)

            tile_system.update_tile_positions()
            graphics_system.draw_entities()

            clock.tick(self.fps)
