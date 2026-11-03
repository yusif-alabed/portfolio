import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class SubjectScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")

        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("arial", 25)

        self.maths_button = Button(190, 335, 280, 70, "Maths Voyage")
        self.english_button = Button(530, 335, 280, 70, "English Voyage")
        self.back_button = Button(350, 470, 300, 55, "Return to Menu")

    def start_adventure(self, subject):
        self.manager.subject = subject

        from game.scenes.harbour_scene import HarbourScene

        self.manager.change_scene(
            HarbourScene(
                self.manager,
                self.username,
                self.student_id,
            )
        )

    def handle_events(self, events):
        for event in events:
            if self.maths_button.was_clicked(event):
                self.start_adventure("maths")

            if self.english_button.was_clicked(event):
                self.start_adventure("english")

            if self.back_button.was_clicked(event):
                from game.scenes.menu_scene import MenuScene

                self.manager.change_scene(
                    MenuScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        panel = pygame.Surface((760, 430), pygame.SRCALPHA)
        panel.fill((5, 18, 38, 230))
        pygame.draw.rect(panel, GOLD, panel.get_rect(), width=5)
        screen.blit(panel, (120, 110))

        title = self.title_font.render("Choose Your Voyage", True, GOLD)
        subtitle = self.text_font.render(
            "Which subject would you like to practise?",
            True,
            CREAM,
        )
        note = self.text_font.render(
            "Each subject remembers its own difficulty.",
            True,
            CREAM,
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 245)))
        screen.blit(note, note.get_rect(center=(WIDTH // 2, 285)))

        self.maths_button.draw(screen)
        self.english_button.draw(screen)
        self.back_button.draw(screen)
