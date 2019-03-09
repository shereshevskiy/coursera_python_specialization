#!/usr/bin/env python
# coding: utf-8
# автор: Чугунов Денис Валерьевич
import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __add__(self, other):
        """CСѓРјРјР° РґРІСѓС… РІРµРєС‚РѕСЂРѕРІ
        """
        return type(self)(self.start + other.start, self.end + other.end)

    def __sub__(self, other):
        """HР°Р·РЅРѕСЃС‚СЊ РґРІСѓС… РІРµРєС‚РѕСЂРѕРІ
        """
        return type(self)(self.start - other.start, self.end - other.end)

    def __mul__(self, other):
        """РЈРјРЅРѕР¶РµРЅРёРµ РІРµРєС‚РѕСЂР° РЅР° С‡РёСЃР»Рѕ
        """
        return type(self)(self.start * other, self.end * other)

    def __len__(self):
        """Р”Р»РёРЅР° РІРµРєС‚РѕСЂР°
        """
        return math.sqrt(self.start ** 2 + self.end ** 2)

    def int_pair(self):
        return (int(self.start), int(self.end))


class Polyline(object):

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self):
        """Р”РѕР±Р°РІР»РµРЅРёРµ РІ Р»РѕРјР°РЅСѓСЋ С‚РѕС‡РєРё (Vec2d) c РµС‘ СЃРєРѕСЂРѕСЃС‚СЊСЋ
        """
        self.speeds = Vec2d(object)
        self.points = Vec2d(object)
        self.points.points_vec.append(point)
        self.speeds.speeds_vec.append(speed)

    def set_points(self):
        """РџРµСЂСЃС‡РёС‚С‹РІР°РЅРёРµ РєРѕРѕСЂРґРёРЅР°С‚ РѕРїРѕСЂРЅС‹С… С‚РѕС‡РµРє
        """
        for p in range(len(self.points)):
            points[p] = add(self.points[p], self.speeds[p])
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """РћС‚СЂРёСЃРѕРІРєР° Р»РѕРјР°РЅРѕР№
        """
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, (int(self.points[p_n][0]), int(self.points[p_n][1])),
                                 (int(self.points[p_n + 1][0]), int(self.points[p_n + 1][1])), width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, (int(p[0]), int(p[1])), width)


class get_knot(Polyline):

    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))

    def get_points(base_points, count):
        alpha = 1 / count

        res = []
        for i in range(count):
            res.append(get_point(base_points, i * alpha))
        return res


def get_knot(points, count):
    def __init__(self, steps):
        Polyline.__init__(self)
        self.steps = steps

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1

    if deg == 0:
        return points[0]
    return points[deg] * alpha + self._get_point(points, alpha, deg - 1) * (1 - alpha)


def _get_points(self, base_points):
    alpha = 1 / self.steps
    res = []
    for i in range(steps.steps):
        res.append(self._get_point(base_points, i * alpha))
    return res


def _get_knot(self, points):
    self.points = []
    if len(points) < 3:
        return
    for i in range(-2, len(points) - 2):
        ptn = []
        ptn.append((points[i] + points[i + 1]) * 0.5)
        ptn.append(points[i + 1])
        ptn.append((points[i + 1] + points[i + 2]) * 0.5)

        for p in self._get_points(ptn):
            self.points.append(point)
            self.speeds.append(Vec2D((0, 0)))


def set_points(self):
    Polyline.set_points(self)
    self.get_knot()


def add_point(self, point, speed=Vec2D((0, 0))):
    Polyline.set_points(self, point, speed)
    self._get_knot()


if __name__ == "__main__":
    """РћСЃРЅРѕРІРЅР°СЏ РїСЂРѕРіСЂР°РјРјР°
    """
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        draw_points(points)
        draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            set_points(points, speeds)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
