import math
import pygame

from config import MIN_SEGMENT_LENGTH
from genome import Genome


class Biomorph:
    next_id = 1

    def __init__(self, genome=None, parent_id=None):
        self.id = Biomorph.next_id
        Biomorph.next_id += 1
        self.parent_id = parent_id
        self.genome = genome if genome else Genome()

    def breed_child(self):
        return Biomorph(self.genome.child_variant(), parent_id=self.id)

    def crossover_child(self, other):
        return Biomorph(self.genome.crossover(other.genome).mutate(), parent_id=self.id)

    def get_color(self):
        angle = self.genome.traits["branch_angle"]
        width = self.genome.traits["body_width"]
        wing = self.genome.traits["wing_span"]
        return (
            int(72 + angle * 128),
            int(88 + wing * 126),
            int(105 + width * 96),
        )

    def draw(self, surface, rect, selected=False):
        center_x = rect.centerx
        base_y = rect.centery + rect.height * 0.31
        color = self.get_color()
        body_color = self._mix(color, (230, 236, 228), 0.22)
        line_width = max(1, int(self.genome.scaled("body_width", 1.0, 2.6)))

        if selected:
            pygame.draw.rect(surface, (245, 211, 97), rect.inflate(-6, -6), 2, border_radius=8)

        self._draw_wings(surface, center_x, base_y, color)
        self._draw_body(surface, center_x, base_y, body_color, line_width)
        self._draw_branch_pair(surface, center_x, base_y - 8, -math.pi / 2, self._trunk_length(), self.genome.recursion_depth(), line_width, color)
        self._draw_antennae(surface, center_x, base_y - self._trunk_length() * 0.92, color)

    def _draw_body(self, surface, x, base_y, color, line_width):
        length = self._trunk_length()
        width = self.genome.scaled("body_width", 6, 17)
        thorax_y = base_y - length * 0.40
        head_y = base_y - length * 0.82

        pygame.draw.ellipse(surface, color, (x - width * 0.40, base_y - length * 0.38, width * 0.80, length * 0.50), line_width)
        pygame.draw.ellipse(surface, color, (x - width * 0.52, thorax_y - width * 0.45, width * 1.04, width * 0.90), line_width)
        pygame.draw.circle(surface, color, (int(x), int(head_y)), max(5, int(width * 0.34)), line_width)
        pygame.draw.line(surface, color, (x, base_y), (x, head_y), max(1, line_width))

    def _draw_wings(self, surface, x, base_y, color):
        span = self.genome.scaled("wing_span", 10, 34)
        height = self.genome.scaled("branch_ratio", 15, 42)
        alpha_color = self._mix(color, (255, 255, 255), 0.45)
        wing_y = base_y - self._trunk_length() * 0.52

        left = [
            (x - 3, wing_y),
            (x - span, wing_y - height * 0.72),
            (x - span * 0.58, wing_y + height * 0.42),
        ]
        right = [(2 * x - px, py) for px, py in left]
        pygame.draw.polygon(surface, alpha_color, left, 1)
        pygame.draw.polygon(surface, alpha_color, right, 1)

    def _draw_antennae(self, surface, x, y, color):
        length = self.genome.scaled("trunk_length", 9, 23)
        angle = self.genome.scaled("antenna_angle", 0.25, 1.05)

        for side in (-1, 1):
            end_x = x + math.cos(-math.pi / 2 + side * angle) * length
            end_y = y + math.sin(-math.pi / 2 + side * angle) * length
            pygame.draw.line(surface, color, (x, y), (end_x, end_y), 1)
            pygame.draw.circle(surface, color, (int(end_x), int(end_y)), 2)

    def _draw_branch_pair(self, surface, x, y, angle, length, depth, width, color):
        self._draw_recursive_branch(surface, x, y, angle, length, depth, width, color)

    def _draw_recursive_branch(self, surface, x, y, angle, length, depth, width, color):
        if depth <= 0 or length < MIN_SEGMENT_LENGTH:
            return

        curve = self.genome.scaled("curvature", -0.28, 0.28)
        next_x = x + math.cos(angle + curve) * length
        next_y = y + math.sin(angle + curve) * length
        pygame.draw.line(surface, color, (x, y), (next_x, next_y), max(1, int(width)))

        branch_angle = self.genome.scaled("branch_angle", 0.28, 0.95)
        ratio = self.genome.scaled("branch_ratio", 0.48, 0.68)
        next_width = max(1, width * 0.65)

        for side in (-1, 1):
            self._draw_recursive_branch(
                surface,
                next_x,
                next_y,
                angle + side * branch_angle + curve * 0.45,
                length * ratio,
                depth - 1,
                next_width,
                color,
            )

    def _trunk_length(self):
        return self.genome.scaled("trunk_length", 22, 49)

    def _mix(self, color, other, amount):
        return tuple(int(color[i] * (1.0 - amount) + other[i] * amount) for i in range(3))
