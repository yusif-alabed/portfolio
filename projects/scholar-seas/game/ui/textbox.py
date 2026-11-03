import pygame


class TextBox:

    def __init__(self, x, y, width, height, password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.password = password

        self.font = pygame.font.SysFont("arial", 24)

        self.normal_colour = (18, 48, 75)
        self.active_colour = (230, 180, 60)
        self.text_colour = (10, 25, 50)
        self.background_colour = (245, 230, 190)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < 20:
                self.text += event.unicode

    def draw(self, screen):
        shadow_rect = self.rect.move(4, 4)
        pygame.draw.rect(
            screen,
            (7, 20, 35),
            shadow_rect,
        )
        pygame.draw.rect(
            screen,
            self.background_colour,
            self.rect,
        )

        if self.active:
            border_colour = self.active_colour
        else:
            border_colour = self.normal_colour

        pygame.draw.rect(
            screen,
            border_colour,
            self.rect,
            width=4,
        )

        if self.password:
            displayed_text = "*" * len(self.text)
        else:
            displayed_text = self.text

        text_image = self.font.render(displayed_text, True, self.text_colour)
        screen.blit(text_image, (self.rect.x + 10, self.rect.y + 8))

        if self.active:
            cursor_x = self.rect.x + 12 + text_image.get_width()
            pygame.draw.line(
                screen,
                self.text_colour,
                (cursor_x, self.rect.y + 9),
                (cursor_x, self.rect.bottom - 9),
                width=2,
            )
