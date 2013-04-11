import os, pygame
from pygame.locals import *
import pygame.gfxdraw
import Leap
import time

pointer_radius = 4

class LeapDraw:
    """ This class handles all rendering. Positions to render should be updated here. """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.pointers = []
        self.pointers.append((0,0))

        self.resetBackground()

        self.should_draw = False

    def render(self):
        global pointer_radius
        self.screen.blit(self.background, (0, 0))
        if (self.should_draw):
            pygame.gfxdraw.filled_circle(self.background, self.pointers[0][0], self.pointers[0][1], pointer_radius, Color('red'))

        pygame.gfxdraw.filled_circle(self.screen, self.pointers[0][0], self.pointers[0][1], pointer_radius, Color('blue'))
        pygame.display.update()

    def resetBackground(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(Color('black'))

class LeapListener(Leap.Listener):
    def on_connect(self, controller):
        print "Connected to Leap"

    def on_frame(self, controller):
        global pointer_radius

        frame = controller.frame()

        pointer_count = 0

        if not frame.hands.empty:
            for hand in frame.hands:
                if not hand.fingers.empty:
                    for finger in hand.fingers:
                        pos = finger.tip_position

                        # It seems that actual range is about [-500, 500]
                        # but in practice, [-350, 350] is a better bet
                        x = pos.x
                        x += 350
                        x *= self.screen_size[0] / 700.0

                        if x < 0:
                            x = 0
                        elif x > self.screen_size[0] - pointer_radius:
                            x = self.screen_size[0] - pointer_radius

                        x = int(x)

                        # The actual range here is probably about [-500, 500] too
                        # but it lets the user relax their arm a bit not to use the full range
                        # May change this later
                        y = int(pos.y)
                        y = self.screen_size[1] - y
                        print "render at (%d, %d, %d)" % (x, y, int(pos.z))

                        self.renderer.pointers[pointer_count] = (x,y)

                        self.renderer.should_draw = pos.z < 0


def main():
    # Pygame init
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Leap Drawing')

    leap_controller = Leap.Controller()
    listener = LeapListener()

    renderer = LeapDraw()
    listener.renderer = renderer
    listener.screen_size = renderer.screen.get_size()

    leap_controller.add_listener(listener)

    time.sleep(.1)

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True

        renderer.render()
        # pygame.time.delay(10)
        time.sleep(.015)

    leap_controller.remove_listener(listener)

if __name__ == '__main__':
    main()
