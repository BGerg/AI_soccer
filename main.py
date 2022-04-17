import pygame as pygame

from inventory import create_field
from events import start_match, initialize_logic

pygame.init()
BLACK = (0, 0, 0)
WIDTH = 600
HEIGHT = 400
window_surface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
window_surface.fill(BLACK)


def run():
    create_field()  # players and ball
    initialize_logic()  # assign events and starting state
    start_match()  # start game loop


if __name__ == '__main__':
    run()

