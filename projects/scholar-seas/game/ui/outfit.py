import pygame

from shared.database import get_student

image_cache = {}


def resize_sprite(image, size):
    return pygame.transform.smoothscale(image, size)


def load_outfit(student_id, size, direction="down"):
    student = get_student(student_id)

    hat_names = {
        None: "none",
        "Deckhand Bandana": "bandana",
        "Navigator Hat": "navigator",
        "Captain's Tricorn": "captain",
    }
    coat_names = {
        None: "none",
        "Sailor Coat": "sailor",
        "Royal Captain Coat": "royal",
    }
    weapon_names = {
        None: "none",
        "Wooden Cutlass": "wooden",
        "Golden Cutlass": "golden",
    }

    hat = hat_names[student["equipped_hat"]]
    coat = coat_names[student["equipped_coat"]]
    weapon = weapon_names[student["equipped_weapon"]]

    filename = hat + "_" + coat + "_" + weapon + ".png"
    path = (
        "game/assets/sprites/outfits_v3/"
        + direction
        + "/"
        + filename
    )

    if path not in image_cache:
        image_cache[path] = pygame.image.load(path).convert_alpha()

    return resize_sprite(image_cache[path], size)
