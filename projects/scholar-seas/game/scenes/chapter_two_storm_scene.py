import pygame

from game.scenes.base_scene import Scene
from game.systems.audio import play_sound
from game.ui.art import load_background
from game.ui.button import Button
from shared.database import add_rewards, get_story_chapter, save_story_chapter

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
GREEN = (45, 180, 95)
RED = (220, 65, 65)


class ChapterTwoStormScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("battle.png")

        self.title_font = pygame.font.SysFont("arial", 44, bold=True)
        self.text_font = pygame.font.SysFont("arial", 26)
        self.small_font = pygame.font.SysFont("arial", 21)

        self.west_button = Button(105, 505, 230, 60, "Sail West")
        self.north_button = Button(385, 505, 230, 60, "Sail North")
        self.east_button = Button(665, 505, 230, 60, "Sail East")
        self.continue_button = Button(
            350,
            585,
            300,
            60,
            "Continue Story",
        )

        self.challenges = [
            (
                "Black clouds block the northern route.",
                "The compass shows clear water to the east.",
                "East",
            ),
            (
                "Sharp reefs rise from the eastern waves.",
                "A safe channel opens to the north.",
                "North",
            ),
            (
                "Lightning strikes ahead of the ship.",
                "Treasure Island appears in the west.",
                "West",
            ),
        ]

        self.challenge_number = 0
        self.ship_health = 3
        self.complete = False
        self.message = "Choose the safest direction."
        self.message_colour = CREAM

    def handle_events(self, events):
        for event in events:
            if self.complete:
                if self.continue_button.was_clicked(event):
                    from game.scenes.chapter_two_complete_scene import (
                        ChapterTwoCompleteScene,
                    )

                    self.manager.change_scene(
                        ChapterTwoCompleteScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )
                continue

            if self.west_button.was_clicked(event):
                self.choose_direction("West")

            if self.north_button.was_clicked(event):
                self.choose_direction("North")

            if self.east_button.was_clicked(event):
                self.choose_direction("East")

    def choose_direction(self, direction):
        correct_direction = self.challenges[
            self.challenge_number
        ][2]

        if direction == correct_direction:
            play_sound("correct")
            self.challenge_number += 1

            if self.challenge_number == len(self.challenges):
                self.finish_challenge()
            else:
                self.message = "Correct! The ship sails onwards."
                self.message_colour = GREEN
        else:
            play_sound("wrong")
            self.ship_health -= 1
            self.message = "Wrong turn! The ship takes damage."
            self.message_colour = RED

            if self.ship_health == 0:
                self.ship_health = 3
                self.challenge_number = 0
                self.message = "The storm pushed you back. Try again!"

    def finish_challenge(self):
        play_sound("victory")
        self.complete = True
        self.message_colour = GREEN

        if get_story_chapter(self.student_id) <= 2:
            add_rewards(self.student_id, 15, 30)
            save_story_chapter(self.student_id, 3)
            self.message = "Storm cleared! You earned 15 coins and 30 XP!"
        else:
            self.message = "Storm cleared! Treasure Island is ahead."

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        dark_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_layer.fill((0, 5, 25, 125))
        screen.blit(dark_layer, (0, 0))

        title_panel = pygame.Rect(180, 35, 640, 95)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "The Storm Passage",
            True,
            GOLD,
        )
        title_rect = title.get_rect(center=(WIDTH // 2, 82))
        screen.blit(title, title_rect)

        if self.complete:
            line_one = "The dark clouds split apart."
            line_two = "Treasure Island is straight ahead!"
        else:
            challenge = self.challenges[self.challenge_number]
            line_one = challenge[0]
            line_two = challenge[1]

        panel = pygame.Rect(160, 175, 680, 240)
        panel_surface = pygame.Surface(
            (panel.width, panel.height),
            pygame.SRCALPHA,
        )
        panel_surface.fill((10, 25, 50, 225))
        screen.blit(panel_surface, panel.topleft)
        pygame.draw.rect(screen, GOLD, panel, width=5)

        lines = [line_one, line_two]
        y_position = 235

        for line in lines:
            image = self.text_font.render(line, True, CREAM)
            image_rect = image.get_rect(
                center=(WIDTH // 2, y_position)
            )
            screen.blit(image, image_rect)
            y_position += 65

        if self.complete:
            progress_text = "Passage complete"
        else:
            progress_text = (
                "Decision "
                + str(self.challenge_number + 1)
                + " / "
                + str(len(self.challenges))
                + "     Ship strength: "
                + "♥" * self.ship_health
            )

        progress = self.small_font.render(
            progress_text,
            True,
            GOLD,
        )
        progress_rect = progress.get_rect(center=(WIDTH // 2, 370))
        screen.blit(progress, progress_rect)

        message = self.small_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message.get_rect(center=(WIDTH // 2, 460))
        screen.blit(message, message_rect)

        if self.complete:
            self.continue_button.draw(screen)
        else:
            self.west_button.draw(screen)
            self.north_button.draw(screen)
            self.east_button.draw(screen)
