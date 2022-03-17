#!/usr/bin/env python3
import sys
import math
import pygame

SCALE = 1.314
W_WIDTH = 1280
W_HEIGHT = 720
FPS_COUNT = 24
WINDOW_TITLE = "PiNezka | Author: Wasiak Florke Daniel <wasiak.daniel@gmail.com>"
WINDOW_RESOLUTION = (W_WIDTH, W_HEIGHT)

TARGET_CENTER = (W_WIDTH/2, W_HEIGHT/2)
TARGET_SIZE = 400


class Target:
    def __init__(self, center):
        self._center = center
        self._point = center[0]-TARGET_SIZE/2, center[1]-TARGET_SIZE/2
        self._width = TARGET_SIZE

    def draw(self, window):
        line_color = (200, 200, 200)

        pygame.draw.rect(window, line_color, (self._point[0], self._point[1], self._width, self._width), 2)
        pygame.draw.circle(window, line_color, self._center, self._width/2, 2)

    def is_in_rect(self, point):
        return (self._point[0] < point[0] < self._point[0] + self._width) and \
               (self._point[1] < point[1] < self._point[1] + self._width)

    def is_in_circle(self, point):
        if not self.is_in_rect(point):
            return False

        a = math.pow(self._center[0] - point[0], 2)
        b = math.pow(self._center[1] - point[1], 2)
        if math.sqrt(a + b) < self._width/2:
            return True

        return False


global TARGET
TARGET = Target(TARGET_CENTER)


def draw_checker(window):
    line_color = (30, 30, 30)

    spacing = (10 * SCALE)
    vertical_lines = W_WIDTH / spacing      # 800 / 10 = 80
    horizontal_lines = W_HEIGHT / spacing

    for i in range(int(vertical_lines)):
        x = i*spacing
        pygame.draw.line(window, line_color, (x, 0), (x, W_HEIGHT))

    for i in range(int(horizontal_lines)):
        y = i*spacing
        pygame.draw.line(window, line_color, (0, y), (W_WIDTH, y))


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

        global TARGET
        TARGET.draw(self._window)

        pygame.display.update()

    def _pygame_event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(TARGET.is_in_circle(pos))

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

