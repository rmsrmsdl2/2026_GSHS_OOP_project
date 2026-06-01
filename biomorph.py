import random
import pygame
from genome import Genome


class Biomorph:
    next_id = 1

    def __init__(self, genome=None, x=None, y=None, age=0):
        self.id = Biomorph.next_id
        Biomorph.next_id += 1
        self.genome = genome if genome else Genome()
        self.x = x if x is not None else random.randint(60, 1040)
        self.y = y if y is not None else random.randint(90, 650)
        self.fitness = 0.0
        self.selection_error = 0.0
        self.energy = 1.0
        self.age = age

        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)

    def update(self, width, height):
        speed = 0.5 + self.genome.traits["movement_speed"] * 2.5
        efficiency = self.genome.traits["energy_efficiency"]

        self.x += self.dx * speed
        self.y += self.dy * speed
        self.energy -= 0.00045 * speed * (1.25 - efficiency)

        if random.random() < 0.018:
            self.dx += random.uniform(-0.7, 0.7)
            self.dy += random.uniform(-0.7, 0.7)

        length = max(0.2, (self.dx ** 2 + self.dy ** 2) ** 0.5)
        self.dx /= length
        self.dy /= length

        if self.x < 20 or self.x > width - 20:
            self.dx *= -1
        if self.y < 80 or self.y > height - 20:
            self.dy *= -1

        self.x = max(20, min(width - 20, self.x))
        self.y = max(80, min(height - 20, self.y))

    def reproduce_with(self, partner):
        child_genome = self.genome.crossover(partner.genome).mutate()
        child_x = (self.x + partner.x) / 2 + random.randint(-35, 35)
        child_y = (self.y + partner.y) / 2 + random.randint(-35, 35)
        return Biomorph(child_genome, child_x, child_y)

    def get_color(self):
        angle = self.genome.traits["branch_angle"]
        efficiency = self.genome.traits["energy_efficiency"]
        speed = self.genome.traits["movement_speed"]

        brightness = 0.55 + self.fitness * 0.45
        return (
            int((70 + angle * 170) * brightness),
            int((90 + efficiency * 145) * brightness),
            int((95 + speed * 135) * brightness),
        )

    def draw(self, screen):
        size = int(8 + self.genome.traits["body_size"] * 18)
        angle = self.genome.traits["branch_angle"]
        speed = self.genome.traits["movement_speed"]

        color = self.get_color()
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

        branch_len = size + 8 + speed * 6
        spread = 0.25 + angle * 0.95
        left_x = self.x - branch_len * spread
        right_x = self.x + branch_len * spread
        top_y = self.y - branch_len

        pygame.draw.line(screen, color, (self.x, self.y), (left_x, top_y), 2)
        pygame.draw.line(screen, color, (self.x, self.y), (right_x, top_y), 2)

        if self.fitness > 0.78:
            pygame.draw.circle(screen, (245, 220, 120), (int(self.x), int(self.y)), size + 3, 1)
