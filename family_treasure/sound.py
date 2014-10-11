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
from data import filepath


class SoundSystem:
    """In charge of handling sounds.
    """

    def __init__(self, configuration):
        """Initialization

        configuration is a dictionary associating a sound name to its file.
        """
        self.sounds = {}
        for pair in configuration.iteritems():
            self.sounds[pair[0]] = pygame.mixer.Sound(
                filepath(pair[1])
            )

    def play(self, name):
        """Play the sound associated to name.
        """
        self.sounds[name].play()
