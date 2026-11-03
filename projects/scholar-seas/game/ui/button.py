import pygame


class Button:

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.font = pygame.font.SysFont("arial", 24, bold=True)

        self.normal_colour = (18, 48, 75)
        self.hover_colour = (28, 92, 112)
        self.text_colour = (245, 230, 190)
        self.border_colour = (230, 180, 60)
        self.shadow_colour = (7, 20, 35)

    def was_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True

        return False

    def draw(self, screen):
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            colour = self.hover_colour
        else:
            colour = self.normal_colour

        shadow_rect = self.rect.move(5, 5)

        pygame.draw.rect(
            screen,
            self.shadow_colour,
            shadow_rect,
        )
        pygame.draw.rect(
            screen,
            colour,
            self.rect,
        )
        pygame.draw.rect(
            screen,
            self.border_colour,
            self.rect,
            width=4,
        )

        corner_size = 6
        for corner in [
            self.rect.topleft,
            (self.rect.right - corner_size, self.rect.top),
            (self.rect.left, self.rect.bottom - corner_size),
            (
                self.rect.right - corner_size,
                self.rect.bottom - corner_size,
            ),
        ]:
            pygame.draw.rect(
                screen,
                self.text_colour,
                (
                    corner[0],
                    corner[1],
                    corner_size,
                    corner_size,
                ),
            )

        text_image = self.font.render(self.text, True, self.text_colour)
        text_rect = text_image.get_rect(center=self.rect.center)

        screen.blit(text_image, text_rect)
