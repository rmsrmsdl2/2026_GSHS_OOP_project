import pygame

from config import (
    GRID_COLUMNS,
    GRID_ROWS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TRAIT_LABELS,
    TRAIT_NAMES,
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 20)
        self.small_font = pygame.font.SysFont("malgungothic", 16)
        self.tiny_font = pygame.font.SysFont("malgungothic", 13)
        self.card_rects = []

    def draw(self, world):
        self.screen.fill((18, 20, 22))
        self._draw_header(world)
        self.card_rects = self._layout_cards()
        best_index = self._best_index(world)

        for index, biomorph in enumerate(world.population):
            score = world.fitness(biomorph)
            self._draw_card(index, biomorph, world.selected_index == index, index == best_index, score)

        self._draw_environment_panel(world)
        self._draw_gene_panel(world)
        pygame.display.flip()

    def _draw_header(self, world):
        pygame.draw.rect(self.screen, (35, 39, 43), (0, 0, SCREEN_WIDTH, 76))
        title = self.font.render("수학적 바이오모프 곤충 모형", True, (241, 244, 238))
        info = self.small_font.render(
            f"세대 {world.generation}   |   클릭: 부모 선택   |   N: 선택 개체 변이   |   R: 무작위 초기화   |   ESC: 종료",
            True,
            (191, 199, 190),
        )
        message = self.tiny_font.render(world.message, True, (153, 205, 183))
        self.screen.blit(title, (24, 15))
        self.screen.blit(info, (24, 43))
        self.screen.blit(message, (760, 45))

    def _layout_cards(self):
        rects = []
        left = 24
        top = 96
        right_panel = 286
        gap = 14
        area_w = SCREEN_WIDTH - right_panel - left - 20
        area_h = SCREEN_HEIGHT - top - 24
        card_w = (area_w - gap * (GRID_COLUMNS - 1)) / GRID_COLUMNS
        card_h = (area_h - gap * (GRID_ROWS - 1)) / GRID_ROWS

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                x = left + col * (card_w + gap)
                y = top + row * (card_h + gap)
                rects.append(pygame.Rect(round(x), round(y), round(card_w), round(card_h)))

        return rects

    def _draw_card(self, index, biomorph, selected, best, score):
        rect = self.card_rects[index]
        bg = (30, 34, 36) if not selected else (41, 45, 39)
        border = (68, 74, 78)
        if best:
            border = (106, 205, 137)
        if selected:
            border = (237, 201, 92)

        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, border, rect, 1 if not selected else 2, border_radius=8)

        number = self.tiny_font.render(f"#{biomorph.id}", True, (190, 197, 187))
        fitness = self.tiny_font.render(f"{score:.2f}", True, (153, 205, 183) if best else (178, 188, 177))
        self.screen.blit(number, (rect.x + 10, rect.y + 8))
        self.screen.blit(fitness, (rect.right - fitness.get_width() - 10, rect.y + 8))
        biomorph.draw(self.screen, rect.inflate(-16, -28), selected)

    def _draw_environment_panel(self, world):
        x = SCREEN_WIDTH - 266
        y = 96
        w = 242
        h = 164
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        title = self.small_font.render("자동 변화 환경", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 16))

        labels = {
            "light": "빛",
            "humidity": "습도",
            "wind": "바람",
            "temperature": "온도",
        }
        for i, (name, value) in enumerate(world.environment.factors.items()):
            row_y = y + 48 + i * 28
            label = self.tiny_font.render(f"{labels[name]} {value:.2f}", True, (217, 223, 214))
            self.screen.blit(label, (x + 16, row_y))
            pygame.draw.rect(self.screen, (58, 64, 66), (x + 94, row_y + 5, 120, 7), border_radius=4)
            pygame.draw.rect(self.screen, (117, 173, 205), (x + 94, row_y + 5, int(120 * value), 7), border_radius=4)

    def _draw_gene_panel(self, world):
        biomorph = world.selected
        x = SCREEN_WIDTH - 266
        y = 278
        w = 242
        h = 322
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        score = world.fitness(biomorph)
        title = self.small_font.render(f"선택 유전자  적합도 {score:.2f}", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 16))

        compact_traits = TRAIT_NAMES[:7]
        for i, name in enumerate(compact_traits):
            value = biomorph.genome.traits[name]
            target = world.environment.optimal_traits[name]
            row_y = y + 45 + i * 39
            label = self.tiny_font.render(f"{TRAIT_LABELS[name]}  {value:.2f}", True, (217, 223, 214))
            self.screen.blit(label, (x + 16, row_y))
            pygame.draw.rect(self.screen, (58, 64, 66), (x + 16, row_y + 20, 198, 7), border_radius=4)
            pygame.draw.rect(
                self.screen,
                (117, 190, 151),
                (x + 16, row_y + 20, int(198 * value), 7),
                border_radius=4,
            )
            target_x = x + 16 + int(198 * target)
            pygame.draw.line(self.screen, (237, 201, 92), (target_x, row_y + 17), (target_x, row_y + 30), 2)

        self._draw_mechanism_panel(world)

    def _draw_mechanism_panel(self, world):
        x = SCREEN_WIDTH - 266
        y = SCREEN_HEIGHT - 126
        w = 242
        h = 102
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        title = self.small_font.render("작동 원리", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 12))
        lines = [
            "환경값이 자동으로 변함",
            "환경마다 유리한 형질이 달라짐",
            "노란 선은 현재 최적 형질",
            "클릭한 부모의 유전자가 변이됨",
        ]
        for i, text in enumerate(lines):
            img = self.tiny_font.render(text, True, (205, 213, 202))
            self.screen.blit(img, (x + 16, y + 36 + i * 18))

    def get_card_index_at(self, position):
        for index, rect in enumerate(self.card_rects):
            if rect.collidepoint(position):
                return index
        return None

    def _best_index(self, world):
        return max(range(len(world.population)), key=lambda index: world.fitness(world.population[index]))


class InputHandler:
    def handle(self, event, world, renderer):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            index = renderer.get_card_index_at(event.pos)
            if index is not None:
                world.select(index)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                world.mutate_selected()
            elif event.key == pygame.K_r:
                world.randomize()
            elif event.key == pygame.K_ESCAPE:
                return False

        return True
