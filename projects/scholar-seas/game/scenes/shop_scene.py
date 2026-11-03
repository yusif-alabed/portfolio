import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button
from shared.database import (
    buy_item,
    equip_item,
    get_inventory,
    get_shop_items,
    get_student,
)

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
GREEN = (70, 210, 125)
RED = (235, 85, 85)


class ShopScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("shop.png")

        self.title_font = pygame.font.SysFont(
            "arial",
            42,
            bold=True,
        )
        self.text_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont(
            "arial",
            21,
            bold=True,
        )

        self.back_button = Button(
            350,
            625,
            300,
            45,
            "Return to Harbour",
        )

        self.message = "Choose an item to purchase."
        self.message_colour = CREAM

        self.items = []
        self.owned_item_ids = []
        self.equipped_names = []
        self.item_buttons = []
        self.coins = 0

        self.load_shop()

    def load_shop(self):
        self.items = get_shop_items()

        inventory = get_inventory(self.student_id)
        student = get_student(self.student_id)

        self.owned_item_ids = []

        for item in inventory:
            self.owned_item_ids.append(
                item["item_id"]
            )

        self.coins = student["coins"]

        self.equipped_names = [
            student["equipped_hat"],
            student["equipped_coat"],
            student["equipped_weapon"],
        ]

        self.item_buttons = []

        positions = [
            (75, 190),
            (525, 190),
            (75, 275),
            (525, 275),
            (75, 360),
            (525, 360),
            (300, 445),
        ]

        for number in range(len(self.items)):
            item = self.items[number]
            x, y = positions[number]

            label = (
                item["name"]
                + " - "
                + str(item["price"])
                + " coins"
            )

            if item["name"] in self.equipped_names:
                label += "  [Equipped]"
            elif item["item_id"] in self.owned_item_ids:
                label += "  [Owned]"

            button = Button(
                x,
                y,
                400,
                55,
                label,
            )
            button.font = pygame.font.SysFont(
                "arial",
                16,
                bold=True,
            )

            self.item_buttons.append(button)

    def handle_events(self, events):
        for event in events:
            for number in range(len(self.item_buttons)):
                button = self.item_buttons[number]

                if button.was_clicked(event):
                    item = self.items[number]

                    if item["item_id"] in self.owned_item_ids:
                        success, message = equip_item(
                            self.student_id,
                            item["item_id"],
                        )
                    else:
                        success, message = buy_item(
                            self.student_id,
                            item["item_id"],
                        )

                    self.message = message

                    if success:
                        self.message_colour = GREEN
                    else:
                        self.message_colour = RED

                    self.load_shop()

            if self.back_button.was_clicked(event):
                from game.scenes.harbour_scene import HarbourScene

                self.manager.change_scene(
                    HarbourScene(
                        self.manager,
                        self.username,
                        self.student_id,
                        start_position="shop",
                    )
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title = self.title_font.render(
            "The Gilded Anchor",
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 55)
        )
        title_shadow = self.title_font.render(
            "The Gilded Anchor",
            True,
            (0, 0, 0),
        )
        screen.blit(title_shadow, title_rect.move(3, 3))
        screen.blit(title, title_rect)

        description = self.text_font.render(
            "Spend battle rewards on pirate equipment.",
            True,
            CREAM,
        )
        description_rect = description.get_rect(
            center=(WIDTH // 2, 105)
        )
        screen.blit(description, description_rect)

        coins_text = self.text_font.render(
            "Your coins: " + str(self.coins),
            True,
            GOLD,
        )
        coins_rect = coins_text.get_rect(
            center=(WIDTH // 2, 145)
        )
        screen.blit(coins_text, coins_rect)

        for button in self.item_buttons:
            button.draw(screen)

        message_panel = pygame.Rect(210, 530, 580, 55)
        pygame.draw.rect(
            screen,
            NAVY,
            message_panel,
        )
        pygame.draw.rect(
            screen,
            GOLD,
            message_panel,
            width=4,
        )

        message_image = self.small_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message_image.get_rect(
            center=message_panel.center
        )
        message_shadow = self.small_font.render(
            self.message,
            True,
            (0, 0, 0),
        )
        screen.blit(message_shadow, message_rect.move(2, 2))
        screen.blit(message_image, message_rect)

        self.back_button.draw(screen)
