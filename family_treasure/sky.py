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

from geometry import Positionable
from graphics import Renderable, Colorable
from animation import Animable, ColorAnimation

day_color = (12, 32, 139, 0)
night_color = (12, 32, 139, 128)
duration = 3


class Sky:
    """Helper class for sky transitions.
    """
    def __init__(self, entity):
        self.entity = entity

    def to_night(self):
        animable = self.entity.get_component(Animable)
        animable.add_animation(ColorAnimation(night_color, duration))

    def to_day(self):
        animable = self.entity.get_component(Animable)
        animable.add_animation(ColorAnimation(day_color, duration))


def create_sky_effect(world, pos, size, layer):
    """Setup a sky entity and return its helper.
    """
    sky = world.entity()
    sky.add_components(
        Positionable(pos[0], pos[1], size[0], size[1]),
        Colorable(day_color),
        Renderable(
            lambda brush, color: brush.draw_rect(color, (0, 0), size),
            layer
        ),
        Animable()
    )

    return Sky(sky)
