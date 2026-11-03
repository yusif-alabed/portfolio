from datetime import date

import pygame

from game.scenes.base_scene import Scene
from game.scenes.login_scene import LoginScene
from game.scenes.time_limit_scene import TimeLimitScene
from game.systems.audio import start_music
from game.ui.art import load_background
from shared.database import add_play_seconds, get_seconds_played_today, get_settings

WIDTH = 1000
HEIGHT = 700
FPS = 60

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)


class StartScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.background = load_background("ui.png")

        self.title_font = pygame.font.SysFont(
            "arial",
            64,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 28)
        self.message = "Press SPACE to begin your adventure"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.change_scene(
                        LoginScene(self.manager)
                    )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        panel = pygame.Surface((700, 210), pygame.SRCALPHA)
        panel.fill((5, 18, 38, 220))
        pygame.draw.rect(panel, GOLD, panel.get_rect(), width=5)
        screen.blit(panel, (150, 225))

        title = self.title_font.render(
            "Scholar Seas",
            True,
            GOLD,
        )
        message = self.text_font.render(
            self.message,
            True,
            CREAM,
        )

        title_shadow = self.title_font.render(
            "Scholar Seas",
            True,
            (0, 0, 0),
        )
        message_shadow = self.text_font.render(
            self.message,
            True,
            (0, 0, 0),
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, 290)
        )
        message_rect = message.get_rect(
            center=(WIDTH // 2, 380)
        )

        screen.blit(title_shadow, title_rect.move(4, 4))
        screen.blit(message_shadow, message_rect.move(3, 3))
        screen.blit(title, title_rect)
        screen.blit(message, message_rect)


class SceneManager:

    def __init__(self):
        self.current_scene = None
        self.next_scene = None
        self.running = True

        self.fade_alpha = 0
        self.fade_direction = 0
        self.fade_speed = 650

        self.student_id = None
        self.play_seconds = 0
        self.saved_seconds = 0
        self.time_limit_seconds = None
        self.active_mission = None
        self.subject = "maths"

    def change_scene(self, new_scene):
        if isinstance(new_scene, LoginScene):
            self.save_playtime()
            self.student_id = None
            self.active_mission = None
            self.subject = "maths"

        if self.current_scene is None:
            self.current_scene = new_scene
        else:
            self.next_scene = new_scene
            self.fade_direction = 1

    def update_transition(self, dt):
        if self.fade_direction == 1:
            self.fade_alpha += self.fade_speed * dt

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.current_scene = self.next_scene
                self.next_scene = None
                self.fade_direction = -1

        elif self.fade_direction == -1:
            self.fade_alpha -= self.fade_speed * dt

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0

    def draw_transition(self, screen):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        fade.set_alpha(int(self.fade_alpha))
        screen.blit(fade, (0, 0))

    def start_tracking(self, student_id):
        self.student_id = student_id
        self.play_seconds = 0
        self.saved_seconds = get_seconds_played_today(
            student_id
        )

        settings = get_settings(student_id)

        if settings is None:
            self.time_limit_seconds = None
            return

        if date.today().weekday() < 5:
            limit_minutes = settings["weekday_limit_min"]
        else:
            limit_minutes = settings["weekend_limit_min"]

        self.time_limit_seconds = limit_minutes * 60

    def update_playtime(self, dt):
        if self.student_id is None:
            return

        self.play_seconds += dt

        total_seconds = self.saved_seconds + self.play_seconds

        if (
            self.time_limit_seconds is not None
            and total_seconds >= self.time_limit_seconds
        ):
            self.save_playtime()
            self.student_id = None
            self.change_scene(TimeLimitScene(self))
            return

        if self.play_seconds >= 10:
            seconds_to_save = int(self.play_seconds)

            add_play_seconds(
                self.student_id,
                seconds_to_save,
            )

            self.saved_seconds += seconds_to_save
            self.play_seconds -= seconds_to_save

    def save_playtime(self):
        if self.student_id is None:
            return

        seconds_to_save = int(self.play_seconds)

        if seconds_to_save > 0:
            add_play_seconds(
                self.student_id,
                seconds_to_save,
            )

            self.saved_seconds += seconds_to_save

        self.play_seconds = 0

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(FPS) / 1000
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.update_playtime(dt)

            if self.fade_direction == 0:
                self.current_scene.handle_events(events)
                self.current_scene.update(dt)

            self.update_transition(dt)
            self.current_scene.draw(screen)
            self.draw_transition(screen)

            pygame.display.flip()

        self.save_playtime()


def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Scholar Seas")
    start_music()

    manager = SceneManager()
    manager.change_scene(StartScene(manager))
    manager.run()

    pygame.quit()


if __name__ == "__main__":
    main()
