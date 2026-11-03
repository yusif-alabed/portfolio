import pygame

WIDTH = 1000
HEIGHT = 700


def load_background(filename):
    image = pygame.image.load(
        "game/assets/backgrounds/" + filename
    ).convert()

    return pygame.transform.scale(
        image,
        (WIDTH, HEIGHT),
    )
