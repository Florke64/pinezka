#!/usr/bin/env python3
import sys
import math
import random
import pygame

SCALE = 1.314
W_WIDTH = 800
W_HEIGHT = 600
FPS_COUNT = 24
WINDOW_TITLE = "PiNezka | Author: Wasiak Florke Daniel <wasiak.daniel@gmail.com>"
WINDOW_RESOLUTION = (W_WIDTH, W_HEIGHT)

TARGET_CENTER = (int(W_WIDTH/2), int(W_HEIGHT/2))
TARGET_SIZE = int(W_HEIGHT - (0.314 * W_HEIGHT))

BATCH_SHOTS = 218

SHOTS = 0
SHOTS_IN_RECT = 0
SHOTS_IN_CIRCLE = 0

global CALCULATED_PI
CALCULATED_PI = math.pi


def update_pi():
    global CALCULATED_PI
    CALCULATED_PI = (SHOTS_IN_CIRCLE / (SHOTS_IN_RECT+SHOTS_IN_CIRCLE)) * 4


global SHOT_POINTS
SHOT_POINTS = []


def clear_shots():
    global SHOT_POINTS, SHOTS, SHOTS_IN_RECT, SHOTS_IN_CIRCLE
    SHOT_POINTS.clear()
    SHOTS = SHOTS_IN_RECT = SHOTS_IN_CIRCLE = 0


class Target:
    def __init__(self, center):
        self._center = center
        self._point = int(center[0]-TARGET_SIZE/2), int(center[1]-TARGET_SIZE/2)
        self._width = TARGET_SIZE

    def draw(self, window):
        line_color = (200, 200, 200)

        pygame.draw.rect(window, line_color, (self._point[0], self._point[1], self._width, self._width), 1)
        pygame.draw.circle(window, line_color, self._center, self._width/2, 1)

    def is_in_rect(self, point):
        return (self._point[0] <= point[0] <= self._point[0] + self._width) and \
               (self._point[1] <= point[1] <= self._point[1] + self._width)

    def is_in_circle(self, point):
        if not self.is_in_rect(point):
            return False

        a = math.pow(self._center[0] - point[0], 2)
        b = math.pow(self._center[1] - point[1], 2)
        if math.sqrt(a + b) <= self._width/2:
            return True

        return False

    @property
    def point(self):
        return self._point

    @property
    def width(self):
        return self._width


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


def draw_shots(window):
    for shot in SHOT_POINTS:
        point = shot[0]

        if shot[1] == 2:
            color = (0, 255, 0)
        elif shot[1] == 1:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        pygame.draw.circle(window, color, point, 1)


def draw_text(window):
    font_size = 14
    font = pygame.font.SysFont("Arial", font_size)
    font_color = (177, 177, 177)

    result = font.render("Calculated Pi Number: " + str(CALCULATED_PI), True, (255, 255, 255))
    window.blit(result, (TARGET.point[0], TARGET.point[1] + TARGET.width + font_size * 2))

    inside = font.render("Inside of the target: " + str(SHOTS_IN_CIRCLE), True, (70, 220, 70))
    outside = font.render("Outside of the target: " + str(SHOTS_IN_RECT), True, (70, 70, 220))
    window.blit(inside, (TARGET.point[0] + TARGET.width + font_size, TARGET.point[1] + font_size * 2))
    window.blit(outside, (TARGET.point[0] + TARGET.width + font_size, TARGET.point[1] + font_size * 4))

    project = font.render("Project's website: https://github.com/FlrQue/pinezka", True, font_color)
    video_link = font.render("Inspired by: https://www.youtube.com/watch?v=aKyzxK7Wj0o", True, font_color)
    video_title = font.render("\"Dwulatek vs komputer - kto lepiej wyznaczy liczbę pi?\" by Uwaga! Naukowy Bełkot", True, font_color)
    window.blit(project, (font_size, font_size * 1 * 1.1))
    window.blit(video_link, (font_size, font_size * 2 * 1.1))
    window.blit(video_title, (font_size, font_size * 3 * 1.1))

    license = font.render("Created by Daniel Wasiak | Licensed under the MIT license", True, font_color)
    window.blit(license, (font_size, W_HEIGHT - font_size * 2 * 1.1))


def random_shot():
    rand_point = random.randrange(TARGET.point[0] + 1, TARGET.point[0] + TARGET.width), \
                 random.randrange(TARGET.point[1] + 1, TARGET.point[1] + TARGET.width)

    global SHOTS
    SHOTS += 1

    if TARGET.is_in_circle(rand_point):
        magic_number = 2

        global SHOTS_IN_CIRCLE
        SHOTS_IN_CIRCLE += 1

    elif TARGET.is_in_rect(rand_point):
        magic_number = 1

        global SHOTS_IN_RECT
        SHOTS_IN_RECT += 1

    else:
        magic_number = 0

    global SHOT_POINTS
    SHOT_POINTS.append((rand_point, magic_number))


class PiNezka:
    def __init__(self):
        global INSTANCE
        INSTANCE = self

        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._window: pygame.Surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

        pygame.display.set_caption(WINDOW_TITLE)

    def init_app(self):
        pygame.font.init()
        # for i in range(50000):
        #     random_shot()

        pass

    def update(self):
        self._pygame_event_handler()

    def draw(self):
        self._window.fill((0, 0, 0))

        # cosmetic aspect of the background
        draw_checker(self._window)

        draw_shots(self._window)

        global TARGET
        TARGET.draw(self._window)

        draw_text(self._window)

        pygame.display.update()

    def _pygame_event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            if event.type == pygame.MOUSEBUTTONUP:
                # pos = pygame.mouse.get_pos()
                # random_shot()

                if event.button not in (1, 3):
                    return

                if event.button == 3:
                    clear_shots()

                for i in range(BATCH_SHOTS):
                    random_shot()
                    update_pi()

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

