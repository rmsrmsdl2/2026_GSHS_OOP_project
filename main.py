import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from world import World
from visualization import Renderer, InputHandler


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Biomorph Evolution Simulation")

    clock = pygame.time.Clock()
    world = World()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not input_handler.handle(event, world):
                running = False

        world.update()
        renderer.draw(world)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()