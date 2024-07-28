import pygame
import sys

from pygame.locals import *

img_bg = 
def main():
    pygame.init()
    pygame.display.set_caption("PenPen")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
