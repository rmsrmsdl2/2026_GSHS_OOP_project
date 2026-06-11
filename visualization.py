# -*- coding: utf-8 -*-

import pygame

from config import (
    FACTOR_LABELS,
    FACTOR_NAMES,
    GENERATION_INTERVAL,
    GRID_COLUMNS,
    GRID_ROWS,
    MAX_GENERATIONS,
    SCREEN_WIDTH,
    TRAIT_COLORS,
    TRAIT_ENVIRONMENT_NOTES,
    TRAIT_LABELS,
    TRAIT_NAMES,
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 22)
        self.small_font = pygame.font.SysFont("malgungothic", 16)
        self.tiny_font = pygame.font.SysFont("malgungothic", 13)
        self.card_rects = []
        self.start_buttons = {}
        self.colors = {
            "bg": (15, 18, 21),
            "panel": (27, 31, 35),
            "border": (62, 70, 76),
            "text": (239, 243, 238),
            "muted": (166, 176, 168),
            "accent": (153, 205, 183),
            "gold": (237, 201, 92),
            "danger": (235, 112, 101),
            "blue": (116, 196, 255),
        }

    def draw(self, world):
        self.screen.fill(self.colors["bg"])

        if not world.started:
            self._draw_start_page(world)
            pygame.display.flip()
            return

        if world.finished:
            self._draw_result_page(world)
            pygame.display.flip()
            return

        ranked = world.ranked_population()
        ranked_ids = {biomorph.id: rank for rank, (biomorph, _score) in enumerate(ranked[:5], start=1)}

        self._draw_header(world)
        self._draw_stage_background(world)
        self.card_rects = self._layout_cards()

        for index, biomorph in enumerate(world.population):
            score = world.fitness(biomorph)
            rank = ranked_ids.get(biomorph.id)
            self._draw_card(index, biomorph, world.selected_index == index, rank, score)

        self._draw_analytics_panel(world)
        self._draw_side_panel(world, ranked)
        pygame.display.flip()

    def _draw_header(self, world):
        pygame.draw.rect(self.screen, (24, 29, 33), (0, 0, SCREEN_WIDTH, 84))
        pygame.draw.line(self.screen, (54, 62, 68), (0, 83), (SCREEN_WIDTH, 83))
        title = self.font.render("환경 변화 적응 진화 시뮬레이터", True, self.colors["text"])
        subtitle = self.tiny_font.render("환경은 형질을 직접 바꾸지 않고, 어떤 개체가 부모로 선택될지를 바꿉니다.", True, self.colors["muted"])
        self.screen.blit(title, (24, 16))
        self.screen.blit(subtitle, (26, 48))
        self._metric_pill(560, 18, "세대", str(world.generation), self.colors["accent"])
        self._metric_pill(705, 18, "개체 수", str(len(world.population)), self.colors["blue"])
        self._metric_pill(842, 18, "모드", "자동" if world.auto_generation else "수동", self.colors["gold"])
        controls = "N 다음 세대   R 초기화   A 환경 자동   G 세대 자동   D 급변   1-4 요인 선택   <- -> 조절   SPACE 일시정지"
        self.screen.blit(self.tiny_font.render(controls, True, (184, 194, 187)), (560, 54))

    def _draw_stage_background(self, world):
        light = world.environment.factors["light"]
        humidity = world.environment.factors["humidity"]
        wind = world.environment.factors["wind"]
        field = pygame.Rect(18, 100, 920, 452)
        base = (int(22 + light * 24), int(28 + humidity * 22), int(30 + light * 20))
        pygame.draw.rect(self.screen, base, field, border_radius=10)
        pygame.draw.rect(self.screen, (55, 64, 68), field, 1, border_radius=10)

        for i in range(8):
            y = field.y + 28 + i * 50
            x = field.x + 28 + ((i * 83 + world.generation * 9) % 240)
            length = int(38 + wind * 82)
            pygame.draw.line(self.screen, (70, 83, 88), (x, y), (x + length, y - int(wind * 14)), 1)

        label = self.tiny_font.render("각 세대의 상위 적합도 개체가 자연선택되어 다음 세대의 부모가 됩니다.", True, (170, 181, 174))
        self.screen.blit(label, (field.x + 16, field.y + 12))

    def _layout_cards(self):
        rects = []
        left = 38
        top = 138
        gap = 10
        area_w = 880
        area_h = 386
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
        bg = (26, 31, 35) if not selected else (38, 42, 35)
        border = self.colors["gold"] if selected else (self.colors["accent"] if rank else self.colors["border"])
        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, border, rect, 2 if selected else 1, border_radius=8)

        if rank:
            self._small_badge(rect.x + 8, rect.y + 7, f"선택 {rank}", self.colors["accent"])
        else:
            self.screen.blit(self.tiny_font.render(f"#{biomorph.id}", True, self.colors["muted"]), (rect.x + 10, rect.y + 8))

        fitness = self.tiny_font.render(f"{score:.3f}", True, self.colors["accent"] if rank else (185, 195, 188))
        self.screen.blit(fitness, (rect.right - fitness.get_width() - 9, rect.y + 8))
        inner = rect.inflate(-16, -28)
        inner.y += 8
        biomorph.draw(self.screen, inner, selected)
        self._bar(rect.x + 9, rect.bottom - 14, rect.width - 18, 5, score, self.colors["accent"])

    def _draw_analytics_panel(self, world):
        rect = pygame.Rect(18, 568, 920, 168)
        self._panel(rect, "세대별 자연선택 분석 그래프")
        if len(world.history) < 2:
            msg = self.tiny_font.render("다음 세대가 진행되면 그래프가 누적됩니다.", True, self.colors["muted"])
            self.screen.blit(msg, (rect.x + 18, rect.y + 44))
            return

        self._line_graph(
            pygame.Rect(rect.x + 18, rect.y + 44, 420, 92),
            [
                ("평균 적합도", [row["avg_fitness"] for row in world.history], self.colors["accent"]),
                ("최고 적합도", [row["best_fitness"] for row in world.history], self.colors["gold"]),
            ],
            0.0,
            1.0,
        )
        self._line_graph(
            pygame.Rect(rect.x + 476, rect.y + 44, 420, 92),
            [("선택 오차 D", [row["avg_error"] for row in world.history], self.colors["danger"])],
            0.0,
            1.0,
        )
        latest = world.history[-1]
        summary = f"평균 적합도 {latest['avg_fitness']:.3f}   최고 적합도 {latest['best_fitness']:.3f}   평균 오차 D {latest['avg_error']:.3f}"
        self.screen.blit(self.tiny_font.render(summary, True, (205, 214, 207)), (rect.x + 18, rect.bottom - 24))

    def _draw_side_panel(self, world, ranked):
        x = 958
        self._draw_environment_panel(world, x, 100)
        self._draw_environment_graph(world, x, 284)
        self._draw_selected_panel(world, x, 430)
        self._draw_rank_event_panel(world, ranked, x, 650)

    def _draw_environment_panel(self, world, x, y):
        rect = pygame.Rect(x, y, 300, 166)
        self._panel(rect, "환경 선택압")
        mode = "자동" if world.environment.auto_mode else "수동"
        self._small_badge(rect.right - 72, rect.y + 15, mode, self.colors["gold"] if mode == "수동" else self.colors["accent"])

        for i, name in enumerate(FACTOR_NAMES):
            value = world.environment.factors[name]
            selected = name == world.environment.selected_factor
            row_y = rect.y + 44 + i * 26
            color = self.colors["gold"] if selected else self.colors["text"]
            self.screen.blit(self.tiny_font.render(f"{i + 1}. {FACTOR_LABELS[name]}", True, color), (rect.x + 16, row_y))
            self._bar(rect.x + 104, row_y + 4, 142, 8, value, self.colors["gold"] if selected else self.colors["blue"])
            value_img = self.tiny_font.render(f"{value:.2f}", True, self.colors["muted"])
            self.screen.blit(value_img, (rect.right - value_img.get_width() - 16, row_y))

        self._bar(rect.x + 16, rect.bottom - 17, 268, 6, world.frame_count / GENERATION_INTERVAL, self.colors["accent"])

    def _draw_environment_graph(self, world, x, y):
        rect = pygame.Rect(x, y, 300, 128)
        self._panel(rect, "환경 요인 변화")
        graph_rect = pygame.Rect(rect.x + 16, rect.y + 42, 268, 66)
        colors = {
            "light": (255, 214, 96),
            "humidity": (102, 190, 255),
            "wind": (178, 190, 204),
            "temperature": (238, 112, 101),
        }
        series = [(FACTOR_LABELS[name], [row["factors"][name] for row in world.history], colors[name]) for name in FACTOR_NAMES]
        self._line_graph(graph_rect, series, 0.0, 1.0, show_labels=False)

    def _draw_selected_panel(self, world, x, y):
        biomorph = world.selected
        score = world.fitness(biomorph)
        rect = pygame.Rect(x, y, 300, 202)
        self._panel(rect, f"선택 개체 #{biomorph.id}")
        self.screen.blit(self.small_font.render(f"적합도 exp(-D): {score:.3f}", True, self.colors["accent"]), (rect.x + 16, rect.y + 38))

        important = self._largest_trait_gaps(biomorph, world)[:4]
        for i, (name, gap) in enumerate(important):
            value = biomorph.genome.traits[name]
            target = world.environment.optimal_traits[name]
            row_y = rect.y + 68 + i * 28
            self.screen.blit(self.tiny_font.render(TRAIT_LABELS[name], True, self.colors["text"]), (rect.x + 16, row_y))
            self._bar(rect.x + 104, row_y + 4, 128, 8, value, TRAIT_COLORS[name])
            marker_x = rect.x + 104 + int(128 * target)
            pygame.draw.line(self.screen, self.colors["gold"], (marker_x, row_y), (marker_x, row_y + 16), 2)
            gap_img = self.tiny_font.render(f"{gap:.2f}", True, self.colors["muted"])
            self.screen.blit(gap_img, (rect.right - gap_img.get_width() - 16, row_y))

        note_name = important[0][0] if important else TRAIT_NAMES[0]
        note = self._shorten(TRAIT_ENVIRONMENT_NOTES[note_name], 36)
        self.screen.blit(self.tiny_font.render(note, True, (184, 194, 187)), (rect.x + 16, rect.bottom - 20))

    def _draw_rank_event_panel(self, world, ranked, x, y):
        rect = pygame.Rect(x, y, 300, 86)
        self._panel(rect, "이번 세대 자연선택")
        for i, (biomorph, score) in enumerate(ranked[:5]):
            px = rect.x + 16 + i * 52
            self._small_badge(px, rect.y + 38, f"#{biomorph.id}", self.colors["accent"])
            self.screen.blit(self.tiny_font.render(f"{score:.2f}", True, self.colors["muted"]), (px + 4, rect.y + 60))
        if world.message:
            msg = self.tiny_font.render(self._shorten(world.message, 34), True, self.colors["gold"])
            self.screen.blit(msg, (rect.x + 16, rect.bottom - 14))

    def _draw_start_page(self, world):
        self.start_buttons = {}
        title = self.font.render("환경 변화 적응 진화 시뮬레이터", True, self.colors["text"])
        subtitle = self.small_font.render("실험을 자동으로 진행할지, 초기 환경 변수를 직접 설정할지 선택하세요.", True, self.colors["muted"])
        self.screen.blit(title, (64, 52))
        self.screen.blit(subtitle, (66, 88))
        if world.setup_mode == "manual":
            self._draw_manual_setup(world)
        else:
            self._draw_mode_choice()

    def _draw_mode_choice(self):
        auto_rect = pygame.Rect(115, 185, 490, 350)
        manual_rect = pygame.Rect(675, 185, 490, 350)
        self.start_buttons["auto"] = auto_rect
        self.start_buttons["manual"] = manual_rect
        self._choice_card(auto_rect, "자동 실행", "환경 요인과 세대가 자동으로 진행됩니다.", "바로 시작", self.colors["accent"])
        self._choice_card(manual_rect, "수동 설정", "초기 환경을 직접 정하고 N으로 세대를 넘깁니다.", "환경 설정", self.colors["gold"])
        self.screen.blit(self.small_font.render("A: 자동 실행    M: 수동 설정    R: 새 개체군", True, self.colors["muted"]), (64, 650))

    def _draw_manual_setup(self, world):
        panel = pygame.Rect(94, 150, 1092, 510)
        self._panel(panel, "수동 초기 환경 설정")
        desc = "1-4로 환경 요인을 선택하고, 방향키로 값을 조절하세요. Enter를 누르면 이 환경으로 실험을 시작합니다."
        self.screen.blit(self.small_font.render(desc, True, self.colors["muted"]), (panel.x + 28, panel.y + 48))
        colors = {"light": (255, 214, 96), "humidity": (102, 190, 255), "wind": (178, 190, 204), "temperature": (238, 112, 101)}

        for i, name in enumerate(FACTOR_NAMES):
            value = world.environment.factors[name]
            selected = name == world.environment.selected_factor
            row_y = panel.y + 112 + i * 78
            label_color = self.colors["gold"] if selected else self.colors["text"]
            self.screen.blit(self.small_font.render(f"{i + 1}. {FACTOR_LABELS[name]}", True, label_color), (panel.x + 36, row_y))
            self._bar(panel.x + 210, row_y + 8, 640, 14, value, colors[name])
            self.screen.blit(self.small_font.render(f"{value:.2f}", True, self.colors["text"]), (panel.x + 880, row_y))

        start_rect = pygame.Rect(panel.right - 250, panel.bottom - 72, 206, 42)
        back_rect = pygame.Rect(panel.x + 28, panel.bottom - 72, 150, 42)
        self.start_buttons["start_manual"] = start_rect
        self.start_buttons["back"] = back_rect
        self._button(start_rect, "실험 시작", self.colors["accent"])
        self._button(back_rect, "뒤로", self.colors["border"])
        self.screen.blit(self.small_font.render(world.message, True, self.colors["gold"]), (panel.x + 28, panel.bottom - 112))

    def _choice_card(self, rect, title, body, button, accent):
        pygame.draw.rect(self.screen, self.colors["panel"], rect, border_radius=10)
        pygame.draw.rect(self.screen, accent, rect, 2, border_radius=10)
        self.screen.blit(self.font.render(title, True, self.colors["text"]), (rect.x + 34, rect.y + 38))
        self.screen.blit(self.small_font.render(body, True, self.colors["muted"]), (rect.x + 36, rect.y + 98))
        lines = ["환경 변화: 자동", "세대 진행: 자동", "전체 흐름 관찰에 적합"] if title == "자동 실행" else ["환경 변화: 직접 설정", "세대 진행: 수동", "특정 조건 실험에 적합"]
        for i, line in enumerate(lines):
            self.screen.blit(self.small_font.render(f"- {line}", True, self.colors["text"]), (rect.x + 36, rect.y + 190 + i * 30))
        self._button(pygame.Rect(rect.x + 34, rect.bottom - 72, 160, 42), button, accent)

    def _button(self, rect, text, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        text_color = (14, 18, 19) if color != self.colors["border"] else self.colors["text"]
        img = self.small_font.render(text, True, text_color)
        self.screen.blit(img, (rect.centerx - img.get_width() // 2, rect.centery - img.get_height() // 2))

    def _draw_result_page(self, world):
        summary = world.experiment_summary()
        representative = summary["winner"]
        title = self.font.render("자연선택 결과 정리", True, self.colors["text"])
        subtitle = self.small_font.render(f"{MAX_GENERATIONS}세대 동안 부모로 선택된 개체군의 형질 변화를 정리합니다.", True, self.colors["muted"])
        self.screen.blit(title, (34, 28))
        self.screen.blit(subtitle, (36, 62))
        self._metric_pill(850, 30, "최종 세대", str(world.generation), self.colors["accent"])
        self._metric_pill(995, 30, "추적 형질", "6개", self.colors["gold"])
        self._metric_pill(1140, 30, "대표 적합도", f"{summary['winner_score']:.3f}", self.colors["blue"])

        rep_rect = pygame.Rect(34, 112, 300, 430)
        self._panel(rep_rect, "대표 선택 개체")
        portrait = pygame.Rect(rep_rect.x + 40, rep_rect.y + 78, 220, 230)
        pygame.draw.rect(self.screen, (20, 24, 28), portrait, border_radius=10)
        pygame.draw.rect(self.screen, self.colors["gold"], portrait, 2, border_radius=10)
        representative.draw(self.screen, portrait.inflate(-26, -22), selected=True)
        details = [
            f"대표 ID: #{representative.id}",
            f"부모 ID: {representative.parent_id if representative.parent_id is not None else '쌩랜덤 돌연변이'}",
            f"대표 적합도: {summary['winner_score']:.3f}",
            f"선택 오차 D: {summary['winner_error']:.3f}",
        ]
        for i, text in enumerate(details):
            self.screen.blit(self.small_font.render(text, True, self.colors["text"] if i == 0 else self.colors["muted"]), (rep_rect.x + 24, rep_rect.y + 330 + i * 24))

        spec_rect = pygame.Rect(354, 112, 256, 430)
        self._panel(spec_rect, "대표 개체 스펙")
        for i, name in enumerate(TRAIT_NAMES):
            value = representative.genome.traits[name]
            target = world.environment.optimal_traits[name]
            gap = abs(value - target)
            row_y = spec_rect.y + 48 + i * 38
            self.screen.blit(self.tiny_font.render(TRAIT_LABELS[name], True, self.colors["text"]), (spec_rect.x + 18, row_y))
            self._bar(spec_rect.x + 100, row_y + 4, 86, 7, value, TRAIT_COLORS[name])
            marker_x = spec_rect.x + 100 + int(86 * target)
            pygame.draw.line(self.screen, self.colors["gold"], (marker_x, row_y), (marker_x, row_y + 14), 2)
            self.screen.blit(self.tiny_font.render(f"{value:.2f} / 차이 {gap:.2f}", True, self.colors["muted"]), (spec_rect.x + 18, row_y + 17))

        trend_rect = pygame.Rect(632, 112, 280, 176)
        self._panel(trend_rect, "선택 부모 적합도 변화")
        self._line_graph(
            pygame.Rect(trend_rect.x + 18, trend_rect.y + 52, 244, 82),
            [
                ("전체 평균", [row["avg_fitness"] for row in world.history], self.colors["accent"]),
                ("최고", [row["best_fitness"] for row in world.history], self.colors["gold"]),
            ],
            0.0,
            1.0,
        )
        fit_text = f"부모 평균: {summary['initial_selected_fitness']:.3f} -> {summary['final_selected_fitness']:.3f}"
        self.screen.blit(self.tiny_font.render(fit_text, True, self.colors["accent"]), (trend_rect.x + 18, trend_rect.bottom - 28))

        trait_rect = pygame.Rect(632, 310, 614, 232)
        self._panel(trait_rect, "세대별 대표 형질 변화 그래프")
        tracked_traits = [
            "trunk_length",
            "branch_angle",
            "curvature",
            "body_width",
            "wing_span",
            "mutation_rate",
        ]
        graph_rect = pygame.Rect(trait_rect.x + 18, trait_rect.y + 50, 578, 130)
        series = [
            (
                TRAIT_LABELS[name],
                [row["avg_traits"][name] for row in world.history],
                TRAIT_COLORS[name],
            )
            for name in tracked_traits
        ]
        self._line_graph(graph_rect, series, 0.0, 1.0)
        guide = self.tiny_font.render("x축: 세대   y축: 개체군 평균 형질값", True, self.colors["muted"])
        self.screen.blit(guide, (trait_rect.x + 18, trait_rect.bottom - 30))

        close_rect = pygame.Rect(34, 574, 1212, 138)
        self._panel(close_rect, "결론")
        for i, text in enumerate(self._build_conclusion(summary)):
            self.screen.blit(self.small_font.render(text, True, self.colors["text"] if i == 0 else self.colors["muted"]), (close_rect.x + 22, close_rect.y + 42 + i * 26))
        guide = self.tiny_font.render("R: 새 실험 시작    ESC: 종료", True, self.colors["gold"])
        self.screen.blit(guide, (close_rect.right - guide.get_width() - 24, close_rect.bottom - 28))

    def _build_conclusion(self, summary):
        best_trait = summary["selected_improved_traits"][0][0]
        close_names = ", ".join(TRAIT_LABELS[name] for name, _gap in summary["closest_traits"][:3])
        fitness_delta = summary["final_avg_fitness"] - summary["initial_avg_fitness"]
        error_delta = summary["final_avg_error"] - summary["initial_avg_error"]
        return [
            "이 결과는 마지막 한 개체의 승패보다, 세대가 지나며 개체군 평균 형질이 어떻게 이동했는지를 보여줍니다.",
            f"선택 기록에서 가장 크게 증가한 형질은 '{TRAIT_LABELS[best_trait]}'입니다. 대표 개체는 {close_names} 형질에서 환경 기준에 가까웠습니다.",
            f"전체 집단 평균 적합도 변화는 {fitness_delta:+.3f}, 평균 선택 오차 D 변화는 {error_delta:+.3f}입니다.",
        ]

    def _line_graph(self, rect, series, min_value, max_value, show_labels=True):
        pygame.draw.rect(self.screen, (20, 24, 28), rect, border_radius=6)
        pygame.draw.rect(self.screen, (50, 58, 64), rect, 1, border_radius=6)
        for ratio in (0.25, 0.5, 0.75):
            y = rect.bottom - int(rect.height * ratio)
            pygame.draw.line(self.screen, (38, 44, 49), (rect.x + 8, y), (rect.right - 8, y), 1)
        span = max(0.001, max_value - min_value)
        for label, values, color in series:
            if len(values) < 2:
                continue
            visible = values[-60:]
            points = []
            for index, value in enumerate(visible):
                x = rect.x + 10 + index * ((rect.width - 20) / max(1, len(visible) - 1))
                normalized = (value - min_value) / span
                y = rect.bottom - 8 - normalized * (rect.height - 16)
                points.append((x, y))
            pygame.draw.lines(self.screen, color, False, points, 2)
        if show_labels:
            label_x = rect.x + 8
            for label, _values, color in series:
                text = self.tiny_font.render(label, True, color)
                self.screen.blit(text, (label_x, rect.y + 7))
                label_x += text.get_width() + 16

    def _largest_trait_gaps(self, biomorph, world):
        gaps = []
        for name in TRAIT_NAMES:
            trait = biomorph.genome.traits[name]
            target = world.environment.optimal_traits[name]
            gaps.append((name, abs(trait - target)))
        return sorted(gaps, key=lambda item: item[1], reverse=True)

    def _panel(self, rect, title):
        pygame.draw.rect(self.screen, self.colors["panel"], rect, border_radius=8)
        pygame.draw.rect(self.screen, self.colors["border"], rect, 1, border_radius=8)
        self.screen.blit(self.small_font.render(title, True, self.colors["text"]), (rect.x + 16, rect.y + 13))

    def _bar(self, x, y, w, h, value, color):
        value = max(0.0, min(1.0, value))
        pygame.draw.rect(self.screen, (50, 57, 62), (x, y, w, h), border_radius=h // 2)
        pygame.draw.rect(self.screen, color, (x, y, int(w * value), h), border_radius=h // 2)

    def _metric_pill(self, x, y, label, value, color):
        rect = pygame.Rect(x, y, 122, 30)
        pygame.draw.rect(self.screen, (31, 36, 40), rect, border_radius=8)
        pygame.draw.rect(self.screen, (58, 66, 72), rect, 1, border_radius=8)
        self.screen.blit(self.tiny_font.render(label, True, self.colors["muted"]), (x + 10, y + 4))
        self.screen.blit(self.small_font.render(value, True, color), (x + 76, y + 6))

    def _small_badge(self, x, y, text, color):
        img = self.tiny_font.render(text, True, (14, 18, 19))
        rect = pygame.Rect(x, y, img.get_width() + 14, 18)
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        self.screen.blit(img, (rect.x + 7, rect.y + 2))

    def _shorten(self, text, limit):
        return text if len(text) <= limit else text[: limit - 3] + "..."

    def get_card_index_at(self, position):
        for index, rect in enumerate(self.card_rects):
            if rect.collidepoint(position):
                return index
        return None


class InputHandler:
    def handle(self, event, world, renderer):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = self._start_action_at(event.pos, renderer)
            if action == "auto":
                world.choose_auto_start()
                return True
            if action == "manual":
                world.choose_manual_setup()
                return True
            if action == "start_manual":
                world.start_manual_experiment()
                return True
            if action == "back":
                world.setup_mode = None
                world.message = "실험 방식을 선택하세요."
                return True
            index = renderer.get_card_index_at(event.pos)
            if world.started and index is not None:
                world.select(index)

        if event.type == pygame.KEYDOWN:
            if not world.started:
                if event.key == pygame.K_a:
                    world.choose_auto_start()
                elif event.key == pygame.K_m:
                    world.choose_manual_setup()
                elif event.key == pygame.K_RETURN and world.setup_mode == "manual":
                    world.start_manual_experiment()
                elif event.key == pygame.K_r:
                    world.randomize()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    world.environment.select_factor(event.key - pygame.K_1)
                elif event.key == pygame.K_LEFT:
                    world.environment.adjust_selected_factor(-0.05)
                elif event.key == pygame.K_RIGHT:
                    world.environment.adjust_selected_factor(0.05)
                elif event.key == pygame.K_ESCAPE:
                    return False
                return True

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

    def _start_action_at(self, position, renderer):
        for action, rect in renderer.start_buttons.items():
            if rect.collidepoint(position):
                return action
        return None
