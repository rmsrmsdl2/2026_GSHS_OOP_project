import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, TRAIT_LABELS, TRAIT_NAMES


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 20)
        self.small_font = pygame.font.SysFont("malgungothic", 16)
        self.tiny_font = pygame.font.SysFont("malgungothic", 13)
        self.trait_colors = {
            "body_size": (238, 105, 95),
            "branch_angle": (96, 178, 255),
            "movement_speed": (255, 204, 92),
            "energy_efficiency": (97, 214, 142),
            "mutation_rate": (204, 126, 255),
        }

    def draw(self, world):
        self.screen.fill((15, 18, 23))
        self._draw_header(world)
        self._draw_environment_field(world)
        self._draw_biomorphs(world)
        self._draw_environment_panel(world)
        self._draw_trait_panel(world)
        self._draw_fitness_panel(world)
        self._draw_event_log(world)
        pygame.display.flip()

    def _draw_header(self, world):
        pygame.draw.rect(self.screen, (29, 35, 44), (0, 0, SCREEN_WIDTH, 72))
        items = [
            f"Generation {world.generation}",
            f"Population {len(world.population)}",
            f"Mode {world.environment.mode}: {world.environment.name}",
            f"Speed x{world.speed_multiplier}",
            "SPACE pause | N next | 1 stable | 2 periodic | 3 shock | F speed | ESC quit",
        ]

        x = 18
        for index, text in enumerate(items):
            color = (242, 244, 247) if index < 4 else (174, 184, 196)
            img = self.small_font.render(text, True, color)
            self.screen.blit(img, (x, 26))
            x += img.get_width() + 28

    def _draw_environment_field(self, world):
        factors = world.environment.factors
        sunlight = factors["sunlight"]
        food = factors["food"]
        wind = factors["wind"]

        sky = (
            int(18 + sunlight * 42),
            int(28 + sunlight * 45),
            int(38 + sunlight * 52),
        )
        pygame.draw.rect(self.screen, sky, (0, 72, SCREEN_WIDTH - 330, SCREEN_HEIGHT - 72))

        food_color = (45, int(80 + food * 100), 62)
        pygame.draw.rect(self.screen, food_color, (0, SCREEN_HEIGHT - 86, SCREEN_WIDTH - 330, 86))

        for i in range(9):
            y = 112 + i * 58
            start_x = 20 + (world.generation * 7 + i * 37) % 160
            length = int(40 + wind * 90)
            pygame.draw.line(
                self.screen,
                (80, 96, 112),
                (start_x, y),
                (start_x + length, y - int(wind * 16)),
                1,
            )

    def _draw_biomorphs(self, world):
        for biomorph in sorted(world.population, key=lambda item: item.fitness):
            biomorph.draw(self.screen)

    def _draw_environment_panel(self, world):
        x = SCREEN_WIDTH - 315
        y = 88
        self._panel(x, y, 295, 180, "Environment Pressure")

        lines = [
            world.environment.description,
            f"Dominant trait: {TRAIT_LABELS[world.environment.get_dominant_pressure()]}",
        ]
        for i, text in enumerate(lines):
            img = self.tiny_font.render(text, True, (210, 216, 224))
            self.screen.blit(img, (x + 14, y + 38 + i * 22))

        factors = world.environment.factors
        labels = [("Sunlight", "sunlight"), ("Food", "food"), ("Wind", "wind"), ("Temp", "temperature")]
        for i, (label, key) in enumerate(labels):
            self._bar(x + 14, y + 88 + i * 20, 160, 8, factors[key], (105, 166, 240), label)

    def _draw_trait_panel(self, world):
        x = SCREEN_WIDTH - 315
        y = 284
        self._panel(x, y, 295, 232, "Trait Average vs Optimal")

        averages = world.get_average_traits()
        for i, name in enumerate(TRAIT_NAMES):
            y_pos = y + 42 + i * 34
            label = TRAIT_LABELS[name]
            value = averages[name]
            optimal = world.environment.optimal_traits[name]
            color = self.trait_colors[name]

            text = self.tiny_font.render(f"{label}  avg {value:.2f} / opt {optimal:.2f}", True, (222, 226, 232))
            self.screen.blit(text, (x + 14, y_pos))

            pygame.draw.rect(self.screen, (57, 64, 76), (x + 14, y_pos + 18, 214, 8))
            pygame.draw.rect(self.screen, color, (x + 14, y_pos + 18, int(value * 214), 8))
            pygame.draw.line(
                self.screen,
                (255, 238, 145),
                (x + 14 + int(optimal * 214), y_pos + 14),
                (x + 14 + int(optimal * 214), y_pos + 30),
                2,
            )

    def _draw_fitness_panel(self, world):
        x = 26
        y = SCREEN_HEIGHT - 205
        self._panel(x, y, 610, 176, "Evolution Analytics")

        stats = world.engine.last_stats
        summary = (
            f"Best fitness {stats['best_fitness']:.3f}   "
            f"Average fitness {stats['average_fitness']:.3f}   "
            f"Average error D {stats['average_error']:.3f}   "
            f"Survivors {stats['survivors']}   Births {stats['births']}"
        )
        img = self.tiny_font.render(summary, True, (222, 226, 232))
        self.screen.blit(img, (x + 14, y + 38))

        self._line_graph(x + 18, y + 70, 270, 82, world.fitness_history, (104, 216, 142), "fitness")
        self._line_graph(x + 318, y + 70, 260, 82, world.error_history, (238, 105, 95), "selection error")

    def _draw_event_log(self, world):
        x = SCREEN_WIDTH - 315
        y = 532
        self._panel(x, y, 295, 170, "Environment Events")

        if not world.environment.event_log:
            return

        for i, (generation, name) in enumerate(world.environment.event_log[-5:]):
            text = self.tiny_font.render(f"Gen {generation}: {name}", True, (214, 220, 228))
            self.screen.blit(text, (x + 14, y + 40 + i * 24))

    def _line_graph(self, x, y, w, h, values, color, label):
        pygame.draw.rect(self.screen, (21, 26, 34), (x, y, w, h))
        text = self.tiny_font.render(label, True, (182, 192, 204))
        self.screen.blit(text, (x + 8, y + 7))

        if len(values) < 2:
            return

        visible = values[-50:]
        high = max(visible)
        low = min(visible)
        span = max(0.001, high - low)
        points = []

        for i, value in enumerate(visible):
            px = x + 12 + i * ((w - 24) / max(1, len(visible) - 1))
            py = y + h - 12 - ((value - low) / span) * (h - 34)
            points.append((px, py))

        pygame.draw.lines(self.screen, color, False, points, 2)

    def _bar(self, x, y, w, h, value, color, label):
        text = self.tiny_font.render(f"{label} {value:.2f}", True, (213, 219, 226))
        self.screen.blit(text, (x, y - 14))
        pygame.draw.rect(self.screen, (55, 62, 74), (x + 76, y, w, h))
        pygame.draw.rect(self.screen, color, (x + 76, y, int(w * value), h))

    def _panel(self, x, y, w, h, title):
        pygame.draw.rect(self.screen, (27, 32, 40), (x, y, w, h))
        pygame.draw.rect(self.screen, (57, 65, 78), (x, y, w, h), 1)
        img = self.small_font.render(title, True, (242, 244, 248))
        self.screen.blit(img, (x + 14, y + 12))


class InputHandler:
    def handle(self, event, world):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.toggle_pause()
            elif event.key == pygame.K_n:
                world.next_generation()
            elif event.key == pygame.K_f:
                world.cycle_speed()
            elif event.key == pygame.K_1:
                world.environment.mode = world.environment.STABLE
                world.environment._record_mode_event()
                world.next_generation()
            elif event.key == pygame.K_2:
                world.environment.mode = world.environment.PERIODIC
                world.environment._record_mode_event()
                world.next_generation()
            elif event.key == pygame.K_3:
                world.environment.mode = world.environment.SHOCK
                world.environment._record_mode_event()
                world.next_generation()
            elif event.key == pygame.K_ESCAPE:
                return False

        return True
