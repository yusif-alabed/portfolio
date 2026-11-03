import pygame

CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)
RED = (180, 45, 45)


class NPC:

    def __init__(self, x, y, name):
        self.name = name

        self.image = pygame.image.load(
            "game/assets/sprites/captain_coral.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (70, 96),
        )

        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

        self.font = pygame.font.SysFont(
            "arial",
            17,
            bold=True,
        )

    def is_near(self, player_rect):
        interaction_area = self.rect.inflate(
            100,
            100,
        )

        return interaction_area.colliderect(
            player_rect
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        name_image = self.font.render(
            self.name,
            True,
            CREAM,
        )
        name_shadow = self.font.render(
            self.name,
            True,
            (0, 0, 0),
        )
        name_rect = name_image.get_rect(
            center=(self.rect.centerx, self.rect.y - 15)
        )

        screen.blit(name_shadow, name_rect.move(2, 2))
        screen.blit(name_image, name_rect)
