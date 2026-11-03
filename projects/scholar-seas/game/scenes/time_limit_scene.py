import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class TimeLimitScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.background = load_background("ui.png")

        self.title_font = pygame.font.SysFont(
            "arial",
            48,
            bold=True,
        )
        self.text_font = pygame.font.SysFont(
            "arial",
            25,
        )

    def handle_events(self, events):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        notice_panel = pygame.Rect(150, 210, 700, 260)
        pygame.draw.rect(screen, NAVY, notice_panel)
        pygame.draw.rect(screen, GOLD, notice_panel, width=5)

        title = self.title_font.render(
            "Today's Voyage Is Complete!",
            True,
            GOLD,
        )

        message = self.text_font.render(
            "You have used today's playtime.",
            True,
            CREAM,
        )

        extra_message = self.text_font.render(
            "Come back tomorrow for another adventure.",
            True,
            CREAM,
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, 275)
        )
        message_rect = message.get_rect(
            center=(WIDTH // 2, 355)
        )
        extra_rect = extra_message.get_rect(
            center=(WIDTH // 2, 405)
        )

        screen.blit(title, title_rect)
        screen.blit(message, message_rect)
        screen.blit(extra_message, extra_rect)
