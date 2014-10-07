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
from geometry import Positionable, get_text_positionable
from graphics import Screen, Renderable, GraphicsSystem
from ecs import World
from mouse import Button, Clickable, MouseSystem

def to_mouse_button(b):
    if b == 1:
        return Button.LEFT
    elif b == 3:
        return Button.RIGHT

def create_text_entity(world, text, color, font_size, x=0, y=0, layer=0, font_type=None):
    """ Create a text entity and returns it """
    entity = world.entity()
    entity.add_components(
        get_text_positionable(text, font_size, x, y, font_type),
        Renderable(
            lambda brush: brush.draw_text(text, color, font_size, font_type),
            layer
        )
    )
    return entity

def create_ingame_screen(world):
    """ Create entities for the ingame screen """
    test_entity = world.entity()
    test_entity.add_components(
        Positionable(10, 10, 30, 15),
        Renderable(
            lambda brush: brush.draw_rect((255, 255, 255), (0, 0), (30, 15)),
            1
        ),
        Clickable(lambda : sys.stdout.write("clicked \n"), Button.LEFT)
        )

    test_entity2 = world.entity()
    test_entity2.add_components(
        Positionable(20, 15, 30, 15),
        Renderable(
            lambda brush: brush.draw_rect((255, 0, 0), (0, 0), (30, 15)),
            0
        )
    )

    test_entity3 = create_text_entity(world, "Yo !", (0, 0, 255), 30, 50, 50)

def create_title_screen(world):
    title = create_text_entity(
        world,
        "The Family's Treasure Tale",
        (255, 255, 255),
        50,
        50,
        150)

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
        create_ingame_screen(world)

        graphics_system = GraphicsSystem(world, screen)
        mouse_system = MouseSystem(world)
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_system.on_mouse_down(event.pos,
                                                   to_mouse_button(event.button))

            graphics_system.draw_entities()

            clock.tick(self.fps)
