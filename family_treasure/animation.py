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

from random import random

from tile import TilePositionable
from graphics import Renderable, Colorable
from ecs import Activable
from light import Lightable

class VanishAnimation:
    """An animation that desactivate an entity after a given duration
    """
    def __init__(self, duration):
        self.remaining_duration = float(duration)

    def update(self, entity, elapsed_time):
        self.remaining_duration -= elapsed_time

        if self.remaining_duration < 1e-6:
            entity.get_component(Activable).toggle()
        
        return self.remaining_duration > 1e-6

class TileMoveAnimation:
    """An animation that applies a certain tile translation to an entity in a
    given duration.
    """

    def __init__(self, movement, duration):
        self.movement_per_second = (
            float(movement[0]) / float(duration),
            float(movement[1]) / float(duration)
        )
        self.remaining_duration = float(duration)

    def update(self, entity, elapsed_time):
        min_time = min(elapsed_time, self.remaining_duration)
        positionable = entity.get_component(TilePositionable)
        positionable.x += self.movement_per_second[0] * min_time
        positionable.y += self.movement_per_second[1] * min_time

        self.remaining_duration -= elapsed_time
        return self.remaining_duration > 1e-6


class SpriteAnimation:
    """An animation that switches between different sprites
    sprite_list[0] is the idle sprite
    sprite_list[1,..] are the move sprites
    """

    def __init__(self, duration, fps, sprite_list):
        self.remaining_duration = float(duration)
        self.change_sprite_delay = 1 / float(fps)
        self.sprite_list = sprite_list
        self.current_sprite = 0
        self.current_step = 0
        self.has_started = False

    def update(self, entity, elapsed_time):
        update_renderable = False

        if not self.has_started:
            self.current_sprite = 1
            update_renderable = True
            self.has_started = True

        self.current_step += elapsed_time
        if self.current_step > self.change_sprite_delay:
            self.current_sprite += 1
            if self.current_sprite == len(self.sprite_list):
                self.current_sprite = 1
            self.current_step = 0
            update_renderable = True

        self.remaining_duration -= elapsed_time
        if self.remaining_duration < 1e-6:
            self.current_sprite = 0
            update_renderable = True

        if update_renderable:
            renderable = entity.get_component(Renderable)
            renderable.render_func = lambda brush: brush.draw_image(
                self.sprite_list[self.current_sprite])

        return self.remaining_duration > 1e-6


class ColorAnimation:
    """An animation that makes a transition to a certain color in a given
    duration.

    The entity must have a Colorable component.
    """
    def __init__(self, target_color, duration):
        self.target_color = target_color
        if len(self.target_color) < 4:
            self.target_color = (
                self.target_color[0],
                self.target_color[1],
                self.target_color[2],
                255
            )

        self.remaining_duration = duration
        self.color_vector = None
        self.current_color = None

    def update(self, entity, elapsed_time):
        min_time = min(elapsed_time, self.remaining_duration)

        colorable = entity.get_component(Colorable)

        if self.color_vector is None:
            rem = self.remaining_duration
            self.current_color = (
                float(colorable.color[0]),
                float(colorable.color[1]),
                float(colorable.color[2]),
                float(colorable.color[3]) if len(colorable.color) == 4 else 255
            )

            self.color_vector = (
                float(self.target_color[0] - colorable.color[0]) / rem,
                float(self.target_color[1] - colorable.color[1]) / rem,
                float(self.target_color[2] - colorable.color[2]) / rem,
                float(self.target_color[3] - colorable.color[3]) / rem if len(colorable.color) == 4 else 0
            )

        self.current_color = (
            self.current_color[0] + self.color_vector[0] * min_time,
            self.current_color[1] + self.color_vector[1] * min_time,
            self.current_color[2] + self.color_vector[2] * min_time,
            self.current_color[3] + self.color_vector[3] * min_time
        )

        colorable.color = (
            float(self.current_color[0]),
            float(self.current_color[1]),
            float(self.current_color[2]),
            float(self.current_color[3])
        )

        self.remaining_duration -= elapsed_time
        return self.remaining_duration > 1e-6


class FlickerAnimation:
    """An animation to make a light component flicker.
    """

    def __init__(self, fps):
        self.elapsed_time = 0.0
        self.step = 1.0 / float(fps)

    def update(self, entity, elapsed_time):
        self.elapsed_time += elapsed_time

        if self.elapsed_time >= self.step:
            lightable = entity.get_component(Lightable)
            lightable.flicker = random() * 0.25
            self.elapsed_time %= self.step

        return True


class Animable:
    """Component for entities that can carry animations.
    """

    def __init__(self):
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

    def add_animations(self, *animations):
        for a in animations:
            self.animations.append(a)

    def remove_animation(self, animation):
        self.animations.remove(animation)


class AnimationSystem:
    """System in charge of running animations.
    """
    def __init__(self, world):
        self.world = world

    def update(self, time_elapsed):
        """Update entities' animations.

        time_elapsed is the time to run the animation step, in seconds.
        """
        for entity in self.world.get_entities([Animable]):
            animable = entity.get_component(Animable)
            animations = animable.animations[:]

            for animation in animations:
                if not animation.update(entity, time_elapsed):
                    animable.remove_animation(animation)
