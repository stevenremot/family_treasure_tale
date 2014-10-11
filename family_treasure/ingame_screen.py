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

########################################
#  __________________________________  #
# / Welcome to the land of ugliness, \ #
# \ mooooooo~                        / #
#  ----------------------------------  #
#         \   ^__^                     #
#          \  (oo)\_______             #
#             (__)\       )\/\         #
#                 ||----w |            #
#                 ||     ||            #
#                                      #
########################################

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
from game_screen import transition
from gameover_screen import create_gameover_screen
from light import Lightable
from happyend_screen import create_happyend_screen
from animation import TileMoveAnimation, Animable, FlickerAnimation
from mouse import Clickable, Button, add_cursor_change_hoverable
from fear import Frightenable, Frightening
from sound import SoundSystem


def create_building(world, scenario_state, sound_system):
    up_door = world.entity()
    up_door.add_components(
        Positionable(0, 0, 50, 100),
        Renderable(
            lambda brush: brush.draw_image("door2_t.png"),
            3
        ),
        TilePositionable("wall", (8, 1), 1),
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

    up_window = world.entity()
    up_window.add_components(
        Positionable(0, 0, 100, 100),
        Renderable(
            lambda brush: brush.draw_image("window_t.png"),
            1
        ),
        TilePositionable("wall", (7, 1), 1),
        Activable(False)
    )

    left_window = world.entity()
    left_window.add_components(
        Positionable(0, 0, 100, 100),
        Renderable(
            lambda brush: brush.draw_image("window_l.png"),
            1
        ),
        TilePositionable("wall", (0, 3), 1),
        Activable(False)
    )

    down_window_renderable = Renderable(
        lambda brush: brush.draw_image("window_b.png"),
        1
    )

    down_window_toggled = [False]

    def toggle_down_window():
        down_window_renderable.render_image(
            "window_b.png" if down_window_toggled[0] else "window_semiopen_b.png",
            (0, 0) if down_window_toggled[0] else (-24, 0)
        )
        down_window_toggled[0] = not down_window_toggled[0]
        sound_system.play("window")

    down_window = world.entity()
    down_window.add_components(
        Positionable(0, 0, 100, 100),
        down_window_renderable,
        TilePositionable("wall", (4, 10), 1),
        Clickable(
            toggle_down_window,
            Button.LEFT
        ),
        Activable(False)
    )
    add_cursor_change_hoverable(down_window)

    def is_activated(entity):
        return entity.get_component(Activable).activated

    scenario_state["has_window"] = lambda: is_activated(up_window)
    scenario_state["has_down_door"] = lambda: is_activated(down_door)
    scenario_state["has_up_door"] = lambda: is_activated(up_door)
    scenario_state["has_right_door"] = lambda: is_activated(right_door)

    scenario_state["window"] = up_window

    building = Building(
        [
            Room((0, 0), [left_door, right_door, down_door, left_window]),
            Room((0, 30), [up_door, left_window]),
            Room((30, 0), [left_door, down_door, up_window]),
            Room((30, 30), [up_door, down_window])
        ],
        (30, 30)
    )

    scenario_state["minimap"] = create_minimap(world, (700, 50), building)

    for i in range(2, 5):
        bookshelf = world.entity()
        bookshelf.add_components(
            Positionable(0, 0, 50, 100),
            Renderable(
                lambda brush: brush.draw_image("bookshelf.png"),
                1
            ),
            TilePositionable("ground", (i, 1), 1)
        )

        if i == 2:
            def bookshelf_move(animable, scenario_state, direction, duration):
                def move():
                    animable.add_animation(
                        TileMoveAnimation(direction, duration)
                    )
                    scenario_state["bookshelf_moved"] =\
                        not scenario_state["bookshelf_moved"]
                    sound_system.play("furniture")

                return move
            
            animable = Animable()
            scenario_state["bookshelf_moved"] = False
            scenario_state["bookshelf_move_left"] =\
                bookshelf_move(animable, scenario_state, (-2, 0), 1)
            scenario_state["bookshelf_move_right"] =\
                bookshelf_move(animable, scenario_state, (2, 0), 1)
            scenario_state["bookshelf_can_move"] = True

            def toggle_bookshelf(bookshelf):
                def toggle():
                    if scenario_state["bookshelf_can_move"]:
                        if scenario_state["bookshelf_moved"]:
                            scenario_state["bookshelf_move_right"]()
                        else:
                            scenario_state["bookshelf_move_left"]()

                return toggle

            bookshelf.add_components(
                animable,
                Clickable(
                    toggle_bookshelf(bookshelf),
                    Button.LEFT
                ),
                Frightening()
            )
            
            add_cursor_change_hoverable(bookshelf)

    fireplace_anim = Animable()
    fireplace_anim.add_animation(
        FlickerAnimation(6, 0.3)
    )

    fireplace = world.entity()
    fireplace.add_components(
        Positionable(0, 0, 100, 100),
        Renderable(
            lambda brush: brush.draw_image("fireplace.png"),
            1
        ),
        TilePositionable("ground", (8, 1), 1),
        Lightable(
            Positionable(-130, 60, 360, 120),
            Positionable(-230, 30, 560, 200),
            (205, 155, 29, 64)
        ),
        fireplace_anim
    )

    scenario_state["fireplace"] = fireplace


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
    def ghosts():
        scenario_state["ghosts"] = True

    mother.entity.add_component(
        Frightenable(ghosts)
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

    burglar.entity.get_component(Animable).add_animation(
        FlickerAnimation(6, 0.75)
    )

    burglar.entity.add_component(
        Lightable(
            Positionable(-20, 10, 60, 60),
            Positionable(-70, -40, 160, 160),
            (205, 155, 29, 64)
        )
    )

    scenario_state["burglar"] = burglar

def create_bubble(world, scenario_state):
    bubble = world.entity()
    bubble.add_components(
        Positionable(0, 0, 70, 70),
        Renderable(lambda brush: None, 20),
        TilePositionable("ground", (0, 0), 20),
        Activable(),
        Animable()
    )
    bubble.get_component(Activable).toggle()

    scenario_state["bubble"] = bubble


def setup_animation(world, scheduler, end_game, scenario_state, sound_system):
    father = scenario_state["father"]
    mother = scenario_state["mother"]
    burglar = scenario_state["burglar"]

    bubble = scenario_state["bubble"]

    compartment = scenario_state["compartment"]
    window = scenario_state["window"]
    fireplace = scenario_state["fireplace"]

    minimap = scenario_state["minimap"]

    sky = scenario_state["sky"]

    scenario_state["ghosts"] = False
    scenario_state["fireplace_unlit"] = False

    def father_release_chest():
        father.animation_name = "boy"

    def set_pos(entity, pos):
        def setter():
            entity.get_component(TilePositionable).pos = pos
        return setter

    def look(character, direction):
        def setter():
            character.direction = direction
            if character.entity.has_component(Frightenable):
                frightenable = character.entity.get_component(Frightenable)
                if direction is CharacterDirection.UP:
                    frightenable.look_up = True
                else:
                    frightenable.look_up = False

        return setter

    def bookshelf_disable():
        scenario_state["bookshelf_can_move"] = False

    def bookshelf_enable():
        scenario_state["bookshelf_can_move"] = True

    def fireplace_unlit():
        scenario_state["fireplace_unlit"] = True

    def pop():
        sound_system.play("bubble")

    burglar.entity.get_component(Activable).toggle()
    minimap.disable()
    bookshelf_disable()

    # Introduction
    introduction_begin = scheduler\
        .at(1)\
        .bubble(father, bubble, "bubble_chest.png", 1)\
        .call(pop)\
        .after(2)\
        .bubble(mother, bubble, "bubble_smile.png", 1)\
        .call(pop)\
        .after(2)\
        .bubble(father, bubble, "bubble_idea.png", 1)\
        .call(pop)\
        .after(1.5)\
        .walk(father, CharacterDirection.UP, 3.5, 2)\
        .after(0.7)\
        .call(look(mother, CharacterDirection.UP))\
        .after(1.4)\
        .set_image(compartment, "compartment_open_chest.png")\
        .call(father_release_chest)\
        .after(0.3)\
        .call(lambda: sound_system.play("window"))\
        .set_image(compartment, "compartment.png")\
        .after(0.3)\
        .walk(father, CharacterDirection.DOWN, 2, 1)\
        .call(bookshelf_enable)\
        .after(1)\
        .walk(father, CharacterDirection.RIGHT, 8, 4.5)\
        .after(1)\
        .call(look(mother, CharacterDirection.RIGHT))\
        .after(1)

    #first bad end
    first_bad_end = introduction_begin\
        .when(lambda: scenario_state["ghosts"])\
        .bubble(mother, bubble, "bubble_ghost.png", 1)\
        .call(pop)\
        .after(1)\
        .call(look(mother, CharacterDirection.DOWN))\
        .after(0.3)\
        .call(look(mother, CharacterDirection.UP))\
        .after(0.3)\
        .call(look(mother, CharacterDirection.LEFT))\
        .after(0.3)\
        .call(look(mother, CharacterDirection.RIGHT))\
        .after(1)\
        .bubble(father, bubble, "bubble_ghost.png", 1)\
        .call(pop)\
        .after(1)\
        .call(look(father, CharacterDirection.DOWN))\
        .after(0.3)\
        .call(look(father, CharacterDirection.RIGHT))\
        .after(0.3)\
        .call(look(father, CharacterDirection.LEFT))\
        .after(0.3)\
        .call(look(father, CharacterDirection.UP))\
        .after(1)\
        .walk(mother, CharacterDirection.RIGHT, 6, 1)\
        .after(0.5)\
        .walk(father, CharacterDirection.UP, 1.5, 0.3)\
        .after(0.5)\
        .walk(father, CharacterDirection.LEFT, 2, 0.4)\
        .after(0.5)\
        .walk(mother, CharacterDirection.UP, 3, 0.5)\
        .after(0.2)\
        .walk(father, CharacterDirection.DOWN, 3.5, 0.8)\
        .after(0.5)\
        .walk(mother, CharacterDirection.LEFT, 2, 0.4)\
        .after(0.3)\
        .walk(father, CharacterDirection.RIGHT, 3, 0.7)\
        .after(0.7)\
        .toggle(father.entity)\
        .walk(mother, CharacterDirection.RIGHT, 2, 0.3)\
        .after(0.3)\
        .walk(mother, CharacterDirection.DOWN, 6, 1)\
        .after(1)\
        .walk(mother, CharacterDirection.RIGHT, 2.5, 0.5)\
        .after(0.5)\
        .walk(mother, CharacterDirection.UP, 1.6, 0.3)\
        .after(0.3)\
        .call(look(mother, CharacterDirection.RIGHT))\
        .after(0.3)\
        .toggle(mother.entity)\
        .after(2)\
        .call(lambda: transition(
            world,
            scheduler,
            end_game,
            create_gameover_screen
        ))

    introduction_end = introduction_begin\
        .when(lambda: not scenario_state["ghosts"])\
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
        .after(1)\
        .toggle_light(fireplace)\
        .after(5)

    # Burglar comes
    introduction_end\
        .call(minimap.disable)\
        .call(bookshelf_disable)

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
        .set_image(window, "window_semiopen.png")\
        .call(lambda: sound_system.play("window"))\
        .after(0.1)\
        .call(lambda: sound_system.play("wind"))\
        .after(0.4)\
        .set_image(window, "window_open.png")\
        .after(0.5)\
        .call(set_pos(burglar.entity, (6, 1)))\
        .call(look(burglar, CharacterDirection.DOWN))\
        .toggle(burglar.entity)\
        .after(0.5)\
        .walk(burglar, CharacterDirection.DOWN, 3, 1.5)\
        .after(0.5)\
        .toggle_light(fireplace, False)\
        .set_image(fireplace, "fireplace_down.png")\
        .call(fireplace_unlit)\
        .after(1)\
        .bubble(burglar, bubble, "bubble_blind.png", 1)\
        .call(pop)

    introduction_end\
        .after(0.8)\
        .when(lambda: scenario_state["has_down_door"]() and not scenario_state["has_window"]())\
        .call(set_pos(burglar.entity, (6, 7)))\
        .call(look(burglar, CharacterDirection.UP))\
        .toggle(burglar.entity)\
        .after(0.5)\
        .walk(burglar, CharacterDirection.UP, 3, 1.5)

    # Burgler searches randomly
    burglar_find_step = introduction_end\
        .after(1)\
        .toggle_light(burglar.entity)\
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
        .walk(burglar, CharacterDirection.RIGHT, 3, 1.5)\
        .after(2)

    burglar_steal_step = burglar_find_step\
        .when(lambda: not scenario_state["bookshelf_moved"] or not scenario_state["fireplace_unlit"])\
        .bubble(burglar, bubble, "bubble_question.png", 1)\
        .call(pop)\
        .after(1)\
        .walk(burglar, CharacterDirection.LEFT, 3, 0.7)\
        .after(0.7)\
        .call(look(burglar, CharacterDirection.UP))\
        .after(0.1)\
        .bubble(burglar, bubble, "bubble_exclamation.png", 1)\
        .call(pop)\
        .after(1.2)

    burglar_steal_step\
        .when(lambda: not scenario_state["bookshelf_moved"])\
        .call(lambda: sound_system.play("window"))\
        .set_image(compartment, "compartment_open_chest.png")\
        .after(0.5)\
        .bubble(burglar, bubble, "bubble_smile_money.png", 1)\
        .call(pop)\
        .after(1)\
        .call(lambda: transition(
            world,
            scheduler,
            end_game,
            create_gameover_screen
        ))

    burglar_steal_step\
        .when(lambda: scenario_state["bookshelf_moved"] and not scenario_state["fireplace_unlit"])\
        .bubble(burglar, bubble, "bubble_question.png", 1)\
        .call(pop)\
        .after(1)\
        .call(scenario_state["bookshelf_move_right"])\
        .after(1.5)\
        .call(look(burglar, CharacterDirection.UP))\
        .after(0.1)\
        .bubble(burglar, bubble, "bubble_exclamation.png", 1)\
        .call(pop)\
        .after(1)\
        .call(lambda: sound_system.play("window"))\
        .set_image(compartment, "compartment_open_chest.png")\
        .after(0.5)\
        .bubble(burglar, bubble, "bubble_smile_money.png", 1)\
        .call(pop)\
        .after(1)\
        .call(lambda: transition(
            world,
            scheduler,
            end_game,
            create_gameover_screen
        ))

    burglar_find_step\
        .when(lambda: scenario_state["bookshelf_moved"] and scenario_state["fireplace_unlit"])\
        .walk(burglar, CharacterDirection.RIGHT, 3, 1.5)\
        .after(1.5)\
        .call(look(burglar, CharacterDirection.UP))\
        .after(0.1)\
        .bubble(burglar, bubble, "bubble_cry.png", 1)\
        .call(pop)\
        .after(1)\
        .walk(burglar, CharacterDirection.UP, 1, 0.5)\
        .after(0.5)\
        .toggle(burglar.entity)\
        .after(0.5)\
        .call(lambda: transition(
            world,
            scheduler,
            end_game,
            create_happyend_screen
        ))


def create_ingame_screen(world, scheduler, end_game):
    """ Create entities for the ingame screen """
    sound_system = SoundSystem(
        {
            "furniture": "sound/furniture.ogg",
            "bubble": "sound/pop.ogg",
            "wind": "sound/wind.ogg",
            "window": "sound/window.ogg"
        }
    )

    create_room(world, sound_system)
    scenario_state = {}

    create_compartment(world, scenario_state)
    create_father(world, scenario_state)
    create_mother(world, scenario_state)
    create_burglar(world, scenario_state)
    create_bubble(world, scenario_state)

    create_building(world, scenario_state, sound_system)

    sky = create_sky_effect(
        world,
        (0, 0),
        (700, 550),
        300
    )

    scenario_state["sky"] = sky

    setup_animation(world, scheduler, end_game, scenario_state, sound_system)
