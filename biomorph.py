import random
import pygame
from genome import Genome


class Biomorph:
    def __init__(self, genome=None, x=None, y=None):
        self.genome = genome if genome else Genome()
        self.x = x if x is not None else random.randint(60, 1040)
        self.y = y if y is not None else random.randint(90, 650)
        self.fitness = 0.0
        self.energy = 1.0

        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)

    def update(self, width, height):
        speed = 0.5 + self.genome.traits["movement_speed"] * 2.5
        efficiency = self.genome.traits["energy_efficiency"]

        self.x += self.dx * speed
        self.y += self.dy * speed
        self.energy -= 0.0007 * speed * (1.2 - efficiency)

        if self.x < 20 or self.x > width - 20:
            self.dx *= -1
        if self.y < 80 or self.y > height - 20:
            self.dy *= -1

        self.x = max(20, min(width - 20, self.x))
        self.y = max(80, min(height - 20, self.y))

    def reproduce(self):
        child_genome = self.genome.mutate()
        return Biomorph(child_genome, self.x + random.randint(-25, 25), self.y + random.randint(-25, 25))

    def get_color(self):
        angle = self.genome.traits["branch_angle"]
        efficiency = self.genome.traits["energy_efficiency"]
        speed = self.genome.traits["movement_speed"]

        return (
            int(80 + angle * 150),
            int(100 + efficiency * 130),
            int(100 + speed * 120),
        )

    def draw(self, screen):
        size = int(8 + self.genome.traits["body_size"] * 18)
        angle = self.genome.traits["branch_angle"]

        color = self.get_color()
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

        branch_len = size + 8
        left_x = self.x - branch_len * angle
        right_x = self.x + branch_len * angle
        top_y = self.y - branch_len

        pygame.draw.line(screen, color, (self.x, self.y), (left_x, top_y), 2)
        pygame.draw.line(screen, color, (self.x, self.y), (right_x, top_y), 2)