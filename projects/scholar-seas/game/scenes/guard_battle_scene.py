import pygame

from game.scenes.battle_scene import BattleScene
from game.ui.art import load_background
from game.ui.outfit import load_outfit

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class GuardBattleScene(BattleScene):

    def __init__(
        self,
        manager,
        username,
        student_id,
        reef_scene,
        guard,
    ):
        super().__init__(manager, username, student_id)

        self.reef_scene = reef_scene
        self.guard = guard
        self.attack_sound = "attack"

        self.background = load_background("guard_arena.png")
        self.player_ship = load_outfit(
            self.student_id,
            (175, 175),
        )

        guard_image = pygame.image.load(
            "game/assets/sprites/reef_guard.png"
        ).convert_alpha()
        self.enemy_ship = pygame.transform.scale(
            guard_image,
            (115, 173),
        )

        self.message = "Defeat the skeleton guard to continue!"

    def handle_events(self, events):
        for event in events:
            if not self.battle_over:
                for number in range(len(self.answer_buttons)):
                    button = self.answer_buttons[number]

                    if button.was_clicked(event):
                        self.check_answer(self.answers[number])

            elif self.back_button.was_clicked(event):
                if self.player_won:
                    if self.guard in self.reef_scene.guards:
                        self.reef_scene.guards.remove(self.guard)

                    self.reef_scene.show_message(
                        "Skeleton guard defeated! The path is clear."
                    )
                else:
                    self.reef_scene.player.rect.center = (1200, 1480)
                    self.reef_scene.show_message(
                        "The skeleton guard won. You escaped to the dock."
                    )

                self.reef_scene.caught_cooldown = 1
                self.manager.change_scene(self.reef_scene)

    def check_answer(self, chosen_answer):
        super().check_answer(chosen_answer)

        if self.battle_over:
            self.back_button.text = "Return to Maze"

            if self.player_won:
                self.message = (
                    "Skeleton defeated! You earned 10 coins and 20 XP!"
                )
                self.message_colour = GOLD
            else:
                self.message = "Defeat! Escape and try again."

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        dark_layer = pygame.Surface((1000, 700), pygame.SRCALPHA)
        dark_layer.fill((0, 0, 20, 70))
        screen.blit(dark_layer, (0, 0))

        heading_panel = pygame.Rect(270, 12, 460, 88)
        pygame.draw.rect(screen, NAVY, heading_panel)
        pygame.draw.rect(screen, GOLD, heading_panel, width=4)

        title = self.title_font.render(
            "Skeleton Guard Battle",
            True,
            GOLD,
        )
        title_rect = title.get_rect(center=(WIDTH // 2, 40))
        screen.blit(title, title_rect)

        difficulty = self.message_font.render(
            "Question difficulty: " + str(self.difficulty),
            True,
            CREAM,
        )
        difficulty_rect = difficulty.get_rect(center=(WIDTH // 2, 76))
        screen.blit(difficulty, difficulty_rect)

        self.draw_health_bar(
            screen,
            55,
            130,
            self.player_health,
            self.username,
        )
        self.draw_health_bar(
            screen,
            645,
            130,
            self.enemy_health,
            "Skeleton Guard",
        )

        screen.blit(self.player_ship, (115, 170))
        screen.blit(self.enemy_ship, (755, 172))

        question_panel = pygame.Rect(215, 345, 570, 105)
        pygame.draw.rect(screen, NAVY, question_panel)
        pygame.draw.rect(screen, GOLD, question_panel, width=4)

        question = self.text_font.render(
            self.question_text,
            True,
            CREAM,
        )
        question_rect = question.get_rect(center=(WIDTH // 2, 375))
        screen.blit(question, question_rect)

        message = self.message_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message.get_rect(center=(WIDTH // 2, 420))
        screen.blit(message, message_rect)

        if self.battle_over:
            self.back_button.draw(screen)
        else:
            for button in self.answer_buttons:
                button.draw(screen)
