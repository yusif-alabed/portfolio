import pygame


class ReefGuard:

    def __init__(self, start_x, end_x, y):
        image = pygame.image.load(
            "game/assets/sprites/reef_guard.png"
        ).convert_alpha()
        self.right_image = pygame.transform.scale(image, (55, 82))
        self.left_image = pygame.transform.flip(
            self.right_image,
            True,
            False,
        )

        self.start_x = start_x
        self.end_x = end_x
        self.x = float(start_x)
        self.y = y
        self.speed = 75
        self.direction = 1

        self.rect = pygame.Rect(0, 0, 38, 55)
        self.rect.midbottom = (start_x, y + 30)

    def update(self, dt):
        self.x += self.speed * self.direction * dt

        if self.x >= self.end_x:
            self.x = self.end_x
            self.direction = -1
        elif self.x <= self.start_x:
            self.x = self.start_x
            self.direction = 1

        self.rect.midbottom = (int(self.x), self.y + 30)

    def draw(self, screen, camera_x, camera_y):
        if self.direction == 1:
            image = self.right_image
        else:
            image = self.left_image

        screen_x = self.rect.centerx - camera_x
        screen_y = self.rect.bottom - camera_y

        shadow = pygame.Rect(0, 0, 42, 12)
        shadow.center = (screen_x, screen_y - 3)
        pygame.draw.ellipse(screen, (20, 25, 30), shadow)

        image_rect = image.get_rect(midbottom=(screen_x, screen_y))
        screen.blit(image, image_rect)
