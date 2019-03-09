# автор: Новичкова Анастасия Ивановна

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, x_or_pair, y=None, speed=0):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
        self.speed = speed

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vec2d(self.x * other, self.y * other)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def int_pair(self):
        return self.x, self.y


class Polyline:

    def __init__(self):
        self.points = list()

    def add_point(self, point):
        self.points.append(point)

    def delete_point(self, point=None):
        if point == None:
            self.points.pop()
        else:
            self.points.remove(point)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] * self.points[p].speed
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.points[p].speed = (- self.points[p].speed[0], self.points[p].speed[1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.points[p].speed = (self.points[p].speed[0], -self.points[p].speed[1])

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)


class Knot(Polyline):
    Knots = []

    def __init__(self, count):
        super().__init__()
        self.count = count
        Knot.Knots.append(self)

    def add_point(self, point):
        super().add_point(point)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def delete_point(self, point=None):
        super().delete_point(point)
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * 0.5, self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * 0.5]
            res.extend(self.get_points(ptn))
        return res

    @staticmethod
    def delete_points_from_curves():
        for _knot in Knot.Knots:
            for arg in args:
                _knot.delete_point(arg)

    @staticmethod
    def add_points_to_curves():
        for _knot in Knot.Knots:
            for arg in args:
                _knot.add_point(arg)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)


# РћС‚СЂРёСЃРѕРІРєР° СЃРїСЂР°РІРєРё
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"], ["Num+", "More points"],
            ["Num-", "Less points"], ["", ""], [str(steps), "Current points"]]
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# РћСЃРЅРѕРІРЅР°СЏ РїСЂРѕРіСЂР°РјРјР°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    steps = 35
    working = True
    polyline = Polyline()
    knot = Knot(steps)
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
                    polyline = Polyline()
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.add_point(Vec2d(event.pos, speed=Vec2d(random.random() * 2, random.random() * 2)))
                knot.add_point(Vec2d(event.pos, speed=Vec2d(random.random() * 2, random.random() * 2)))
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points(polyline.points)
        knot.draw_points(knot.get_knot(), 3, color)
        if not pause:
            polyline.set_points()
            knot.set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)