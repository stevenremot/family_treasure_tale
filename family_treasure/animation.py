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

from tile import TilePositionable

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

class Animable:
    """Component for entities that can carry animations.
    """

    def __init__(self):
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

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
