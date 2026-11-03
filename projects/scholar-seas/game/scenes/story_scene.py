import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)


class StoryScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")

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
            550,
            240,
            55,
            "Continue",
        )

        self.story_page = 0

        self.story = [
            [
                "Captain Coral has summoned you to the harbour.",
                "A mysterious storm has scattered the Number Gems",
                "across the islands of Scholar Seas.",
            ],
            [
                "Without the gems, the islands are losing their",
                "knowledge. A pirate named Captain Confusion wants",
                "to hide them forever.",
            ],
            [
                "Your first clue points towards Addition Atoll.",
                "The route is patrolled by Captain Confusion's fleet.",
                "You will have to fight your way through.",
            ],
            [
                "Captain Coral has marked a safe route on your map.",
                "Win the first battle, land on Addition Atoll and",
                "search the beach for the three missing clues.",
            ],
            [
                "The Number Gem is guarded beyond the island.",
                "Prepare your ship and answer the learning questions",
                "to complete your first voyage!",
            ],
        ]

    def handle_events(self, events):
        for event in events:
            if self.continue_button.was_clicked(event):
                self.story_page += 1

                if self.story_page >= len(self.story):
                    self.story_page = len(self.story) - 1
                    from game.scenes.harbour_scene import HarbourScene

                    self.manager.active_mission = (
                        "chapter_1_battle"
                    )

                    self.manager.change_scene(
                        HarbourScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_panel = pygame.Rect(170, 65, 660, 90)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "Chapter 1: The Missing Gems",
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 110)
        )
        screen.blit(title, title_rect)

        story_panel = pygame.Rect(
            140,
            190,
            720,
            280,
        )

        pygame.draw.rect(
            screen,
            CREAM,
            story_panel,
            border_radius=15,
        )
        pygame.draw.rect(
            screen,
            GOLD,
            story_panel,
            width=5,
            border_radius=15,
        )

        lines = self.story[self.story_page]

        y_position = 255

        for line in lines:
            text = self.text_font.render(
                line,
                True,
                BROWN,
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
        page_panel = pygame.Rect(440, 480, 120, 40)
        pygame.draw.rect(screen, NAVY, page_panel)
        pygame.draw.rect(screen, GOLD, page_panel, width=3)
        page_rect = page_text.get_rect(
            center=page_panel.center
        )
        screen.blit(page_text, page_rect)

        self.continue_button.draw(screen)
