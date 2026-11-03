import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)


class ChapterThreeStoryScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")
        self.story_page = 0

        self.title_font = pygame.font.SysFont(
            "arial",
            36,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 25)

        self.continue_button = Button(
            380,
            550,
            240,
            55,
            "Continue",
        )

        self.story = [
            [
                "The two Number Gems point towards Skull Reef.",
                "Captain Blackreef guards the final gem inside",
                "his ruined fortress.",
            ],
            [
                "The reef is filled with winding paths and rocks.",
                "Find your way from the dock to the fortress",
                "without getting trapped.",
            ],
            [
                "Blackreef believes strength always wins.",
                "Show him that knowledge is the greatest",
                "treasure on Scholar Seas!",
            ],
        ]

    def handle_events(self, events):
        for event in events:
            if self.continue_button.was_clicked(event):
                self.story_page += 1

                if self.story_page >= len(self.story):
                    self.story_page = len(self.story) - 1
                    from game.scenes.skull_reef_scene import SkullReefScene

                    self.manager.active_mission = "chapter_3_boss"
                    self.manager.change_scene(
                        SkullReefScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_panel = pygame.Rect(135, 65, 730, 90)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "Chapter 3: The Fortress of Skull Reef",
            True,
            GOLD,
        )
        title_rect = title.get_rect(center=title_panel.center)
        screen.blit(title, title_rect)

        story_panel = pygame.Rect(140, 190, 720, 280)
        pygame.draw.rect(screen, CREAM, story_panel)
        pygame.draw.rect(screen, GOLD, story_panel, width=5)

        y_position = 255

        for line in self.story[self.story_page]:
            text = self.text_font.render(line, True, BROWN)
            text_rect = text.get_rect(
                center=(WIDTH // 2, y_position)
            )
            screen.blit(text, text_rect)
            y_position += 55

        page_panel = pygame.Rect(440, 480, 120, 40)
        pygame.draw.rect(screen, NAVY, page_panel)
        pygame.draw.rect(screen, GOLD, page_panel, width=3)

        page_text = self.text_font.render(
            str(self.story_page + 1)
            + " / "
            + str(len(self.story)),
            True,
            CREAM,
        )
        page_rect = page_text.get_rect(center=page_panel.center)
        screen.blit(page_text, page_rect)

        self.continue_button.draw(screen)
