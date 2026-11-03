from pathlib import Path

import pygame

MUSIC_FILE = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "music"
    / "pirates_orchestra.mp3"
)
SFX_FOLDER = Path(__file__).resolve().parents[1] / "assets" / "sfx"
sounds = {}


def start_music():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(str(MUSIC_FILE))
        pygame.mixer.music.set_volume(0.22)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Music could not be played.")


def play_sound(name):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        if name not in sounds:
            extension = ".wav"
            if name == "cannon":
                extension = ".ogg"

            sounds[name] = pygame.mixer.Sound(
                str(SFX_FOLDER / (name + extension))
            )
            sounds[name].set_volume(0.45)

        sounds[name].play()
    except (pygame.error, FileNotFoundError):
        pass
