import pygame, sys
from graphics import Screen

class Game:
    """Basic game launcher class
    Usage:
    >> game = Game(fps, (width, height))
    >> game.run()
    """

    def __init__(self, fps, window_size):
        self.fps = fps
        self.window_size = window_size

    def run(self):
        """Execute the game loop"""
        pygame.init()
        screen = Screen(self.window_size)
        clock = pygame.time.Clock()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #TODO: call ClickSystem
                    print("Someone clicked")

            #TODO: call GraphicsSystem
            screen.fill((0,0,0))
            screen.flip()

            clock.tick(self.fps)
