import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button
from shared.database import get_student

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class MenuScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")
        student = get_student(student_id)
        self.coins = student["coins"]
        self.xp = student["xp"]
        self.level = student["level"]

        self.title_font = pygame.font.SysFont(
            "arial",
            50,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 25)

        self.battle_button = Button(
            180,
            300,
            280,
            60,
            "Explore Harbour",
        )
        self.shop_button = Button(
            540,
            300,
            280,
            60,
            "Pirate Shop",
        )
        self.logout_button = Button(
            540,
            410,
            280,
            60,
            "Log out",
        )
        self.character_button = Button(
            180,
            410,
            280,
            60,
            "My Pirate",
        )

        self.message = "Choose your next adventure."

    def handle_events(self, events):
        for event in events:
            if self.battle_button.was_clicked(event):
                from game.scenes.subject_scene import SubjectScene

                self.manager.change_scene(
                    SubjectScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

            if self.shop_button.was_clicked(event):
                from game.scenes.shop_scene import ShopScene

                self.manager.change_scene(
                    ShopScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

            if self.logout_button.was_clicked(event):
                from game.scenes.login_scene import LoginScene

                self.manager.change_scene(
                    LoginScene(self.manager)
                )
            if self.character_button.was_clicked(event):
                from game.scenes.character_scene import CharacterScene

                self.manager.change_scene(
                    CharacterScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        information_panel = pygame.Surface(
            (700, 190),
            pygame.SRCALPHA,
        )
        information_panel.fill((5, 18, 38, 220))
        pygame.draw.rect(
            information_panel,
            GOLD,
            information_panel.get_rect(),
            width=5,
        )
        screen.blit(information_panel, (150, 35))

        title = self.title_font.render(
            "Scholar Seas",
            True,
            GOLD,
        )
        welcome = self.text_font.render(
            "Welcome aboard, " + self.username + "!",
            True,
            CREAM,
        )
        message = self.text_font.render(
            self.message,
            True,
            CREAM,
        )
        status = self.text_font.render(
            "Level "
            + str(self.level)
            + "    Coins: "
            + str(self.coins)
            + "    XP: "
            + str(self.xp),
            True,
            GOLD,
        )

        title_rect = title.get_rect(center=(WIDTH // 2, 85))
        welcome_rect = welcome.get_rect(center=(WIDTH // 2, 145))
        status_rect = status.get_rect(center=(WIDTH // 2, 190))
        message_rect = message.get_rect(center=(WIDTH // 2, 620))

        screen.blit(title, title_rect)
        screen.blit(welcome, welcome_rect)
        screen.blit(status, status_rect)

        self.battle_button.draw(screen)
        self.shop_button.draw(screen)
        self.logout_button.draw(screen)
        self.character_button.draw(screen)

        message_panel = pygame.Rect(250, 590, 500, 55)
        pygame.draw.rect(screen, NAVY, message_panel)
        pygame.draw.rect(screen, GOLD, message_panel, width=4)
        screen.blit(message, message_rect)
