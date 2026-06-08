import pygame

from config import (
    FACTOR_LABELS,
    FACTOR_NAMES,
    GENERATION_INTERVAL,
    GRID_COLUMNS,
    GRID_ROWS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TRAIT_ENVIRONMENT_NOTES,
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
        ranked_ids = {biomorph.id: rank for rank, (biomorph, _score) in enumerate(world.ranked_population()[:5], start=1)}

        for index, biomorph in enumerate(world.population):
            score = world.fitness(biomorph)
            rank = ranked_ids.get(biomorph.id)
            self._draw_card(index, biomorph, world.selected_index == index, rank, score)

        self._draw_environment_panel(world)
        self._draw_gene_panel(world)
        self._draw_mechanism_panel(world)
        pygame.display.flip()

    def _draw_header(self, world):
        pygame.draw.rect(self.screen, (35, 39, 43), (0, 0, SCREEN_WIDTH, 76))
        title = self.font.render("수학적 바이오모프 환경 적응 시뮬레이션", True, (241, 244, 238))
        env_mode = "자동" if world.environment.auto_mode else "수동"
        gen_mode = "자동" if world.auto_generation else "수동"
        info = self.small_font.render(
            f"세대 {world.generation} | 환경 {env_mode} | 세대교체 {gen_mode} | 클릭: 정보 | N: 다음세대 | A: 환경자동 | G: 세대자동 | D: 자연재해",
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
        right_panel = 318
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

    def _draw_card(self, index, biomorph, selected, rank, score):
        rect = self.card_rects[index]
        bg = (30, 34, 36) if not selected else (41, 45, 39)
        border = (68, 74, 78)
        if rank:
            border = (106, 205, 137)
        if selected:
            border = (237, 201, 92)

        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, border, rect, 1 if not selected else 2, border_radius=8)

        left_text = f"#{biomorph.id}"
        if rank:
            left_text += f"  {rank}위"
        number = self.tiny_font.render(left_text, True, (190, 197, 187))
        fitness = self.tiny_font.render(f"{score:.2f}", True, (153, 205, 183) if rank else (178, 188, 177))
        self.screen.blit(number, (rect.x + 10, rect.y + 8))
        self.screen.blit(fitness, (rect.right - fitness.get_width() - 10, rect.y + 8))
        biomorph.draw(self.screen, rect.inflate(-16, -28), selected)

    def _draw_environment_panel(self, world):
        x = SCREEN_WIDTH - 292
        y = 96
        w = 268
        h = 214
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        mode = "자동 변화" if world.environment.auto_mode else "수동 조절"
        title = self.small_font.render(f"환경 변수 ({mode})", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 14))

        for i, name in enumerate(FACTOR_NAMES):
            value = world.environment.factors[name]
            selected = name == world.environment.selected_factor
            row_y = y + 46 + i * 28
            color = (237, 201, 92) if selected else (217, 223, 214)
            label = self.tiny_font.render(f"{i + 1}. {FACTOR_LABELS[name]} {value:.2f}", True, color)
            self.screen.blit(label, (x + 16, row_y))
            pygame.draw.rect(self.screen, (58, 64, 66), (x + 102, row_y + 5, 130, 7), border_radius=4)
            pygame.draw.rect(self.screen, (117, 173, 205), (x + 102, row_y + 5, int(130 * value), 7), border_radius=4)

        progress = world.frame_count / GENERATION_INTERVAL
        pygame.draw.rect(self.screen, (58, 64, 66), (x + 16, y + 166, 232, 8), border_radius=4)
        pygame.draw.rect(self.screen, (153, 205, 183), (x + 16, y + 166, int(232 * progress), 8), border_radius=4)
        guide = self.tiny_font.render("1-4 선택, ←/→ 수동 조절, A 자동 전환", True, (184, 193, 181))
        self.screen.blit(guide, (x + 16, y + 184))

    def _draw_gene_panel(self, world):
        biomorph = world.selected
        x = SCREEN_WIDTH - 292
        y = 326
        w = 268
        h = 266
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        score = world.fitness(biomorph)
        title = self.small_font.render(f"선택 개체 적합도 {score:.2f}", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 14))

        compact_traits = TRAIT_NAMES[:6]
        for i, name in enumerate(compact_traits):
            value = biomorph.genome.traits[name]
            target = world.environment.optimal_traits[name]
            row_y = y + 43 + i * 35
            label = self.tiny_font.render(f"{TRAIT_LABELS[name]} {value:.2f}", True, (217, 223, 214))
            self.screen.blit(label, (x + 16, row_y))
            pygame.draw.rect(self.screen, (58, 64, 66), (x + 112, row_y + 5, 120, 7), border_radius=4)
            pygame.draw.rect(self.screen, (117, 190, 151), (x + 112, row_y + 5, int(120 * value), 7), border_radius=4)
            target_x = x + 112 + int(120 * target)
            pygame.draw.line(self.screen, (237, 201, 92), (target_x, row_y + 2), (target_x, row_y + 15), 2)

        note_name = compact_traits[world.generation % len(compact_traits)]
        note = TRAIT_ENVIRONMENT_NOTES[note_name]
        note_img = self.tiny_font.render(note, True, (184, 193, 181))
        self.screen.blit(note_img, (x + 16, y + 232))

    def _draw_mechanism_panel(self, world):
        x = SCREEN_WIDTH - 292
        y = 608
        w = 268
        h = 128
        pygame.draw.rect(self.screen, (30, 34, 36), (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, (68, 74, 78), (x, y, w, h), 1, border_radius=8)

        title = self.small_font.render("작동 원리", True, (241, 244, 238))
        self.screen.blit(title, (x + 16, y + 10))
        lines = [
            "상위 5개체 -> 각 3자손 -> 다음 세대",
            "큰 날개+강풍처럼 조합도 적합도에 반영",
            "D키 자연재해는 연속 변화가 아닌 급격한 사건",
        ]
        for i, text in enumerate(lines):
            img = self.tiny_font.render(text, True, (205, 213, 202))
            self.screen.blit(img, (x + 16, y + 34 + i * 18))

        for i, text in enumerate(world.environment.event_log[-2:]):
            img = self.tiny_font.render(text, True, (153, 205, 183))
            self.screen.blit(img, (x + 16, y + 92 + i * 16))

    def get_card_index_at(self, position):
        for index, rect in enumerate(self.card_rects):
            if rect.collidepoint(position):
                return index
        return None


class InputHandler:
    def handle(self, event, world, renderer):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            index = renderer.get_card_index_at(event.pos)
            if index is not None:
                world.select(index)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                world.next_generation()
            elif event.key == pygame.K_r:
                world.randomize()
            elif event.key == pygame.K_SPACE:
                world.toggle_pause()
            elif event.key == pygame.K_a:
                world.environment.toggle_auto_mode()
            elif event.key == pygame.K_g:
                world.toggle_auto_generation()
            elif event.key == pygame.K_d:
                world.trigger_disaster()
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                world.environment.select_factor(event.key - pygame.K_1)
            elif event.key == pygame.K_LEFT:
                world.environment.adjust_selected_factor(-0.05)
            elif event.key == pygame.K_RIGHT:
                world.environment.adjust_selected_factor(0.05)
            elif event.key == pygame.K_ESCAPE:
                return False

        return True
