import pygame

from config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from visualization import InputHandler, Renderer
from world import World


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("수학적 바이오모프 곤충 모형")

    clock = pygame.time.Clock()
    world = World()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not input_handler.handle(event, world, renderer):
                running = False

        world.update()
        renderer.draw(world)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
