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

import pygame
from geometry import Positionable
from graphics import Renderable, Colorable


class Lightable:
    """Component for entities that emit light"""

    def __init__(self, inner_light_ellipse, outer_light_ellipse, color):
        """light_ellipse: positionable component that is the bounding
        rectangle of an ellipse color: rgba light color
        """
        self.inner_light_ellipse = inner_light_ellipse
        self.outer_light_ellipse = outer_light_ellipse
        self.color = color
        self.toggled = False
        self.flicker = 0.0

    def toggle(self, bool=True):
        self.toggled = bool


class LightSystem:
    """System that creates the light from the sky and
    lightable entities"""

    def __init__(self, world):
        self.world = world

    def update(self):
        from sky import Sky

        for sky_entity in self.world.get_entities([Sky]):
            sky_pos = sky_entity.get_component(Positionable)
            sky_color = sky_entity.get_component(Colorable).color
            light_surface = pygame.Surface(
                (sky_pos.width, sky_pos.height),
                pygame.SRCALPHA
            )
            light_surface.fill(sky_color)
            #light_surface.set_clip(100, 100, 500, 400)

            light_entities = self.world.get_entities([Positionable, Lightable])
            # First pass, outer lights
            for entity in light_entities:
                light = entity.get_component(Lightable)

                if light.toggled:
                    pos = entity.get_component(Positionable)
                    self.draw_light_ellipse(
                        light_surface,
                        pos,
                        light.outer_light_ellipse,
                        self.fade_color(light.color, 3 + light.flicker)
                    )

            # Second pass, inner lights
            for entity in light_entities:
                light = entity.get_component(Lightable)

                if light.toggled:
                    pos = entity.get_component(Positionable)
                    self.draw_light_ellipse(
                        light_surface,
                        pos,
                        light.inner_light_ellipse,
                        self.fade_color(light.color, 1 + light.flicker)
                    )

            sky_rect = pygame.Rect(
                sky_pos.x,
                sky_pos.y,
                sky_pos.width,
                sky_pos.height
            )
            r = sky_entity.get_component(Renderable)
            r.render_func = lambda brush, color: brush.blit(
                light_surface,
                sky_rect
            )

    def draw_light_ellipse(self, light_surface, pos, light_ellipse, color):
        light_rect = pygame.Rect(
            light_ellipse.x,
            light_ellipse.y,
            light_ellipse.width,
            light_ellipse.height
        )
        light_rect = light_rect.move(pos.x, pos.y)
        pygame.draw.ellipse(light_surface, color, light_rect)

    def fade_color(self, color, ratio):
        return (
            color[0],
            color[1],
            color[2],
            int(float(color[3]) / float(ratio))
        )
