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
from graphics import Renderable
from animation import TileMoveAnimation, SpriteAnimation, Animable
from tile import TilePositionable
from geometry import Positionable
from ecs import Activable


class CharacterDirection:
    LEFT = 'r'
    RIGHT = 'l'
    DOWN = 't'
    UP = 'b'


class Character(object):
    """Helper class for managing a character entity.
    """
    def __init__(self, entity, animation_name, base_direction, fps):
        self.entity = entity
        self._animation_name = animation_name
        self._direction = base_direction
        self.set_idle_image()
        self.fps = fps
        self.current_animation = None

    def set_idle_image(self):
        """Update the renderable to draw idle image.
        """
        idle_image = self.animation_list[0]
        renderable = self.entity.get_component(Renderable)
        renderable.render_func = lambda brush: brush.draw_image(idle_image)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
        if self.current_animation is not None:
            self.current_animation.stop()
        self.set_idle_image()

    @property
    def animation_name(self):
        return self._animation_name

    @animation_name.setter
    def animation_name(self, name):
        self._animation_name = name
        self.set_idle_image()

    def walk(self, direction, distance, duration):
        """Make the character walk the direction for a certain distance and
        duration.

        """
        self._direction = direction

        if direction == CharacterDirection.LEFT:
            vector = (-distance, 0)
        elif direction == CharacterDirection.RIGHT:
            vector = (distance, 0)
        elif direction == CharacterDirection.UP:
            vector = (0, -distance)
        else:
            vector = (0, distance)

        self.current_animation = SpriteAnimation(
            duration,
            self.fps,
            self.animation_list
        )

        self.entity.get_component(Animable).add_animations(
            TileMoveAnimation(vector, duration),
            self.current_animation
        )

    @property
    def animation_list(self):
        return [
            "%s_%s_idle.png" % (self.animation_name, self._direction),
            "%s_%s_move_1.png" % (self.animation_name, self._direction),
            "%s_%s_move_2.png" % (self.animation_name, self._direction)
        ]


def create_character(world, base_pos, animation_name, base_direction, fps):
    character = world.entity()
    character.add_components(
        Positionable(0, 0, 40, 80),
        Renderable(lambda brush: None, 2),
        TilePositionable("ground", base_pos, 2),
        Animable(),
        Activable()
    )
    return Character(
        character,
        animation_name,
        base_direction,
        fps
    )
