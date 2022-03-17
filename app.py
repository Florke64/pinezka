#!/usr/bin/env python3
import sys
import pygame

SCALE = 2
W_WIDTH = 800
W_HEIGHT = 600
FPS_COUNT = 24
WINDOW_TITLE = "PiNezka by Wasiak Florke Daniel <wasiak.daniel@gmail.com>"
WINDOW_RESOLUTION = (W_WIDTH, W_HEIGHT)


def draw_checker(window):
    line_color = (30, 30, 30)

    spacing = (10 * SCALE)
    vertical_lines = W_WIDTH / spacing      # 800 / 10 = 80
    horizontal_lines = W_HEIGHT / spacing

    for i in range(int(vertical_lines)):
        x = i*spacing
        pygame.draw.line(window, line_color, (x, 0), (x, 600))

    for i in range(int(horizontal_lines)):
        y = i*spacing
        pygame.draw.line(window, line_color, (0, y), (800, y))


class PiNezka:
    def __init__(self):
        global INSTANCE
        INSTANCE = self

        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._window: pygame.Surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

        pygame.display.set_caption(WINDOW_TITLE)

    def init_app(self):
        pass

    def update(self):
        self._pygame_event_handler()

    def draw(self):
        self._window.fill((0, 0, 0))

        # cosmetic aspect of the background
        draw_checker(self._window)

        pygame.display.update()

    def _pygame_event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def mainloop(self):
        while self._running:
            self._clock.tick(FPS_COUNT)

            self.update()
            self.draw()

        pygame.quit()
        sys.exit(0)


global INSTANCE
INSTANCE: PiNezka

if __name__ == "__main__":
    INSTANCE = PiNezka()
    INSTANCE.init_app()
    INSTANCE.mainloop()

    sys.exit(1)

