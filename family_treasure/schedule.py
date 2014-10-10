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

from animation import Animable
from ecs import Activable
from graphics import Renderable

class Step:
    """Represent a hook in a precise time to execute actions.
    """

    def __init__(self, time):
        self.time = time
        self.hooks = []
        self.chained_steps = []

    def call(self, func):
        """Ask to execute func at this step.
        """
        self.hooks.append(func)
        return self

    def animate(self, entity, animation):
        """Ask to execute an animation on an entity at this step.
        """
        self.hooks.append(lambda: self._execute_animation(entity, animation))
        return self

    def _execute_animation(self, entity, animation):
        """Execute animation on entity.
        """
        animable = entity.get_component(Animable)
        if animable is None:
            raise "Entity should have an Animable component"

        animable.add_animation(animation)

    def toggle(self, entity):
        """Activate / deactivate an entity at this step.

        entity must have the Activable component.
        """
        self.hooks.append(lambda: self.execute_toggle(entity))
        return self

    def execute_toggle(self, entity):
        """Toggle entity.
        """
        activable = entity.get_component(Activable)

        if activable is None:
            raise "Entity should have an Activable component"

        activable.toggle()

    def walk(self, character, direction, distance, duration):
        """Make entity walk at this step.
        """
        self.hooks.append(
            lambda: character.walk(direction, distance, duration)
        )
        return self

    def set_image(self, entity, image):
        """Set entity's image.
        """
        self.hooks.append(lambda: self.execute_set_image(entity, image))
        return self

    def execute_set_image(self, entity, image):
        renderable = entity.get_component(Renderable)

        if renderable is None:
            raise "Entity must be renderable"

        renderable.render_image(image)

    def run_hooks(self, steps):
        """Run all the hooks defined before.

        Append the chaind steps into steps
        """
        for hook in self.hooks:
            hook()

        steps += self.chained_steps

    def when(self, cond_func):
        """Return a new Step object, and register a hook that will execute the
        step only if cond_func() is true on the moment.
        """
        step = Step(0)
        self.hooks.append(
            lambda: (step.run_hooks(self.chained_steps) if cond_func() else None)
        )
        return step

    def after(self, duration):
        """Declare a hook that will be executed duration after this step.
        """
        step = Step(self.time + duration)
        self.chained_steps.append(step)
        return step


class Scheduler:
    """Class in charge of register hooks and executing them at the right time.
    """
    def __init__(self):
        self.steps = []
        self.time = 0

    def reset(self):
        """Reset scheduler.
        """
        self.time = 0
        self.steps[:] = []

    def at(self, time):
        """Return a step scheduled to run at time.
        """
        existing_steps = [step for step in self.steps if step.time == time]

        if existing_steps:
            step = existing_steps[0]
        else:
            step = Step(time)
            self.steps.append(step)

        return step

    def update(self, elapsed_time):
        """Update total time, and execute steps that must happen before this
        time.

        elapsed_time must be in the same unit of the one used with "at".
        """
        self.time += elapsed_time
        steps_to_execute = [step for step in self.steps if step.time <= self.time]
        for step in steps_to_execute:
            step.run_hooks(self.steps)
        self.steps = [step for step in self.steps if not step in steps_to_execute]
