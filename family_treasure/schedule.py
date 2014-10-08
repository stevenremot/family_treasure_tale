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

class Step:
    """Represent a hook in a precise time to execute actions.
    """

    def __init__(self, time):
        self.time = time
        self.hooks = []

    def call(self, func):
        """Ask to execute func at this step.
        """
        self.hooks.append(func)

    def animate(self, entity, animation):
        """Ask to execute an animation on an entity at this step.
        """
        self.hooks.append(lambda: self._execute_animation(entity, animation))

    def _execute_animation(self, entity, animation):
        """Execute animation on entity.
        """
        animable = entity.get_component(Animable)
        if animable is None:
            raise "Entity should have an Animable component"

        animable.add_animation(animation)

    def run_hooks(self):
        """Run all the hooks defined before.
        """
        for hook in self.hooks:
            hook()

    def when(self, cond_func):
        """Return a new Step object, and register a hook that will execute the
        step only if cond_func() is true on the moment.
        """
        step = Step(0)
        self.hooks.append(lambda: (step.run_hooks() if cond_func() else None))
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
            step.run_hooks()
        self.steps = [step for step in self.steps if not step in steps_to_execute]
