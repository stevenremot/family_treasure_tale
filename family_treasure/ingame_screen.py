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
from sky import create_sky_effect

# -----
from geometry import Positionable
from tile import TilePositionable
from graphics import Renderable
from ecs import Activable
from character import CharacterDirection, create_character


def create_building(world, scenario_state):
    up_door = world.entity()
    up_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_t.png"),
            3
        ),
        TilePositionable("wall", (8, 1), 3),
        Activable(False)
    )

    left_door = world.entity()
    left_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_l.png"),
            3
        ),
        TilePositionable("wall", (0, 6), 3),
        Activable(False)
    )

    down_door = world.entity()
    down_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_b.png"),
            3
        ),
        TilePositionable("wall", (8, 10), 3),
        Activable(False)
    )

    right_door = world.entity()
    right_door.add_components(
        Positionable(0, 0, 100, 50),
        Renderable(
            lambda brush: brush.draw_image("door2_r.png"),
            3
        ),
        TilePositionable("wall", (12, 6), 3),
        Activable(False)
    )

    window = world.entity()
    window.add_components(
        Positionable(0, 0, 100, 100),
        Renderable(
            lambda brush: brush.draw_image("window_t.png"),
            1
        ),
        TilePositionable("wall", (7, 1), 1),
        Activable(False)
    )

    def is_activated(entity):
        return entity.get_component(Activable).activated

    scenario_state["has_window"] = lambda: is_activated(window)
    scenario_state["has_down_door"] = lambda: is_activated(down_door)
    scenario_state["has_up_door"] = lambda: is_activated(up_door)
    scenario_state["has_right_door"] = lambda: is_activated(right_door)

    scenario_state["window"] = window

    building = Building(
        [
            Room((0, 0), [left_door, right_door, down_door, window]),
            Room((0, 30), [up_door]),
            Room((30, 0), [left_door, down_door]),
            Room((30, 30), [up_door])
        ],
        (30, 30)
    )

    scenario_state["minimap"] = create_minimap(world, (700, 50), building)


def close_compartment(compartment):
    renderable = compartment.get_component(Renderable)
    renderable.render_func = lambda brush: brush.draw_image("compartment.png")


def create_compartment(world, scenario_state):
    compartment = world.entity()
    compartment.add_components(
        Positionable(0, 0, 50, 50),
        Renderable(
            lambda brush: brush.draw_image("compartment_open.png"),
            1
        ),
        TilePositionable("wall", (2, 0.3), 2)
    )

    scenario_state["compartment"] = compartment


def create_father(world, scenario_state):
    father = create_character(
        world,
        (0, 4.5),
        "boy_chest",
        CharacterDirection.RIGHT,
        2.5
    )

    scenario_state["father"] = father


def create_mother(world, scenario_state):
    mother = create_character(
        world,
        (1, 4),
        "girl",
        CharacterDirection.LEFT,
        2.5
    )

    scenario_state["mother"] = mother


def create_burglar(world, scenario_state):
    burglar = create_character(
        world,
        (1, 4),
        "burglar_lantern",
        CharacterDirection.LEFT,
        2.5
    )

    scenario_state["burglar"] = burglar


