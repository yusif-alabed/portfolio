import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
GREEN = (55, 190, 100)
RED = (235, 85, 85)


class ChapterOneIslandScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("battle.png")

        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.clue_names = ["Torn Map", "Brass Compass", "Golden Key"]
        self.correct_order = ["Brass Compass", "Torn Map", "Golden Key"]
        self.selected_clues = []

        self.clue_buttons = [
            Button(110, 370, 240, 60, "Torn Map"),
            Button(380, 370, 240, 60, "Brass Compass"),
            Button(650, 370, 240, 60, "Golden Key"),
        ]
        self.continue_button = Button(
            350,
            535,
            300,
            55,
            "Sail to the Gem",
        )

        self.message = "Choose the first clue."
        self.message_colour = CREAM
        self.complete = False

    def choose_clue(self, clue):
        expected = self.correct_order[len(self.selected_clues)]

        if clue == expected:
            self.selected_clues.append(clue)
            self.message = "Correct clue! Keep searching."
            self.message_colour = GREEN

            if len(self.selected_clues) == len(self.correct_order):
                self.complete = True
                self.message = (
                    "The clues reveal the Number Gem's hiding place!"
                )
        else:
            self.selected_clues = []
            self.message = "Wrong order. Start with the compass."
            self.message_colour = RED

    def handle_events(self, events):
        for event in events:
            if not self.complete:
                for number in range(len(self.clue_buttons)):
                    if self.clue_buttons[number].was_clicked(event):
                        clue = self.clue_names[number]

                        if clue not in self.selected_clues:
                            self.choose_clue(clue)

            elif self.continue_button.was_clicked(event):
                from game.scenes.battle_scene import BattleScene

                self.manager.change_scene(
                    BattleScene(
                        self.manager,
                        self.username,
                        self.student_id,
                        chapter_stage=2,
                    )
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        shade = pygame.Surface((1000, 700), pygame.SRCALPHA)
        shade.fill((0, 8, 25, 105))
        screen.blit(shade, (0, 0))

        title_panel = pygame.Rect(150, 45, 700, 95)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "Addition Atoll: The Hidden Clues",
            True,
            GOLD,
        )
        screen.blit(title, title.get_rect(center=title_panel.center))

        story_panel = pygame.Rect(120, 175, 760, 145)
        pygame.draw.rect(screen, NAVY, story_panel)
        pygame.draw.rect(screen, GOLD, story_panel, width=4)

        lines = [
            "A stone tablet gives you the order:",
            "Find direction, then the route, then unlock the treasure.",
            "Select the Compass, Map and Key in the correct order.",
        ]
        for number in range(len(lines)):
            image = self.text_font.render(lines[number], True, CREAM)
            rect = image.get_rect(center=(WIDTH // 2, 210 + number * 40))
            screen.blit(image, rect)

        if not self.complete:
            for button in self.clue_buttons:
                button.draw(screen)

        progress = self.small_font.render(
            "Clues found: "
            + str(len(self.selected_clues))
            + " / "
            + str(len(self.correct_order)),
            True,
            CREAM,
        )
        screen.blit(progress, progress.get_rect(center=(WIDTH // 2, 475)))

        message = self.text_font.render(
            self.message,
            True,
            self.message_colour,
        )
        screen.blit(message, message.get_rect(center=(WIDTH // 2, 505)))

        if self.complete:
            self.continue_button.draw(screen)
