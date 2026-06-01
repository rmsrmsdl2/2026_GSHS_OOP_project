import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TRAIT_NAMES


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 20)
        self.small_font = pygame.font.SysFont("malgungothic", 16)

    def draw(self, world):
        self.screen.fill((18, 22, 28))
        self._draw_environment_panel(world)
        self._draw_biomorphs(world)
        self._draw_trait_panel(world)
        self._draw_graph(world)
        pygame.display.flip()

    def _draw_biomorphs(self, world):
        for biomorph in world.population:
            biomorph.draw(self.screen)

    def _draw_environment_panel(self, world):
        pygame.draw.rect(self.screen, (32, 38, 48), (0, 0, SCREEN_WIDTH, 72))

        lines = [
            f"Generation: {world.generation}",
            f"Population: {len(world.population)}",
            f"Environment: {world.environment.name}",
            "SPACE: pause | N: next generation | ESC: quit",
        ]

        x = 20
        for text in lines:
            img = self.font.render(text, True, (230, 235, 240))
            self.screen.blit(img, (x, 22))
            x += img.get_width() + 35

    def _draw_trait_panel(self, world):
        x = SCREEN_WIDTH - 280
        y = 90

        pygame.draw.rect(self.screen, (28, 34, 43), (x, y, 250, 230))
        title = self.font.render("Average Traits", True, (255, 255, 255))
        self.screen.blit(title, (x + 15, y + 12))

        averages = world.get_average_traits()

        for i, name in enumerate(TRAIT_NAMES):
            value = averages[name]
            optimal = world.environment.optimal_traits[name]

            label = self.small_font.render(f"{name}: {value:.2f}", True, (220, 220, 220))
            self.screen.blit(label, (x + 15, y + 48 + i * 32))

            pygame.draw.rect(self.screen, (55, 62, 75), (x + 145, y + 52 + i * 32, 80, 8))
            pygame.draw.rect(self.screen, (80, 180, 120), (x + 145, y + 52 + i * 32, int(value * 80), 8))
            pygame.draw.circle(self.screen, (240, 190, 80), (x + 145 + int(optimal * 80), y + 56 + i * 32), 5)

    def _draw_graph(self, world):
        if len(world.average_trait_history) < 2:
            return

        x = 30
        y = SCREEN_HEIGHT - 180
        w = 420
        h = 130

        pygame.draw.rect(self.screen, (28, 34, 43), (x, y, w, h))
        title = self.small_font.render("Trait Change Graph", True, (240, 240, 240))
        self.screen.blit(title, (x + 12, y + 10))

        colors = {
            "body_size": (240, 100, 100),
            "branch_angle": (100, 180, 255),
            "movement_speed": (255, 210, 90),
            "energy_efficiency": (100, 220, 140),
            "mutation_rate": (210, 120, 255),
        }

        max_points = min(30, len(world.average_trait_history))
        data = world.average_trait_history[-max_points:]

        for trait in TRAIT_NAMES:
            points = []
            for i, record in enumerate(data):
                px = x + 20 + i * ((w - 40) / max(1, max_points - 1))
                py = y + h - 20 - record[trait] * (h - 45)
                points.append((px, py))

            if len(points) >= 2:
                pygame.draw.lines(self.screen, colors[trait], False, points, 2)


class InputHandler:
    def handle(self, event, world):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.toggle_pause()
            elif event.key == pygame.K_n:
                world.next_generation()
            elif event.key == pygame.K_ESCAPE:
                return False

        return True