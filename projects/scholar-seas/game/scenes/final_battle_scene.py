import pygame

from game.scenes.battle_scene import BattleScene
from game.ui.art import load_background
from game.ui.outfit import load_outfit

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
RED = (180, 45, 45)
GREEN = (35, 150, 80)
GREY = (55, 60, 70)


class FinalBattleScene(BattleScene):

    def __init__(self, manager, username, student_id):
        super().__init__(
            manager,
            username,
            student_id,
            boss_battle=True,
        )

        self.background = load_background("blackreef_arena.png")

        self.big_title_font = pygame.font.SysFont(
            "arial",
            38,
            bold=True,
        )
        self.name_font = pygame.font.SysFont(
            "arial",
            22,
            bold=True,
        )
        self.player_ship = load_outfit(
            self.student_id,
            (145, 145),
        )
        self.enemy_ship = pygame.transform.scale(
            self.enemy_ship,
            (135, 178),
        )

    def draw_panel(self, screen, rectangle, border_colour=GOLD):
        panel = pygame.Surface(
            (rectangle.width, rectangle.height),
            pygame.SRCALPHA,
        )
        panel.fill((10, 25, 50, 225))
        screen.blit(panel, rectangle.topleft)
        pygame.draw.rect(
            screen,
            border_colour,
            rectangle,
            width=4,
            border_radius=8,
        )

    def draw_boss_health(
        self,
        screen,
        x,
        y,
        width,
        health,
        maximum,
        colour,
    ):
        pygame.draw.rect(
            screen,
            GREY,
            (x, y, width, 24),
            border_radius=7,
        )

        filled_width = int(width * health / maximum)
        pygame.draw.rect(
            screen,
            colour,
            (x, y, filled_width, 24),
            border_radius=7,
        )

        pygame.draw.rect(
            screen,
            CREAM,
            (x, y, width, 24),
            width=2,
            border_radius=7,
        )

        health_text = self.message_font.render(
            str(health) + " / " + str(maximum),
            True,
            CREAM,
        )
        health_rect = health_text.get_rect(
            center=(x + width // 2, y + 12)
        )
        screen.blit(health_text, health_rect)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        darkness = pygame.Surface((1000, 700), pygame.SRCALPHA)
        darkness.fill((0, 8, 25, 35))
        screen.blit(darkness, (0, 0))

        heading_panel = pygame.Rect(185, 12, 630, 82)
        self.draw_panel(screen, heading_panel)

        title = self.big_title_font.render(
            "THE FINAL DUEL",
            True,
            GOLD,
        )
        title_rect = title.get_rect(center=(WIDTH // 2, 39))
        screen.blit(title, title_rect)

        subtitle = self.message_font.render(
            "Defeat Captain Blackreef and reclaim the Astrolabe",
            True,
            CREAM,
        )
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 72))
        screen.blit(subtitle, subtitle_rect)

        player_panel = pygame.Rect(35, 105, 285, 78)
        boss_panel = pygame.Rect(680, 105, 285, 78)
        self.draw_panel(screen, player_panel)
        self.draw_panel(screen, boss_panel, RED)

        player_name = self.name_font.render(
            self.username,
            True,
            CREAM,
        )
        player_name_rect = player_name.get_rect(center=(178, 124))
        screen.blit(player_name, player_name_rect)

        boss_name = self.name_font.render(
            "CAPTAIN BLACKREEF",
            True,
            CREAM,
        )
        boss_name_rect = boss_name.get_rect(center=(822, 124))
        screen.blit(boss_name, boss_name_rect)

        self.draw_boss_health(
            screen,
            60,
            145,
            235,
            self.player_health,
            100,
            GREEN,
        )
        self.draw_boss_health(
            screen,
            705,
            145,
            235,
            self.enemy_health,
            150,
            RED,
        )

        floor_y = 375
        player_x = 125
        boss_x = 755
        player_y = floor_y - self.player_ship.get_height()
        boss_y = floor_y - self.enemy_ship.get_height()

        pygame.draw.ellipse(screen, (8, 8, 12), (116, 358, 125, 22))
        pygame.draw.ellipse(screen, (8, 8, 12), (742, 358, 160, 24))
        screen.blit(self.player_ship, (player_x, player_y))
        screen.blit(self.enemy_ship, (boss_x, boss_y))

        difficulty = self.message_font.render(
            self.subject.title()
            + " difficulty "
            + str(self.difficulty),
            True,
            CREAM,
        )
        difficulty_panel = pygame.Rect(410, 126, 180, 36)
        self.draw_panel(screen, difficulty_panel)
        difficulty_rect = difficulty.get_rect(center=difficulty_panel.center)
        screen.blit(difficulty, difficulty_rect)

        question_panel = pygame.Rect(120, 390, 760, 65)
        self.draw_panel(screen, question_panel)

        question_image = self.text_font.render(
            self.question_text,
            True,
            CREAM,
        )
        question_rect = question_image.get_rect(center=(500, 409))
        screen.blit(question_image, question_rect)

        message_image = self.message_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message_image.get_rect(center=(500, 438))
        screen.blit(message_image, message_rect)

        if self.battle_over:
            self.back_button.draw(screen)
        else:
            for button in self.answer_buttons:
                button.draw(screen)
