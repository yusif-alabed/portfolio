import pygame

from game.scenes.base_scene import Scene
from game.ui.art import load_background
from game.ui.button import Button
from game.ui.outfit import load_outfit
from shared.database import (
    equip_item,
    get_inventory,
    get_student,
    unequip_item,
)

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)
RED = (170, 45, 45)
BLUE = (35, 85, 145)
BLACK = (25, 25, 30)


class CharacterScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)
        self.username = username
        self.student_id = student_id
        self.background = load_background("ui.png")

        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("arial", 17)

        self.hat_button = Button(575, 235, 300, 58, "Hat")
        self.coat_button = Button(575, 330, 300, 58, "Coat")
        self.weapon_button = Button(575, 425, 300, 58, "Weapon")

        for button in [self.hat_button, self.coat_button, self.weapon_button]:
            button.font = pygame.font.SysFont("arial", 16, bold=True)

        self.back_button = Button(600, 590, 260, 50, "Return to Menu")
        self.message = "Click a slot to change your equipped item."
        self.load_character()

    def load_character(self):
        self.student = get_student(self.student_id)
        self.inventory = get_inventory(self.student_id)

        self.hat_button.text = self.slot_text(
            "Hat", self.student["equipped_hat"]
        )
        self.coat_button.text = self.slot_text(
            "Coat", self.student["equipped_coat"]
        )
        self.weapon_button.text = self.slot_text(
            "Weapon", self.student["equipped_weapon"]
        )
        self.character_image = load_outfit(
            self.student_id,
            (300, 300),
        )

    def slot_text(self, slot_name, item_name):
        if item_name is None:
            item_name = "Nothing equipped"
        return slot_name + ": " + item_name

    def change_equipment(self, slot):
        choices = [None]

        for item in self.inventory:
            if item["slot"] == slot:
                choices.append(item)

        if len(choices) == 1:
            self.message = "You do not own any " + slot + " items yet."
            return

        current_name = self.student["equipped_" + slot]
        next_number = 0

        for number in range(len(choices)):
            choice = choices[number]
            choice_name = None if choice is None else choice["name"]
            if choice_name == current_name:
                next_number = (number + 1) % len(choices)
                break

        next_item = choices[next_number]

        if next_item is None:
            success, self.message = unequip_item(self.student_id, slot)
        else:
            success, self.message = equip_item(
                self.student_id,
                next_item["item_id"],
            )

        if success:
            self.load_character()

    def handle_events(self, events):
        for event in events:
            if self.hat_button.was_clicked(event):
                self.change_equipment("hat")
            if self.coat_button.was_clicked(event):
                self.change_equipment("coat")
            if self.weapon_button.was_clicked(event):
                self.change_equipment("weapon")

            if self.back_button.was_clicked(event):
                from game.scenes.menu_scene import MenuScene

                self.manager.change_scene(
                    MenuScene(self.manager, self.username, self.student_id)
                )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_panel = pygame.Rect(250, 15, 500, 80)
        pygame.draw.rect(screen, NAVY, title_panel)
        pygame.draw.rect(screen, GOLD, title_panel, width=5)

        title = self.title_font.render(
            self.username + "'s Pirate", True, GOLD
        )
        screen.blit(title, title.get_rect(center=title_panel.center))

        character_panel = pygame.Rect(100, 130, 400, 460)
        equipment_panel = pygame.Rect(550, 130, 350, 400)
        pygame.draw.rect(screen, CREAM, character_panel, border_radius=15)
        pygame.draw.rect(
            screen, GOLD, character_panel, width=5, border_radius=15
        )
        pygame.draw.rect(screen, BROWN, equipment_panel, border_radius=15)
        pygame.draw.rect(
            screen, GOLD, equipment_panel, width=5, border_radius=15
        )

        character_rect = self.character_image.get_rect(
            center=character_panel.center
        )
        screen.blit(self.character_image, character_rect)

        equipment_title = self.title_font.render("Equipment", True, GOLD)
        equipment_title = pygame.transform.scale(
            equipment_title,
            (equipment_title.get_width() * 3 // 4,
             equipment_title.get_height() * 3 // 4),
        )
        screen.blit(
            equipment_title,
            equipment_title.get_rect(center=(725, 175)),
        )

        self.hat_button.draw(screen)
        self.coat_button.draw(screen)
        self.weapon_button.draw(screen)

        message = self.small_font.render(self.message, True, CREAM)
        screen.blit(message, message.get_rect(center=(725, 505)))
        self.back_button.draw(screen)
