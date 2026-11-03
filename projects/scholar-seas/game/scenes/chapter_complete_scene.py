import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button
from shared.database import save_story_chapter

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)


class ChapterCompleteScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")

        save_story_chapter(
            self.student_id,
            2,
        )

        self.title_font = pygame.font.SysFont(
            "arial",
            48,
            bold=True,
        )
        self.text_font = pygame.font.SysFont(
            "arial",
            25,
        )

        self.menu_button = Button(
            350,
            545,
            300,
            55,
            "Return to Harbour",
        )

    def handle_events(self, events):
        for event in events:
            if self.menu_button.was_clicked(event):
                from game.scenes.harbour_scene import HarbourScene

                self.manager.change_scene(
                    HarbourScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_panel = pygame.Rect(245, 70, 510, 100)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "Chapter 1 Complete!",
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 120)
        )
        screen.blit(title, title_rect)

        panel = pygame.Rect(
            150,
            200,
            700,
            260,
        )

        pygame.draw.rect(
            screen,
            CREAM,
            panel,
            border_radius=15,
        )
        pygame.draw.rect(
            screen,
            GOLD,
            panel,
            width=5,
            border_radius=15,
        )

        story_lines = [
            "The enemy ship retreats from Addition Atoll!",
            "You recover the first Number Gem from the sea.",
            "Captain Coral will be waiting for you at the port.",
        ]

        y_position = 265

        for line in story_lines:
            text = self.text_font.render(
                line,
                True,
                BROWN,
            )
            text_rect = text.get_rect(
                center=(WIDTH // 2, y_position)
            )
            screen.blit(text, text_rect)

            y_position += 60

        self.menu_button.draw(screen)
