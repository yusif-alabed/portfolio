import pygame

from game.scenes.base_scene import Scene
from game.systems.audio import play_sound
from game.systems.pathfinding import find_shortest_path
from game.ui.art import load_background
from game.ui.button import Button

WIDTH = 1000
HEIGHT = 700

NAVY = (10, 25, 50)
CREAM = (245, 230, 190)
GOLD = (230, 180, 60)
GREEN = (45, 180, 95)
GREY = (120, 130, 140)
RED = (235, 85, 85)


class PuzzleScene(Scene):

    def __init__(self, manager, username, student_id):
        super().__init__(manager)

        self.username = username
        self.student_id = student_id
        self.background = load_background("navigator_trial.png")

        self.island_images = {}
        island_names = [
            "Port",
            "Coral",
            "Fog",
            "Turtle",
            "Skull",
            "Volcano",
            "Treasure",
        ]

        for island in island_names:
            image = pygame.image.load(
                "game/assets/sprites/route_markers/"
                + island.lower()
                + ".png"
            ).convert_alpha()

            visible_area = image.get_bounding_rect()
            image = image.subsurface(visible_area).copy()

            width, height = image.get_size()
            scale = 70 / max(width, height)
            new_size = (
                int(width * scale),
                int(height * scale),
            )
            self.island_images[island] = (
                pygame.transform.smoothscale(image, new_size)
            )

        self.title_font = pygame.font.SysFont(
            "arial",
            36,
            bold=True,
        )
        self.small_font = pygame.font.SysFont(
            "arial",
            18,
        )

        self.island_positions = {
            "Port": (110, 340),
            "Coral": (300, 190),
            "Fog": (300, 500),
            "Turtle": (520, 145),
            "Skull": (520, 350),
            "Volcano": (520, 510),
            "Treasure": (820, 340),
        }

        self.puzzle_costs = [
            [3, 6, 2, 4, 2, 7, 6, 3, 2],
            [5, 2, 6, 7, 2, 4, 3, 6, 3],
            [2, 7, 2, 8, 3, 5, 2, 5, 3],
            [6, 2, 5, 7, 2, 6, 4, 3, 5],
        ]
        self.puzzle_number = 0
        self.graph = self.make_graph(
            self.puzzle_costs[self.puzzle_number]
        )

        self.route = ["Port"]
        self.distance = 0
        self.puzzle_complete = False

        self.safest_route, self.safest_distance = (
            find_shortest_path(
                self.graph,
                "Port",
                "Treasure",
            )
        )

        self.reset_button = Button(
            80,
            625,
            240,
            50,
            "Reset Route",
        )
        self.check_button = Button(
            380,
            625,
            240,
            50,
            "Check My Route",
        )
        self.back_button = Button(
            680,
            625,
            240,
            50,
            "Return to Port",
        )

        self.message = (
            "Start at Port and click a connected island."
        )
        self.message_colour = CREAM

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.check_island_click(event.pos)

            if self.reset_button.was_clicked(event):
                if not self.puzzle_complete:
                    self.reset_route()

            if self.check_button.was_clicked(event):
                if self.puzzle_complete:
                    if self.puzzle_number < len(self.puzzle_costs) - 1:
                        self.next_puzzle()
                    else:
                        from game.scenes.chapter_two_storm_scene import (
                            ChapterTwoStormScene,
                        )

                        self.manager.change_scene(
                            ChapterTwoStormScene(
                                self.manager,
                                self.username,
                                self.student_id,
                            )
                        )
                else:
                    self.check_route()

            if self.back_button.was_clicked(event):
                from game.scenes.menu_scene import MenuScene

                self.manager.change_scene(
                    MenuScene(
                        self.manager,
                        self.username,
                        self.student_id,
                    )
                )

    def make_graph(self, costs):
        return {
            "Port": [("Coral", costs[0]), ("Fog", costs[1])],
            "Coral": [
                ("Port", costs[0]),
                ("Turtle", costs[2]),
                ("Skull", costs[3]),
            ],
            "Fog": [
                ("Port", costs[1]),
                ("Skull", costs[4]),
                ("Volcano", costs[5]),
            ],
            "Turtle": [
                ("Coral", costs[2]),
                ("Treasure", costs[6]),
            ],
            "Skull": [
                ("Coral", costs[3]),
                ("Fog", costs[4]),
                ("Treasure", costs[7]),
            ],
            "Volcano": [
                ("Fog", costs[5]),
                ("Treasure", costs[8]),
            ],
            "Treasure": [
                ("Turtle", costs[6]),
                ("Skull", costs[7]),
                ("Volcano", costs[8]),
            ],
        }

    def next_puzzle(self):
        self.puzzle_number += 1
        self.graph = self.make_graph(
            self.puzzle_costs[self.puzzle_number]
        )
        self.safest_route, self.safest_distance = (
            find_shortest_path(
                self.graph,
                "Port",
                "Treasure",
            )
        )
        self.route = ["Port"]
        self.distance = 0
        self.puzzle_complete = False
        self.check_button.text = "Check My Route"
        self.message = "New chart loaded. Find the safest route."
        self.message_colour = CREAM

    def check_island_click(self, mouse_position):
        for island, position in self.island_positions.items():
            x_distance = mouse_position[0] - position[0]
            y_distance = mouse_position[1] - position[1]

            distance_from_centre = (
                x_distance ** 2
                + y_distance ** 2
            )

            if distance_from_centre <= 42 ** 2:
                self.choose_island(island)
                return

    def choose_island(self, island):
        current_island = self.route[-1]

        if island == current_island:
            return

        if island in self.route:
            self.message = (
                "You have already visited that island."
            )
            self.message_colour = RED
            return

        travel_cost = self.get_travel_cost(
            current_island,
            island,
        )

        if travel_cost is None:
            self.message = (
                "That island is not connected to "
                + current_island
                + "."
            )
            self.message_colour = RED
            return

        self.route.append(island)
        self.distance += travel_cost

        self.message = (
            "Route danger: "
            + str(self.distance)
        )
        self.message_colour = CREAM

        if island == "Treasure":
            self.message = (
                "Treasure reached! Now check your route."
            )
            self.message_colour = GOLD

    def get_travel_cost(self, start, end):
        for neighbour, cost in self.graph[start]:
            if neighbour == end:
                return cost

        return None

    def reset_route(self):
        self.route = ["Port"]
        self.distance = 0

        self.message = (
            "Route reset. Choose your first island."
        )
        self.message_colour = CREAM

    def check_route(self):
        if self.route[-1] != "Treasure":
            self.message = (
                "Your route must finish at Treasure."
            )
            self.message_colour = RED
            return

        if self.distance == self.safest_distance:
            play_sound("correct")
            self.puzzle_complete = True
            if self.puzzle_number < len(self.puzzle_costs) - 1:
                self.check_button.text = "Next Chart"
                self.message = "Correct! Prepare the next chart."
            else:
                self.check_button.text = "Sail This Route"
                self.message = "Correct! Now sail through the storm."

            self.message_colour = GREEN

        else:
            play_sound("wrong")
            self.message = (
                "Your danger was "
                + str(self.distance)
                + ". A safer route exists!"
            )
            self.message_colour = RED

    def route_contains_edge(self, first, second):
        for number in range(len(self.route) - 1):
            route_start = self.route[number]
            route_end = self.route[number + 1]

            if (
                route_start == first
                and route_end == second
            ):
                return True

            if (
                route_start == second
                and route_end == first
            ):
                return True

        return False

    def draw_connections(self, screen):
        drawn_connections = set()

        for island in self.graph:
            for neighbour, travel_cost in self.graph[island]:
                connection = tuple(
                    sorted((island, neighbour))
                )

                if connection in drawn_connections:
                    continue

                drawn_connections.add(connection)

                start = self.island_positions[island]
                end = self.island_positions[neighbour]

                if self.route_contains_edge(
                    island,
                    neighbour,
                ):
                    colour = GREEN
                    line_width = 7
                else:
                    colour = GREY
                    line_width = 3

                pygame.draw.line(
                    screen,
                    colour,
                    start,
                    end,
                    width=line_width,
                )

                middle_x = (
                    start[0] + end[0]
                ) // 2
                middle_y = (
                    start[1] + end[1]
                ) // 2

                cost_text = self.small_font.render(
                    str(travel_cost),
                    True,
                    CREAM,
                )
                cost_rect = cost_text.get_rect(
                    center=(middle_x, middle_y)
                )

                pygame.draw.circle(
                    screen,
                    NAVY,
                    (middle_x, middle_y),
                    14,
                )
                screen.blit(cost_text, cost_rect)

    def draw_islands(self, screen):
        for island, position in self.island_positions.items():
            if island == self.route[-1]:
                outline_colour = GOLD
            elif island in self.route:
                outline_colour = GREEN
            else:
                outline_colour = CREAM

            x, y = position
            pygame.draw.circle(
                screen,
                outline_colour,
                position,
                43,
                width=4,
            )

            image = self.island_images[island]
            image_rect = image.get_rect(center=position)
            screen.blit(image, image_rect)

            label = self.small_font.render(island, True, NAVY)
            label_rect = label.get_rect(center=(x, y + 48))
            label_panel = label_rect.inflate(12, 5)
            pygame.draw.rect(screen, CREAM, label_panel, border_radius=5)
            pygame.draw.rect(screen, outline_colour, label_panel, width=2, border_radius=5)
            screen.blit(label, label_rect)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        instruction_panel = pygame.Rect(230, 72, 540, 38)
        pygame.draw.rect(screen, NAVY, instruction_panel)
        pygame.draw.rect(screen, GOLD, instruction_panel, width=3)

        title = self.title_font.render(
            "The Navigator's Trial - Chart "
            + str(self.puzzle_number + 1)
            + " / "
            + str(len(self.puzzle_costs)),
            True,
            GOLD,
        )
        title_rect = title.get_rect(
            center=(WIDTH // 2, 42)
        )
        screen.blit(title, title_rect)

        instructions = self.small_font.render(
            "Click connected islands and reach Treasure "
            "with the lowest danger.",
            True,
            CREAM,
        )
        instructions_rect = instructions.get_rect(
            center=instruction_panel.center
        )
        screen.blit(
            instructions,
            instructions_rect,
        )

        self.draw_connections(screen)
        self.draw_islands(screen)

        message_panel = pygame.Rect(230, 570, 540, 42)
        pygame.draw.rect(screen, NAVY, message_panel)
        pygame.draw.rect(screen, GOLD, message_panel, width=3)

        message_image = self.small_font.render(
            self.message,
            True,
            self.message_colour,
        )
        message_rect = message_image.get_rect(
            center=message_panel.center
        )
        screen.blit(message_image, message_rect)

        self.reset_button.draw(screen)
        self.check_button.draw(screen)
        self.back_button.draw(screen)
