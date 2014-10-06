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
# along with The Family's treasure tale. If not, see
# <http://www.gnu.org/licenses/>.

from geometry import Positionable

class Button:
    LEFT, RIGHT = range(2)

class Clickable(object):
    """ Component for entities that react when they are clicked """

    def __init__(self, callback, button):
        self.callback = callback
        self.button = button

class Hoverable(object):
    """ Component for entities that react when they are hovered """

    def __init__(self, callback_hovered, callback_unhovered):
        self.callback_hovered = callback_hovered
        self.callback_unhovered = callback_unhovered
        self.is_hovered = False
    

class MouseSystem(object):
    """ System called when mouse events are catched. It manages entities
interactions with the mouse """

    def __init__(self, world):
        self.world = world

    def on_mouse_down(self, pos, button):
        """ Called when the mouse button was clicked on the (x,y) position.
        Search for a clickable entity and thus, call its callback """
        for entity in self.world.get_entities([Positionable, Clickable]):
            positionable = entity.get_component(Positionable)
            clickable = entity.get_component(Clickable)

            if positionable.contains(pos) and clickable.button == button:
                clickable.callback()

    def on_mouse_moved(self, pos):
        """ Called when the mouse was moved into the (x,y) position.
        Search for a hoverable entity and thus, call the adequate callback """
        for entity in self.world.get_entities([Positionable, Hoverable]):
            positionable = entity.get_component(Positionable)
            hoverable = entity.get_component(Hoverable)
            
            if positionable.contains(pos) and not hoverable.is_hovered:
                hoverable.is_hovered = True
                hoverable.callback_hovered()
                
            if not positionable.contains(pos) and hoverable.is_hovered:
                hoverable.is_hovered = False
                hoverable.callback_unhovered()
