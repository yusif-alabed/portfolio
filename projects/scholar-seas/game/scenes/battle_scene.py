import random

import pygame

from game.scenes.base_scene import Scene
from game.systems.audio import play_sound
from game.systems.question_queue import QuestionQueue
from game.ui.art import load_background
from game.ui.button import Button
from game.ui.outfit import load_outfit
from shared.database import (
    add_rewards,
    get_questions_by_topic,
    get_topic_progress,
    record_result,
    save_topic_progress,
)

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
RED = (235, 85, 85)
GREEN = (55, 190, 100)
GREY = (80, 80, 80)


class BattleScene(Scene):

    def __init__(
        self,
        manager,
        username,
        student_id,
        boss_battle=False,
        chapter_stage=1,
        free_play=False,
    ):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.boss_battle = boss_battle
        self.chapter_stage = chapter_stage
        self.free_play = free_play
        self.subject = getattr(self.manager, "subject", "maths")
        if self.boss_battle:
            self.attack_sound = "attack"
        else:
            self.attack_sound = "cannon"

        if self.boss_battle:
            self.background = load_background("skull_reef.png")
        else:
            self.background = load_background("battle.png")

        self.player_health = 100
        if self.boss_battle:
            self.enemy_health = 150
        else:
            self.enemy_health = 100
        self.battle_over = False
        self.player_won = False
        self.rewards_given = False

        self.question_start_time = 0

        progress = get_topic_progress(
            self.student_id,
            self.subject,
        )

        self.difficulty = progress["difficulty"]
        self.correct_streak = progress["correct_streak"]
        self.wrong_streak = progress["wrong_streak"]

        self.title_font = pygame.font.SysFont(
            "arial",
            36,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 25)
        self.message_font = pygame.font.SysFont("arial", 21)

        if self.boss_battle:
            self.player_ship = load_outfit(
                self.student_id,
                (192, 192),
            )

            self.enemy_ship = pygame.image.load(
                "game/assets/sprites/captain_blackreef.png"
            ).convert_alpha()
            self.enemy_ship = pygame.transform.scale(
                self.enemy_ship,
                (175, 230),
            )
        else:
            self.player_ship = pygame.image.load(
                "game/assets/sprites/player_ship.png"
            ).convert_alpha()
            self.player_ship = pygame.transform.scale(
                self.player_ship,
                (300, 200),
            )

            self.enemy_ship = pygame.image.load(
                "game/assets/sprites/enemy_ship.png"
            ).convert_alpha()
            self.enemy_ship = pygame.transform.scale(
                self.enemy_ship,
                (300, 200),
            )

        self.question_queue = QuestionQueue()
        self.current_question = None
        self.question_text = ""
        self.correct_answer = ""
        self.answers = []
        self.answer_buttons = []

        self.back_button = Button(
            350,
            610,
            300,
            50,
            "Return to Port",
        )

        self.message = "Choose the correct answer!"
        self.message_colour = CREAM

        self.load_questions()
        self.show_next_question()

    def load_questions(self):
        questions = list(
            get_questions_by_topic(
                self.subject,
                self.difficulty,
            )
        )

        random.shuffle(questions)

        for question in questions:
            self.question_queue.add(question)

    def show_next_question(self):
        if self.question_queue.is_empty():
            self.load_questions()

        self.current_question = self.question_queue.remove()
        self.question_start_time = pygame.time.get_ticks()

        if self.current_question is None:
            self.question_text = "No questions were found."
            self.answers = []
            self.answer_buttons = []
            return

        self.question_text = self.current_question["question_text"]
        self.correct_answer = self.current_question["correct_answer"]

        self.answers = [
            self.current_question["choice_a"],
            self.current_question["choice_b"],
            self.current_question["choice_c"],
            self.current_question["choice_d"],
        ]

        positions = [
            (170, 465),
            (530, 465),
            (170, 535),
            (530, 535),
        ]

        letters = ["A. ", "B. ", "C. ", "D. "]
        self.answer_buttons = []

        for number in range(4):
            x, y = positions[number]
            label = letters[number] + self.answers[number]

            button = Button(
                x,
                y,
                300,
                50,
                label,
            )

            self.answer_buttons.append(button)

    def handle_events(self, events):
        for event in events:
            if not self.battle_over:
                for number in range(len(self.answer_buttons)):
                    button = self.answer_buttons[number]

                    if button.was_clicked(event):
                        self.check_answer(
                            self.answers[number]
                        )

            if self.battle_over:
                if self.back_button.was_clicked(event):
                    if self.free_play:
                        from game.scenes.harbour_scene import HarbourScene

                        self.manager.change_scene(
                            HarbourScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )
                        )
                        continue

                    if self.player_won:
                        if self.boss_battle:
                            from game.scenes.astrolabe_scene import AstrolabeScene

                            new_scene = AstrolabeScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )
                        else:
                            if self.chapter_stage == 1:
                                from game.scenes.chapter_one_island_scene import (
                                    ChapterOneIslandScene,
                                )

                                new_scene = ChapterOneIslandScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )
                            else:
                                from game.scenes.chapter_complete_scene import (
                                    ChapterCompleteScene,
                                )

                                new_scene = ChapterCompleteScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )

                        self.manager.change_scene(new_scene)

                    else:
                        if self.boss_battle:
                            from game.scenes.skull_reef_scene import SkullReefScene

                            new_scene = SkullReefScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )
                        else:
                            from game.scenes.harbour_scene import HarbourScene

                            new_scene = HarbourScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )

                        self.manager.change_scene(new_scene)

    def adjust_difficulty(self, is_correct):
        old_difficulty = self.difficulty

        if is_correct:
            self.correct_streak += 1
            self.wrong_streak = 0

            if self.correct_streak >= 3:
                if self.difficulty < 3:
                    self.difficulty += 1

                self.correct_streak = 0

        else:
            self.wrong_streak += 1
            self.correct_streak = 0

            if self.wrong_streak >= 2:
                if self.difficulty > 1:
                    self.difficulty -= 1

                self.wrong_streak = 0

        if self.difficulty != old_difficulty:
            self.question_queue = QuestionQueue()

        save_topic_progress(
            self.student_id,
            self.subject,
            self.difficulty,
            self.correct_streak,
            self.wrong_streak,
        )

    def check_answer(self, chosen_answer):
        time_taken_ms = (
            pygame.time.get_ticks()
            - self.question_start_time
        )

        is_correct = (
            chosen_answer == self.correct_answer
        )

        record_result(
            self.student_id,
            self.current_question["question_id"],
            is_correct,
            time_taken_ms,
        )

        self.adjust_difficulty(is_correct)

        if is_correct:
            play_sound(self.attack_sound)
            self.enemy_health -= 25
            if self.boss_battle:
                self.message = "Correct! You strike Blackreef!"
            else:
                self.message = "Correct! Your cannon hits the enemy!"
            self.message_colour = GREEN
        else:
            play_sound("wrong")
            self.player_health -= 20
            if self.boss_battle:
                self.message = "Wrong! Blackreef strikes back!"
            else:
                self.message = "Wrong! The enemy fires back!"
            self.message_colour = RED

        if self.enemy_health <= 0:
            play_sound("victory")
            self.enemy_health = 0
            self.battle_over = True
            self.player_won = True
            if self.boss_battle:
                self.back_button.text = "Restore Astrolabe"
                self.message = (
                    "Blackreef defeated! You earned 40 coins and 80 XP!"
                )
                reward_coins = 40
                reward_xp = 80
            else:
                if self.free_play:
                    self.back_button.text = "Return to Harbour"
                    self.message = (
                        "Training victory! You earned 10 coins and 20 XP!"
                    )
                elif self.chapter_stage == 1:
                    self.back_button.text = "Explore Addition Atoll"
                else:
                    self.back_button.text = "Recover the Number Gem"
                self.message = (
                    "Victory! You earned 10 coins and 20 XP!"
                )
                reward_coins = 10
                reward_xp = 20
            self.message_colour = GOLD

            if not self.rewards_given:
                add_rewards(
                    self.student_id,
                    reward_coins,
                    reward_xp,
                )
                self.rewards_given = True

        elif self.player_health <= 0:
            play_sound("defeat")
            self.player_health = 0
            self.battle_over = True
            self.player_won = False
            self.back_button.text = "Return to Port"

            self.message = (
                "Defeat! Return to port and try again."
            )
            self.message_colour = RED

        else:
            self.show_next_question()

    def draw_health_bar(
        self,
        screen,
        x,
        y,
        health,
        label,
    ):
        label_image = self.message_font.render(
            label,
            True,
            CREAM,
        )

        label_panel = pygame.Rect(x, y - 31, 300, 29)
        pygame.draw.rect(screen, NAVY, label_panel)
        pygame.draw.rect(screen, GOLD, label_panel, width=2)
        screen.blit(label_image, (x, y - 28))

        pygame.draw.rect(
            screen,
            GREY,
            (x, y, 300, 25),
            border_radius=7,
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (x, y, health * 3, 25),
            border_radius=7,
        )

        pygame.draw.rect(
            screen,
            CREAM,
            (x, y, 300, 25),
            width=2,
            border_radius=7,
        )

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw(self, screen):
        self.draw_background(screen)

        heading_panel = pygame.Rect(270, 10, 460, 88)
        pygame.draw.rect(screen, NAVY, heading_panel)
        pygame.draw.rect(screen, GOLD, heading_panel, width=4)

        if self.boss_battle:
            battle_title = "Final Battle: Blackreef"
        elif self.free_play:
            battle_title = "Free Training Battle"
        else:
            battle_title = "Battle at Skull Bay"

        title = self.title_font.render(
            battle_title,
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 38)
        )
        screen.blit(title, title_rect)

        difficulty_image = self.message_font.render(
            "Question difficulty: "
            + str(self.difficulty),
            True,
            CREAM,
        )
        difficulty_rect = difficulty_image.get_rect(
            center=(WIDTH // 2, 76)
        )
        screen.blit(
            difficulty_image,
            difficulty_rect,
        )

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
            "Captain Blackreef" if self.boss_battle else "Enemy Ship",
        )

        if self.boss_battle:
            screen.blit(self.player_ship, (110, 160))
            screen.blit(self.enemy_ship, (720, 125))
        else:
            screen.blit(self.player_ship, (35, 150))
            screen.blit(self.enemy_ship, (665, 150))

        question_image = self.text_font.render(
            self.question_text,
            True,
            CREAM,
        )

        question_panel = pygame.Rect(215, 345, 570, 105)
        pygame.draw.rect(screen, NAVY, question_panel)
        pygame.draw.rect(screen, GOLD, question_panel, width=4)
        question_rect = question_image.get_rect(
            center=(WIDTH // 2, 375)
        )
        screen.blit(
            question_image,
            question_rect,
        )

        message_image = self.message_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message_image.get_rect(
            center=(WIDTH // 2, 420)
        )
        screen.blit(
            message_image,
            message_rect,
        )

        if self.battle_over:
            self.back_button.draw(screen)
        else:
            for button in self.answer_buttons:
                button.draw(screen)
