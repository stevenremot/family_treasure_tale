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

from ecs import World
from tile import TilePositionable

class Frightenable:
    """Component for entities that can be frightened, for example
    by moving furniture
    """
    def __init__(self, fear_func):
        self.fear_func = fear_func
        self.look_up = False
        

class Frightening:
    """Component for entities that frighten frightenables entities
    """

    def __init__(self):
        self.moving = False

class FearSystem:
    """Check that frightenable entities don't look frightening entities
    """

    def __init__(self, world):
        self.world = world

    def update(self):
        for frightening_entity in self.world.get_entities([Frightening, TilePositionable]):
            frightening = frightening_entity.get_component(Frightening)
            if frightening.moving:
                for frightenable_entity in self.world.get_entities([Frightenable, TilePositionable]):
                    frightenable = frightenable_entity.get_component(Frightenable)
                    frightenable_pos = frightenable_entity.get_component(TilePositionable)
                    frightening_pos = frightening_entity.get_component(TilePositionable)
                    dist = (float(frightenable_pos.x) - float(frightening_pos.x)) ** 2 
                    + (float(frightenable_pos.y) - float(frightening_pos.y)) ** 2
                    if frightenable.look_up and dist < 2.0:
                        frightenable.fear_func()
                        

    
