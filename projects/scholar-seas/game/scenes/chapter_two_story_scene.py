import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class ChapterTwoStoryScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("chapter_two.png")
        self.story_page = 0

        self.title_font = pygame.font.SysFont(
            "arial",
            44,
            bold=True,
        )
        self.text_font = pygame.font.SysFont(
            "arial",
            25,
        )

        self.continue_button = Button(
            380,
            515,
            240,
            55,
            "Continue",
        )

        self.story = [
            [
                "The first Number Gem has revealed a map.",
                "It points towards a dangerous chain of islands.",
                "Captain Coral needs your navigation skills.",
            ],
            [
                "Each sea route has a different danger level.",
                "Choose connected islands and keep the total",
                "danger as low as possible.",
            ],
            [
                "The map only shows part of the journey.",
                "A fierce storm guards the final crossing.",
                "You must keep the ship away from danger.",
            ],
            [
                "First, chart the safest route across the islands.",
                "Then steer through the storm using the compass.",
                "One wrong turn could damage the ship.",
            ],
            [
                "Treasure Island waits beyond the dark clouds.",
                "The second Number Gem may be hidden there.",
                "Take the wheel, Navigator!",
            ],
        ]

    def handle_events(self, events):
        for event in events:
            if self.continue_button.was_clicked(event):
                self.story_page += 1

                if self.story_page >= len(self.story):
                    self.story_page = len(self.story) - 1
                    from game.scenes.puzzle_scene import PuzzleScene

                    self.manager.change_scene(
                        PuzzleScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        dark_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_layer.fill((0, 0, 15, 55))
        screen.blit(dark_layer, (0, 0))

        title_panel = pygame.Rect(155, 25, 690, 80)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "Chapter 2: The Navigator's Trial",
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 65)
        )
        screen.blit(title, title_rect)

        panel = pygame.Surface((620, 250), pygame.SRCALPHA)
        panel.fill((10, 25, 50, 225))
        screen.blit(panel, (190, 130))
        pygame.draw.rect(screen, GOLD, (190, 130, 620, 250), width=5)

        y_position = 190

        for line in self.story[self.story_page]:
            text = self.text_font.render(
                line,
                True,
                CREAM,
            )
            text_rect = text.get_rect(
                center=(WIDTH // 2, y_position)
            )
            screen.blit(text, text_rect)

            y_position += 55

        page_text = self.text_font.render(
            str(self.story_page + 1)
            + " / "
            + str(len(self.story)),
            True,
            CREAM,
        )
        page_panel = pygame.Rect(440, 410, 120, 40)
        pygame.draw.rect(screen, NAVY, page_panel)
        pygame.draw.rect(screen, GOLD, page_panel, width=3)
        page_rect = page_text.get_rect(
            center=page_panel.center
        )
        screen.blit(page_text, page_rect)

        self.continue_button.draw(screen)
