import sqlite3

import pygame
from werkzeug.security import check_password_hash, generate_password_hash

from game.scenes.base_scene import Scene
from game.scenes.menu_scene import MenuScene
from game.ui.art import load_background
from game.ui.button import Button
from game.ui.textbox import TextBox
from shared.database import (
    create_student,
    create_user,
    get_student_by_user,
    get_user_by_username,
)

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
BROWN = (90, 55, 30)
RED = (235, 85, 85)
GREEN = (70, 210, 125)


class LoginScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)

        self.background = load_background("ui.png")

        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("arial", 25)
        self.message_font = pygame.font.SysFont(
            "arial",
            19,
            bold=True,
        )

        self.username_box = TextBox(330, 285, 340, 45)
        self.password_box = TextBox(330, 385, 340, 45, password=True)
        self.login_button = Button(300, 475, 185, 50, "Log in")
        self.register_button = Button(515, 475, 185, 50, "Register")
        self.forgot_button = Button(
            350,
            535,
            300,
            42,
            "Forgot password?",
        )

        self.message = ""
        self.message_colour = RED

    def handle_events(self, events):
        for event in events:
            self.username_box.handle_event(event)
            self.password_box.handle_event(event)

            if self.login_button.was_clicked(event):
                self.try_login()
            if self.register_button.was_clicked(event):
                self.try_register()
            if self.forgot_button.was_clicked(event):
                self.message = (
                    "Ask your linked parent to reset it online."
                )
                self.message_colour = GOLD

    def try_login(self):
        username = self.username_box.text.strip()
        password = self.password_box.text

        if username == "":
            self.message = "Please enter your username."
            self.message_colour = RED
            return

        if password == "":
            self.message = "Please enter your password."
            self.message_colour = RED
            return

        user = get_user_by_username(username)

        if user is None:
            self.message = "That account does not exist."
            self.message_colour = RED
        elif not check_password_hash(user["password_hash"], password):
            self.message = "The password is incorrect."
            self.message_colour = RED
        else:
            student = get_student_by_user(user["user_id"])
            self.manager.start_tracking(student["student_id"])

            self.manager.change_scene(
                MenuScene(
                    self.manager,
                    username,
                    student["student_id"],
                )
            )

    def try_register(self):
        username = self.username_box.text.strip()
        password = self.password_box.text

        if len(username) < 3:
            self.message = "Username must contain at least 3 characters."
            self.message_colour = RED
            return

        if len(password) < 6:
            self.message = "Password must contain at least 6 characters."
            self.message_colour = RED
            return

        try:
            password_hash = generate_password_hash(
                password,
                method="pbkdf2:sha256",
            )
            user_id = create_user(username, password_hash, "student")
            create_student(user_id, username, 7)

            self.message = "Account created! You can now log in."
            self.message_colour = GREEN
            self.password_box.text = ""

        except sqlite3.IntegrityError:
            self.message = "That username is already being used."
            self.message_colour = RED

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        panel = pygame.Rect(250, 80, 500, 540)
        pygame.draw.rect(screen, CREAM, panel, border_radius=15)
        pygame.draw.rect(screen, GOLD, panel, width=5, border_radius=15)

        title = self.title_font.render("Captain Login", True, BROWN)
        username_label = self.text_font.render("Username", True, BROWN)
        password_label = self.text_font.render("Password", True, BROWN)

        title_rect = title.get_rect(center=(WIDTH // 2, 145))

        screen.blit(title, title_rect)
        screen.blit(username_label, (330, 250))
        screen.blit(password_label, (330, 350))

        self.username_box.draw(screen)
        self.password_box.draw(screen)
        self.login_button.draw(screen)
        self.register_button.draw(screen)
        self.forgot_button.draw(screen)

        if self.message != "":
            message_panel = pygame.Rect(290, 585, 420, 30)
            pygame.draw.rect(screen, NAVY, message_panel)
            pygame.draw.rect(screen, GOLD, message_panel, width=3)
            message_image = self.message_font.render(
                self.message,
                True,
                self.message_colour,
            )
            message_rect = message_image.get_rect(
                center=message_panel.center
            )
            screen.blit(message_image, message_rect)
