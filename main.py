# -*- coding: utf-8 -*-

import pygame

from config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from visualization import InputHandler, Renderer
from world import World


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("환경 변화 적응 진화 시뮬레이터")

    clock = pygame.time.Clock()
    world = World()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True
    fullscreen = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                fullscreen = not fullscreen
                pygame.display.toggle_fullscreen()
                continue

            if event.type == pygame.MOUSEWHEEL:
                renderer.gallery_scroll_x = max(0, renderer.gallery_scroll_x + event.x * 30 - event.y * 30)
                continue

            if not input_handler.handle(event, world, renderer):
                running = False

        world.update()
        renderer.draw(world)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
