import pygame

from game.entities.player import Player
from game.entities.reef_guard import ReefGuard
from game.scenes.base_scene import Scene
from game.ui.art import load_background

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BLUE = (45, 155, 220)
GREEN = (45, 180, 90)
DARK_GREEN = (15, 85, 50)
LIGHT_GREEN = (145, 245, 155)


class SkullReefScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id

        original_background = load_background("skull_reef.png")
        self.world_width = 2400
        self.world_height = 1680
        self.background = pygame.transform.scale(
            original_background,
            (self.world_width, self.world_height),
        )

        self.player = Player(1200, 1480, self.student_id)
        self.player.set_image_size((86, 86))
        player_centre = self.player.rect.center
        self.player.rect = pygame.Rect(0, 0, 42, 68)
        self.player.rect.center = player_centre
        self.camera_x = 0
        self.camera_y = 0

        self.guards = [
            ReefGuard(1470, 1670, 600),
            ReefGuard(390, 550, 700),
            ReefGuard(1730, 1930, 900),
            ReefGuard(770, 1010, 1100),
        ]
        self.caught_cooldown = 0

        self.title_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 18)

        self.fortress_area = pygame.Rect(1090, 390, 220, 170)

        gem_positions = [
            (900, 1330),
            (390, 1040),
            (530, 640),
            (1850, 860),
            (1650, 1140),
        ]
        self.gems = []

        for position in gem_positions:
            gem = pygame.Rect(0, 0, 30, 30)
            gem.center = position
            self.gems.append(gem)

        self.total_gems = len(self.gems)
        self.gems_collected = 0
        self.message = "Find every Number Gem to unlock the fortress."
        self.message_timer = 4

        self.dialogue = [
            (
                self.username,
                "Blackreef! Your maze could not stop me.",
            ),
            (
                "Captain Blackreef",
                "So, the young navigator finally reaches my fortress.",
            ),
            (
                "Captain Blackreef",
                "The Astrolabe is mine. Defeat me if you want it back!",
            ),
            (
                self.username,
                "Then prepare yourself. Scholar Seas will be free again!",
            ),
        ]
        self.dialogue_active = False
        self.dialogue_page = 0

        self.blackreef_image = pygame.image.load(
            "game/assets/sprites/captain_blackreef.png"
        ).convert_alpha()
        self.blackreef_image = pygame.transform.scale(
            self.blackreef_image,
            (150, 225),
        )

        self.hero_image = pygame.transform.scale(
            self.player.direction_images["down"],
            (190, 190),
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.dialogue_active:
                        self.dialogue_active = False
                        return

                    from game.scenes.harbour_scene import HarbourScene

                    self.manager.change_scene(
                        HarbourScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

                if event.key == pygame.K_e:
                    if self.dialogue_active:
                        self.dialogue_page += 1

                        if self.dialogue_page >= len(self.dialogue):
                            self.dialogue_page = len(self.dialogue) - 1
                            self.start_final_battle()

                        return

                    if self.fortress_area.colliderect(self.player.rect):
                        if self.gems_collected == self.total_gems:
                            self.dialogue_active = True
                            self.dialogue_page = 0
                        else:
                            gems_left = (
                                self.total_gems - self.gems_collected
                            )
                            self.show_message(
                                "The fortress is locked! Find "
                                + str(gems_left)
                                + " more Number Gems."
                            )

    def start_final_battle(self):
        from game.scenes.final_battle_scene import FinalBattleScene

        self.manager.change_scene(
            FinalBattleScene(
                self.manager,
                self.username,
                self.student_id,
            )
        )

    def show_message(self, text):
        self.message = text
        self.message_timer = 4

    def collect_gems(self):
        for gem in self.gems[:]:
            if self.player.rect.colliderect(gem):
                self.gems.remove(gem)
                self.gems_collected += 1

                if self.gems_collected == self.total_gems:
                    self.show_message(
                        "All Number Gems found! Enter the fortress."
                    )
                else:
                    self.show_message(
                        "Number Gem collected! "
                        + str(self.gems_collected)
                        + " / "
                        + str(self.total_gems)
                    )

    def check_guard_collisions(self):
        if self.caught_cooldown > 0:
            return

        for guard in self.guards:
            if self.player.rect.colliderect(guard.rect):
                from game.scenes.guard_battle_scene import GuardBattleScene

                self.caught_cooldown = 1
                self.manager.change_scene(
                    GuardBattleScene(
                        self.manager,
                        self.username,
                        self.student_id,
                        self,
                        guard,
                    )
                )
                return

    def move_player(self, dt):
        keys = pygame.key.get_pressed()
        x_movement = 0
        y_movement = 0
        old_position = self.player.rect.center

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x_movement = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x_movement = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y_movement = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y_movement = 1

        movement_speed = self.player.speed

        if x_movement != 0 and y_movement != 0:
            movement_speed *= 0.7

        old_x = self.player.rect.x
        self.player.rect.x += int(
            x_movement * movement_speed * dt
        )
        if not self.can_stand_here(self.player.rect):
            self.player.rect.x = old_x

        old_y = self.player.rect.y
        self.player.rect.y += int(
            y_movement * movement_speed * dt
        )
        if not self.can_stand_here(self.player.rect):
            self.player.rect.y = old_y

        self.player.rect.clamp_ip(
            pygame.Rect(0, 0, self.world_width, self.world_height)
        )

        moved = self.player.rect.center != old_position
        self.player.update_animation(
            dt,
            x_movement,
            y_movement,
            moved,
        )

    def can_stand_here(self, player_rect):
        foot_y = player_rect.bottom - 5
        foot_points = [
            (player_rect.left + 12, foot_y),
            (player_rect.centerx, foot_y),
            (player_rect.right - 12, foot_y),
        ]

        for point in foot_points:
            if not (0 <= point[0] < self.world_width):
                return False
            if not (0 <= point[1] < self.world_height):
                return False

            red, green, blue = self.background.get_at(point)[:3]

            on_sand = (
                red > 145
                and green > 105
                and blue < 165
                and red > green
                and green > blue
            )

            on_dock = (
                1020 < point[0] < 1380
                and point[1] > 1240
            )

            if not on_sand and not on_dock:
                return False

        return True

    def update_camera(self):
        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_y = self.player.rect.centery - HEIGHT // 2

        self.camera_x = max(
            0,
            min(self.camera_x, self.world_width - WIDTH),
        )
        self.camera_y = max(
            0,
            min(self.camera_y, self.world_height - HEIGHT),
        )

    def update(self, dt):
        if not self.dialogue_active:
            for guard in self.guards:
                guard.update(dt)

            self.move_player(dt)
            self.collect_gems()
            self.check_guard_collisions()

        if self.caught_cooldown > 0:
            self.caught_cooldown -= dt

        self.update_camera()

        if self.message_timer > 0:
            self.message_timer -= dt

            if self.message_timer <= 0:
                self.message = ""

    def draw_gem(self, screen, gem):
        x = gem.centerx - self.camera_x
        y = gem.centery - self.camera_y

        shadow = pygame.Rect(x - 13, y + 13, 26, 5)
        pygame.draw.rect(screen, DARK_GREEN, shadow)

        outline = [
            (x, y - 17),
            (x + 15, y - 5),
            (x + 15, y + 6),
            (x, y + 18),
            (x - 15, y + 6),
            (x - 15, y - 5),
        ]
        pygame.draw.polygon(screen, DARK_GREEN, outline)

        gem_points = [
            (x, y - 13),
            (x + 11, y - 3),
            (x + 11, y + 4),
            (x, y + 14),
            (x - 11, y + 4),
            (x - 11, y - 3),
        ]
        pygame.draw.polygon(screen, GREEN, gem_points)
        pygame.draw.polygon(
            screen,
            LIGHT_GREEN,
            [(x, y - 10), (x - 7, y - 2), (x, y + 9)],
        )
        pygame.draw.rect(screen, CREAM, (x - 4, y - 8, 4, 4))

    def draw_dialogue(self, screen):
        speaker, words = self.dialogue[self.dialogue_page]

        dark_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_layer.fill((0, 0, 0, 145))
        screen.blit(dark_layer, (0, 0))

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 95))
        pygame.draw.rect(screen, (0, 0, 0), (0, 610, WIDTH, 90))

        hero_rect = self.hero_image.get_rect(midbottom=(180, 490))
        boss_rect = self.blackreef_image.get_rect(midbottom=(820, 490))
        screen.blit(self.hero_image, hero_rect)
        screen.blit(self.blackreef_image, boss_rect)

        versus = self.title_font.render("VS", True, GOLD)
        versus_rect = versus.get_rect(center=(WIDTH // 2, 345))
        screen.blit(versus, versus_rect)

        panel = pygame.Rect(85, 475, 830, 150)
        pygame.draw.rect(screen, NAVY, panel)
        pygame.draw.rect(screen, GOLD, panel, width=5)

        speaker_image = self.title_font.render(speaker, True, GOLD)
        words_image = self.text_font.render(words, True, CREAM)
        continue_image = self.text_font.render(
            "Press E to continue",
            True,
            LIGHT_GREEN,
        )

        screen.blit(speaker_image, (115, 495))
        screen.blit(words_image, (115, 540))
        continue_rect = continue_image.get_rect(bottomright=(890, 605))
        screen.blit(continue_image, continue_rect)

    def draw(self, screen):
        screen.blit(
            self.background,
            (-self.camera_x, -self.camera_y),
        )

        for gem in self.gems:
            self.draw_gem(screen, gem)

        for guard in self.guards:
            guard.draw(screen, self.camera_x, self.camera_y)

        player_centre = (
            self.player.rect.centerx - self.camera_x,
            self.player.rect.centery - self.camera_y,
        )
        self.player.draw_at(screen, player_centre)

        heading_panel = pygame.Rect(20, 18, 960, 65)
        pygame.draw.rect(screen, NAVY, heading_panel)
        pygame.draw.rect(screen, GOLD, heading_panel, width=4)

        title = self.title_font.render(
            "Skull Reef Maze",
            True,
            GOLD,
        )
        screen.blit(title, (40, 34))

        gem_counter = self.text_font.render(
            "Number Gems: "
            + str(self.gems_collected)
            + " / "
            + str(self.total_gems),
            True,
            GOLD,
        )
        screen.blit(gem_counter, (300, 39))

        instructions = self.text_font.render(
            "Find gems, avoid guards | Move: WASD/arrows | ESC: Harbour",
            True,
            CREAM,
        )
        instruction_rect = instructions.get_rect(
            topright=(960, 41)
        )
        screen.blit(instructions, instruction_rect)

        if self.fortress_area.colliderect(self.player.rect):
            prompt_panel = pygame.Rect(300, 620, 400, 42)
            pygame.draw.rect(screen, NAVY, prompt_panel)
            pygame.draw.rect(screen, GOLD, prompt_panel, width=3)

            if self.gems_collected == self.total_gems:
                prompt_text = "Press E to enter Blackreef's fortress"
            else:
                prompt_text = "Find every Number Gem to unlock this gate"

            prompt = self.text_font.render(prompt_text, True, CREAM)
            prompt_rect = prompt.get_rect(center=prompt_panel.center)
            screen.blit(prompt, prompt_rect)

        elif self.message != "":
            message_panel = pygame.Rect(230, 620, 540, 42)
            pygame.draw.rect(screen, NAVY, message_panel)
            pygame.draw.rect(screen, GOLD, message_panel, width=3)
            message_image = self.text_font.render(
                self.message,
                True,
                CREAM,
            )
            message_rect = message_image.get_rect(
                center=message_panel.center
            )
            screen.blit(message_image, message_rect)

        if self.dialogue_active:
            self.draw_dialogue(screen)