def setup_animation(scheduler, scenario_state):
    father = scenario_state["father"]
    mother = scenario_state["mother"]
    burglar = scenario_state["burglar"]

    compartment = scenario_state["compartment"]
    window = scenario_state["window"]

    minimap = scenario_state["minimap"]

    sky = scenario_state["sky"]

    def mother_look_up():
        mother.direction = CharacterDirection.UP

    def mother_look_right():
        mother.direction = CharacterDirection.RIGHT

    def father_release_chest():
        father.animation_name = "boy"

    def set_pos(entity, pos):
        def setter():
            entity.get_component(TilePositionable).pos = pos
        return setter

    def look(character, direction):
        def setter():
            character.direction = direction

        return setter

    burglar.entity.get_component(Activable).toggle()
    minimap.disable()

    # Introduction
    introduction_end = scheduler\
        .at(1)\
        .walk(father, CharacterDirection.UP, 3.5, 2)\
        .after(0.7)\
        .call(look(mother, CharacterDirection.UP))\
        .after(1.4)\
        .set_image(compartment, "compartment_open_chest.png")\
        .call(father_release_chest)\
        .after(0.1)\
        .set_image(compartment, "compartment.png")\
        .after(0.3)\
        .walk(father, CharacterDirection.DOWN, 2, 1)\
        .after(1)\
        .walk(father, CharacterDirection.RIGHT, 8, 4.5)\
        .after(1)\
        .call(look(mother, CharacterDirection.RIGHT))\
        .after(1)\
        .walk(mother, CharacterDirection.RIGHT, 6, 3.5)\
        .after(2.5)\
        .walk(father, CharacterDirection.DOWN, 2, 1)\
        .after(1)\
        .walk(father, CharacterDirection.RIGHT, 1.5, 1)\
        .walk(mother, CharacterDirection.DOWN, 1, 0.5)\
        .after(0.5)\
        .walk(mother, CharacterDirection.RIGHT, 2.5, 1.5)\
        .after(0.5)\
        .toggle(father.entity)\
        .after(1)\
        .toggle(mother.entity)\
        .call(minimap.enable)\
        .after(2)\
        .call(sky.to_night)\
        .after(5)

    # Burglar comes
    introduction_end\
        .call(minimap.disable)

    introduction_end\
        .after(0.6)\
        .when(scenario_state["has_up_door"])\
        .call(set_pos(burglar.entity, (6, 1)))\
        .call(look(burglar, CharacterDirection.DOWN))\
        .toggle(burglar.entity)\
        .after(0.5)\
        .walk(burglar, CharacterDirection.DOWN, 3, 1.5)

    introduction_end\
        .when(scenario_state["has_window"])\
        .call(set_pos(burglar.entity, (6, 1)))\
        .call(look(burglar, CharacterDirection.DOWN))\
        .set_image(window, "window_semiopen.png")\
        .after(0.3)\
        .set_image(window, "window_open.png")\
        .after(0.3)\
        .toggle(burglar.entity)\
        .after(0.5)\
        .walk(burglar, CharacterDirection.DOWN, 3, 1.5)

    introduction_end\
        .after(0.6)\
        .when(lambda: scenario_state["has_down_door"]() and not scenario_state["has_window"]())\
        .call(set_pos(burglar.entity, (6, 7)))\
        .call(look(burglar, CharacterDirection.UP))\
        .toggle(burglar.entity)\
        .after(0.5)\
        .walk(burglar, CharacterDirection.UP, 3, 1.5)

    # Burgler searches randomly
    introduction_end\
        .after(3)\
        .walk(burglar, CharacterDirection.RIGHT, 3, 1.5)\
        .after(1.5)\
        .walk(burglar, CharacterDirection.UP, 2, 1)\
        .after(1.5)\
        .walk(burglar, CharacterDirection.LEFT, 4, 2)\
        .after(2)\
        .walk(burglar, CharacterDirection.DOWN, 5, 2.5)\
        .after(2.5)\
        .walk(burglar, CharacterDirection.LEFT, 5, 2.5)\
        .after(2.5)\
        .walk(burglar, CharacterDirection.UP, 2, 1)\
        .after(1)\
        .call(look(burglar, CharacterDirection.RIGHT))\
        .after(0.5)\
        .walk(burglar, CharacterDirection.UP, 3, 1.5)\
        .after(1.5)\
        .walk(burglar, CharacterDirection.RIGHT, 3, 1.5)


def create_ingame_screen(world, scheduler):
    """ Create entities for the ingame screen """
    create_room(world)
    scenario_state = {}

    create_compartment(world, scenario_state)
    create_father(world, scenario_state)
    create_mother(world, scenario_state)
    create_burglar(world, scenario_state)

    create_building(world, scenario_state)

    sky = create_sky_effect(
        world,
        (0, 0),
        (700, 550),
        300
    )

    scenario_state["sky"] = sky

    setup_animation(scheduler, scenario_state)
