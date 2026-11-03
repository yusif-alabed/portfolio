import pygame

from game.ui.outfit import load_outfit


class Player:

    def __init__(self, x, y, student_id=None):
        self.student_id = student_id

        if student_id is None:
            down_image = pygame.image.load(
                "game/assets/sprites/player_pirate.png"
            ).convert_alpha()
            down_image = pygame.transform.scale(
                down_image,
                (60, 90),
            )
            self.direction_images = {
                "down": down_image,
                "up": down_image,
                "left": pygame.transform.flip(
                    down_image, True, False
                ),
                "right": down_image,
            }
        else:
            self.direction_images = {}

            for direction in ["down", "up", "left", "right"]:
                self.direction_images[direction] = load_outfit(
                    student_id,
                    (90, 90),
                    direction,
                )

        self.direction = "down"
        self.image = self.direction_images[self.direction]
        self.is_walking = False
        self.walk_timer = 0
        self.walk_frame = 0
        self.draw_offset = 0

        self.rect = pygame.Rect(0, 0, 60, 90)
        self.rect.center = (x, y)

        self.speed = 220

    def update(self, dt, obstacles):
        keys = pygame.key.get_pressed()

        x_movement = 0
        y_movement = 0
        old_position = self.rect.center

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x_movement = -1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x_movement = 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y_movement = -1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y_movement = 1

        movement_speed = self.speed

        if x_movement != 0 and y_movement != 0:
            movement_speed *= 0.7

        old_x = self.rect.x

        self.rect.x += int(
            x_movement * movement_speed * dt
        )

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                self.rect.x = old_x

        old_y = self.rect.y

        self.rect.y += int(
            y_movement * movement_speed * dt
        )

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                self.rect.y = old_y

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, 1000)
        self.rect.top = max(self.rect.top, 90)
        self.rect.bottom = min(self.rect.bottom, 700)

        moved = self.rect.center != old_position
        self.update_animation(
            dt,
            x_movement,
            y_movement,
            moved,
        )

    def update_animation(
        self,
        dt,
        x_movement,
        y_movement,
        moved,
    ):
        if y_movement < 0:
            self.direction = "up"
        elif y_movement > 0:
            self.direction = "down"
        elif x_movement < 0:
            self.direction = "left"
        elif x_movement > 0:
            self.direction = "right"

        self.is_walking = moved and (
            x_movement != 0 or y_movement != 0
        )

        if self.is_walking:
            self.walk_timer += dt

            if self.walk_timer >= 0.14:
                self.walk_timer = 0
                self.walk_frame = 1 - self.walk_frame

            self.draw_offset = self.walk_frame * 2
        else:
            self.walk_timer = 0
            self.walk_frame = 0
            self.draw_offset = 0
            self.direction = "down"

        self.image = self.direction_images[self.direction]

    def set_image_size(self, size):
        centre = self.rect.center

        if self.student_id is not None:
            for direction in self.direction_images:
                self.direction_images[direction] = load_outfit(
                    self.student_id,
                    size,
                    direction,
                )
        else:
            for direction in self.direction_images:
                self.direction_images[direction] = (
                    pygame.transform.smoothscale(
                        self.direction_images[direction],
                        size,
                    )
                )

        self.image = self.direction_images[self.direction]
        self.rect = self.image.get_rect(center=centre)

    def draw_at(self, screen, centre):
        draw_centre = (
            centre[0],
            centre[1] + self.draw_offset,
        )
        image_rect = self.image.get_rect(center=draw_centre)
        screen.blit(self.image, image_rect)

    def draw(self, screen):
        self.draw_at(screen, self.rect.center)
