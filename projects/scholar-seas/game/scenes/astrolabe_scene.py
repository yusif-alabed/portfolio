import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button
from shared.database import save_story_chapter

WIDTH = 1000

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class AstrolabeScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("astrolabe_restored.png")

        save_story_chapter(self.student_id, 4)
        self.manager.active_mission = None

        self.title_font = pygame.font.SysFont(
            "arial",
            36,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 25)

        self.harbour_button = Button(
            350,
            620,
            300,
            55,
            "Continue",
        )

        self.story_page = 0
        self.story = [
            [
                "The three Number Gems rise into the air.",
                "Their light awakens the Golden Astrolabe!",
            ],
            [
                "Golden light travels across Scholar Seas.",
                "Knowledge returns to every island once more.",
            ],
            [
                "Captain Coral names you a Legendary Navigator.",
                "You defeated Blackreef through knowledge and courage!",
            ],
        ]

    def handle_events(self, events):
        for event in events:
            if self.harbour_button.was_clicked(event):
                if self.story_page < len(self.story) - 1:
                    self.story_page += 1

                    if self.story_page == len(self.story) - 1:
                        self.harbour_button.text = "Return to Harbour"

                    return

                else:
                    from game.scenes.harbour_scene import HarbourScene

                    self.manager.change_scene(
                        HarbourScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_panel = pygame.Rect(160, 25, 680, 78)
        title_surface = pygame.Surface(
            title_panel.size,
            pygame.SRCALPHA,
        )
        title_surface.fill((10, 25, 50, 225))
        screen.blit(title_surface, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            "The Golden Astrolabe Is Restored!",
            True,
            GOLD,
        )
        title_rect = title.get_rect(center=title_panel.center)
        screen.blit(title, title_rect)

        story_panel = pygame.Rect(115, 500, 770, 100)
        story_surface = pygame.Surface(
            story_panel.size,
            pygame.SRCALPHA,
        )
        story_surface.fill((10, 25, 50, 225))
        screen.blit(story_surface, story_panel)
        pygame.draw.rect(screen, GOLD, story_panel, width=5)

        lines = self.story[self.story_page]

        y_position = 530
        for line in lines:
            text = self.text_font.render(line, True, CREAM)
            text_rect = text.get_rect(
                center=(WIDTH // 2, y_position)
            )
            screen.blit(text, text_rect)
            y_position += 38

        self.harbour_button.draw(screen)
