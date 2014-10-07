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

from tile import TileSpace, TilePositionable, TileSystem
from geometry import Positionable, get_text_positionable
from graphics import Screen, Renderable, Colorable, GraphicsSystem
from ecs import World
from mouse import Button, Clickable, Hoverable, MouseSystem

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
        Colorable(color),
        Renderable(
            lambda brush, color: brush.draw_text(text, color, font_size, font_type),
            layer
        )
    )
    return entity

def create_hoverable_text_entity(world, text, color1, color2, font_size, x=0, y=0, layer=0, font_type=None):
    """ Create a text entity with color2 when hovered and color1 elsewhere
    Return the created entity
    """
    entity = create_text_entity(
        world, text, color1, font_size, x, y, layer, font_type)
    entity.add_component(
        Hoverable(
            lambda: entity.get_component(Colorable).set_color(color2),
            lambda: entity.get_component(Colorable).set_color(color1)
        )
    )
    return entity

def gamescreen_transition(world, create_gamescreen_func):
    """ Remove all the world's entities and setup a new gamescreen"""
    world.clear()
    create_gamescreen_func(world)

def create_ingame_screen(world):
    """ Create entities for the ingame screen """

    tile_entity = world.entity()
    tile_entity.add_components(
        Positionable(15, 15, 0, 0),
        TileSpace("space", (15, 15))
    )

    test_entity = world.entity()
    test_entity.add_components(
        Positionable(0, 0, 30, 15),
        Renderable(
            lambda brush: brush.draw_rect((255, 255, 255), (0, 0), (30, 15)),
            1
        ),
        TilePositionable("space", (1, 1), 0),
        Clickable(
            lambda : gamescreen_transition(world, create_gameover_screen),
            Button.LEFT
        )
    )

    test_entity2 = world.entity()
    test_entity2.add_components(
        Positionable(20, 15, 15, 30),
        Renderable(
            lambda brush: brush.draw_image("basic_ground_tile.png"),
            0
        ),
        TilePositionable("space", (3, 2), 0)
    )

    create_text_entity(
        world,
        "Click the white rectangle to lose :-)",
        (0, 0, 255),
        30,
        50,
        50
    )

def create_title_screen(world):
    create_text_entity(
        world,
        "The Family's Treasure Tale",
        (255, 255, 255),
        60,
        50,
        150
    )
    start = create_hoverable_text_entity(
        world,
        "Start",
        (160, 160, 160),
        (255, 255, 255),
        40,
        200,
        300
    )
    start.add_component(
        Clickable(
            lambda: gamescreen_transition(world, create_ingame_screen),
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
        400
    )
    exit.add_component(Clickable(lambda: sys.exit(), Button.LEFT))

def create_gameover_screen(world):
    gameover = create_text_entity(
        world,
        "Game Over",
        (255, 0, 0),
        100,
        250,
        250)
    gameover.add_component(
        Clickable(
            lambda: gamescreen_transition(world, create_title_screen),
            Button.LEFT)
    )


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
