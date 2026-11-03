import pygame

from game.entities.npc import NPC
from game.entities.player import Player
from game.scenes.base_scene import Scene
from game.ui.art import load_background
from shared.database import get_story_chapter

WIDTH = 1000
HEIGHT = 700

SKY = (100, 185, 220)
SAND = (220, 190, 120)
WATER = (35, 125, 175)
WOOD = (130, 85, 45)
DARK_WOOD = (85, 50, 30)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
GREEN = (65, 145, 75)


class HarbourScene(Scene):

    def __init__(
        self,
        manager,
        username,
        student_id,
        start_position=None,
    ):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("harbour.png")

        if start_position == "shop":
            player_x = 165
            player_y = 300
        else:
            player_x = 500
            player_y = 390

        self.player = Player(
            player_x,
            player_y,
            self.student_id,
        )
        self.captain_coral = NPC(
            755,
            315,
            "Captain Coral",
        )
        self.shop_entrance = pygame.Rect(
            120,
            250,
            90,
            75,
        )

        self.ship_area = pygame.Rect(410, 540, 180, 120)
        self.message = ""
        self.message_timer = 0

        self.obstacles = [
            pygame.Rect(70, 0, 275, 245),
            pygame.Rect(0, 35, 70, 200),
            pygame.Rect(315, 105, 65, 155),

            pygame.Rect(650, 20, 250, 275),
            pygame.Rect(590, 95, 70, 170),
            pygame.Rect(890, 80, 110, 195),

            pygame.Rect(0, 325, 130, 155),
            pygame.Rect(825, 330, 175, 165),

            pygame.Rect(0, 500, 410, 200),
            pygame.Rect(590, 500, 410, 200),
        ]

        self.title_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True,
        )
        self.text_font = pygame.font.SysFont(
            "arial",
            18,
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from game.scenes.menu_scene import MenuScene

                    self.manager.change_scene(
                        MenuScene(
                            self.manager,
                            self.username,
                            self.student_id,
                        )
                    )

                if event.key == pygame.K_e:
                    if self.captain_coral.is_near(
                        self.player.rect
                    ):
                        chapter = get_story_chapter(
                            self.student_id
                        )

                        if chapter == 1:
                            if self.manager.active_mission == (
                                "chapter_1_battle"
                            ):
                                new_scene = None
                                self.show_message(
                                    "Captain Coral: Your ship is "
                                    "waiting at the pier!"
                                )
                            else:
                                from game.scenes.story_scene import StoryScene

                                new_scene = StoryScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )

                        elif chapter == 2:
                            from game.scenes.chapter_two_story_scene import (
                                ChapterTwoStoryScene,
                            )

                            new_scene = ChapterTwoStoryScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )

                        elif chapter == 3:
                            if self.manager.active_mission == (
                                "chapter_3_boss"
                            ):
                                from game.scenes.skull_reef_scene import SkullReefScene

                                new_scene = SkullReefScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )
                            else:
                                from game.scenes.chapter_three_story_scene import (
                                    ChapterThreeStoryScene,
                                )

                                new_scene = ChapterThreeStoryScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )

                        else:
                            new_scene = None
                            self.show_message(
                                "Captain Coral: The Astrolabe is restored. "
                                "Scholar Seas is safe!"
                            )

                        if new_scene is not None:
                            self.manager.change_scene(
                                new_scene
                            )

                    if self.shop_entrance.colliderect(
                        self.player.rect
                    ):
                        from game.scenes.shop_scene import ShopScene

                        self.manager.change_scene(
                            ShopScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )
                        )

                    if self.ship_area.colliderect(
                        self.player.rect
                    ):
                        chapter = get_story_chapter(
                            self.student_id
                        )

                        if (
                            chapter == 1
                            and self.manager.active_mission
                            == "chapter_1_battle"
                        ):
                            from game.scenes.battle_scene import BattleScene

                            self.manager.change_scene(
                                BattleScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                )
                            )
                        else:
                            from game.scenes.battle_scene import BattleScene

                            self.manager.change_scene(
                                BattleScene(
                                    self.manager,
                                    self.username,
                                    self.student_id,
                                    free_play=True,
                                )
                            )

    def show_message(self, text):
        self.message = text
        self.message_timer = 4

    def update(self, dt):
        self.player.update(
            dt,
            self.obstacles,
        )

        if self.message_timer > 0:
            self.message_timer -= dt

            if self.message_timer <= 0:
                self.message = ""

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw(self, screen):
        self.draw_background(screen)
        self.captain_coral.draw(screen)
        self.player.draw(screen)

        title = self.title_font.render(
            "Scholar Seas Harbour",
            True,
            GOLD,
        )
        title_shadow = self.title_font.render(
            "Scholar Seas Harbour",
            True,
            (0, 0, 0),
        )
        screen.blit(title_shadow, (27, 27))
        screen.blit(title, (25, 25))

        instructions = self.text_font.render(
            "Move: WASD or arrow keys | ESC: Return to menu",
            True,
            CREAM,
        )
        instructions_rect = instructions.get_rect(
            topright=(975, 34)
        )
        instruction_shadow = self.text_font.render(
            "Move: WASD or arrow keys | ESC: Return to menu",
            True,
            (0, 0, 0),
        )
        shadow_rect = instruction_shadow.get_rect(
            topright=(977, 36)
        )
        screen.blit(instruction_shadow, shadow_rect)
        screen.blit(instructions, instructions_rect)

        if self.message != "":
            message_panel = pygame.Rect(215, 550, 570, 42)
            pygame.draw.rect(
                screen,
                (10, 25, 50),
                message_panel,
            )
            pygame.draw.rect(
                screen,
                GOLD,
                message_panel,
                width=3,
            )
            message_image = self.text_font.render(
                self.message,
                True,
                CREAM,
            )
            message_rect = message_image.get_rect(
                center=message_panel.center
            )
            screen.blit(message_image, message_rect)

        if self.captain_coral.is_near(
            self.player.rect
        ):
            prompt_panel = pygame.Rect(300, 620, 400, 42)
            pygame.draw.rect(screen, (10, 25, 50), prompt_panel)
            pygame.draw.rect(screen, GOLD, prompt_panel, width=3)
            prompt = self.text_font.render(
                "Press E to speak to Captain Coral",
                True,
                CREAM,
            )
            prompt_rect = prompt.get_rect(
                center=prompt_panel.center
            )
            screen.blit(prompt, prompt_rect)

        if self.shop_entrance.colliderect(
            self.player.rect
        ):
            prompt_panel = pygame.Rect(300, 620, 400, 42)
            pygame.draw.rect(screen, (10, 25, 50), prompt_panel)
            pygame.draw.rect(screen, GOLD, prompt_panel, width=3)
            shop_prompt = self.text_font.render(
                "Press E to enter the Pirate Shop",
                True,
                CREAM,
            )
            shop_prompt_rect = shop_prompt.get_rect(
                center=prompt_panel.center
            )
            screen.blit(
                shop_prompt,
                shop_prompt_rect,
            )

        if self.ship_area.colliderect(
            self.player.rect
        ):
            prompt_panel = pygame.Rect(300, 620, 400, 42)
            pygame.draw.rect(screen, (10, 25, 50), prompt_panel)
            pygame.draw.rect(screen, GOLD, prompt_panel, width=3)
            ship_prompt = self.text_font.render(
                "Press E to start a free training battle",
                True,
                CREAM,
            )
            ship_prompt_rect = ship_prompt.get_rect(
                center=prompt_panel.center
            )
            screen.blit(
                ship_prompt,
                ship_prompt_rect,
            )
