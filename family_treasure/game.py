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

import pygame
import sys

from tile import TileSystem
from graphics import Screen, GraphicsSystem
from ecs import World
from mouse import MouseSystem, to_mouse_button
from title_screen import create_title_screen
from animation import AnimationSystem
from schedule import Scheduler
from assets import load_assets
from light import LightSystem


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
        scheduler = Scheduler()
        create_title_screen(world, scheduler)

        graphics_system = GraphicsSystem(world, screen)
        load_assets(graphics_system)

        tile_system = TileSystem(world, 5)

        mouse_system = MouseSystem(world)
        animation_system = AnimationSystem(world)

        light_system = LightSystem(world)

        clock.tick(self.fps)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_system.on_mouse_down(
                        event.pos,
                        to_mouse_button(event.button)
                    )
                elif event.type == pygame.MOUSEMOTION:
                    mouse_system.on_mouse_motion(event.pos)

            clock.tick(self.fps)
            time_elapsed = float(clock.get_time()) / 1000.0

            scheduler.update(time_elapsed)
            animation_system.update(time_elapsed)
            tile_system.update_tile_positions()
            light_system.update()
            graphics_system.draw_entities()

            pygame.display.set_caption(
                "The Family's Treasure Tale --- " + str(clock.get_fps()))
