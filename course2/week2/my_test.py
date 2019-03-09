import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """
    The class of 2-d vectors
    """
    def __init__(self, vector):
        self.vector = tuple(vector)

    def __str__(self):
        return f"Vec2d({self.vector[0]}, {self.vector[1]})"

    def __repr__(self):
        return f"Vec2d({self.vector[0]}, {self.vector[1]})"

    def __add__(self, other):
        """
        sum of 2th vectors
        :param other:
        :return:
        """
        x = self.vector
        if isinstance(other, (int, float)):
            k = other
            return Vec2d((x[0] + k, x[1] + k))
        else:
            y = other.vector
            return Vec2d((x[0] + y[0], x[1] + y[1]))

    def __sub__(self, other):
        """
        СЂР°Р·РЅРѕСЃС‚СЊ РґРІСѓС… РІРµРєС‚РѕСЂРѕРІ

        :param other:
        :return:
        """
        x = self.vector
        y = other.vector
        return Vec2d((x[0] - y[0], x[1] - y[1]))

    def __mul__(self, other):
        x = self.vector

        if isinstance(other, (int, float)):
            k = other
            return Vec2d((x[0] * k, x[1] * k))
        else:
            y = other.vector
            return Vec2d((x[0] * y[0], x[1] * y[1]))

    def __len__(self):
        x = self.vector
        """
        РџСЂРёРјРµС‡Р°РЅРёРµ:
        РќРµ РґРѕ РєРѕРЅС†Р° РїРѕРЅСЏС‚РЅРѕ, РёРјРµР»РѕСЃСЊ Р»Рё РІРІРёРґСѓ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РёРјРµРЅРЅРѕ СЌС‚РѕС‚ РјР°РіРёС‡РµСЃРєРёР№ РјРµС‚РѕРґ РёР»Рё РЅРµС‚.
        Р•СЃР»Рё РµРіРѕ - СЂР°Р±РѕС‚Р°С‚СЊ РЅРµ Р±СѓРґРµС‚, РїРѕСЃРєРѕР»СЊРєСѓ СЌС‚РѕС‚ РјР°РіРёС‡РµСЃРєРёР№ РјРµС‚РѕРґ РёР·РЅР°С‡Р°Р»СЊРЅРѕ РґРѕР»Р¶РµРЅ РґР°РІР°С‚СЊ С‡РёСЃР»Рѕ СЌР»РµРјРµРЅС‚РѕРІ 
        Рё РїРѕСЌС‚РѕРјСѓ РјРѕР¶РµС‚ Р±С‹С‚СЊ С‚РѕР»СЊРєРѕ С†РµР»С‹Рј. Р§С‚РѕР±С‹ РЅРµ РІС‹Р±СЂР°СЃС‹РІР°Р»РѕСЃСЊ РёСЃРєР»СЋС‡РµРЅРёРµ РїСЂРёС€Р»РѕСЃСЊ РґРѕР±Р°РІРёС‚СЊ int РІ 
        return. Р­С‚Рѕ СѓР¶Рµ РЅРµ Р±СѓРґРµС‚ РёСЃС‚РёРЅРЅРѕР№ РґР»РёРЅРЅРѕР№ РІРµРєС‚РѕСЂР°. РџРѕСЌС‚РѕРјСѓ СЂРµР°Р»РёР·РѕРІР°Р» РµС‰Рµ Рё РјРµС‚РѕРґ len(x).
        (Рђ РІРѕРѕР±С‰Рµ СЌС‚РѕС‚ РјРѕРјРµРЅС‚ РІ Р·Р°РґР°РЅРёРё РєР°РєРѕР№-С‚Рѕ СЃС‚СЂР°РЅРЅРѕРІР°С‚С‹Р№ :) )
        """
        return int(math.sqrt(x[0] * x[0] + x[1] * x[1]))

    def len(self):
        """
        Length of the vector
        :return: float
        """
        x = self.vector
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def int_pair(self):
        x = self.vector
        return int(x[0]), int(x[1])

    def distance(self, other):
        return (self - other).len()


class Polyline:
    """
    РЎlass of closed curves (polylines)
    """
    def __init__(self, steps=35, points=None, speeds=None, number=1):
        self.steps = steps
        self.points = points or []
        self.speeds = speeds or []
        self.number = number

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """
        Draw points and polyline

        :param color:
        :param width:
        :param style:
        :param points:
        :return:
        """

        if style == "line":
            for num in range(self.number):
                for p_n in range(-1, len(points) - 1):
                    pygame.draw.line(gameDisplay, color, (points[p_n] + 10*num).int_pair(),
                                     (points[p_n + 1] + 10*num).int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    def add_point(self, point, speed):
        """
        add point with his speed
        :param point:
        :param speed:
        :return:
        """
        self.points.append(point)
        self.speeds.append(speed)

    def get_point(self, points, alpha, deg=None):
        """
        polyline  smoothing
        :param alpha:
        :param deg:
        :return:
        """
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return ((points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha)))

    def get_points(self, base_points):
        count = self.steps
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def set_points(self):
        """
        Recalculation of base points coordinates
        :return:
        """
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].vector[0] > SCREEN_DIM[0] or self.points[p].vector[0] < 0:
                self.speeds[p].vector = (- self.speeds[p].vector[0], self.speeds[p].vector[1])
            if self.points[p].vector[1] > SCREEN_DIM[1] or self.points[p].vector[1] < 0:
                self.speeds[p].vector = (self.speeds[p].vector[0], -self.speeds[p].vector[1])


class Knot(Polyline):
    """
    Knot
    """
    def __init__(self, steps=35, points=None, speeds=None, number=1):
        super().__init__()
        self.steps = steps
        self.points = points or []
        self.speeds = speeds or []
        self.number = number

        self.base_points = []

    def get_knot(self):
        """
        Calculation of the curve points by the base points
        :return:
        """
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.base_points = self.get_knot()

    def set_points(self):
        super().set_points()
        self.base_points = self.get_knot()

    def get_remove_index(self, event_pos, dist=20):
        """
        index of the removing point
        :param dist:
        :param event_pos:
        :param self:
        :return:
        """
        index = None
        for i, p in enumerate(self.points):
            if event_pos.distance(p) < dist:
                index = i
        return index

    def remove_point(self, remove_index):
        """
        Remove one point from self.points and recalculate base point coordinates.
        Point for removal is got by clicking this point on the screen
        :return:
        nothing
        """
        self.points.pop(remove_index)
        self.speeds.pop(remove_index)
        # recalculations base points for polyline
        self.base_points = self.get_knot()

    def speed_change(self, param):
        self.speeds = [spd * param for spd in self.speeds]
        # recalculations base points for polyline
        self.base_points = self.get_knot()

    def speed_up(self, param=1.2):
        self.speed_change(param)

    def speed_down(self, param=0.8):
        self.speed_change(param)

    def restart(self):
        self.points = []
        self.speeds = []
        self.base_points = self.get_knot()


def draw_help(steps):
    """
    The help print
    :param steps:
    :return:
    """
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show/Help"])
    data.append(["R", "Restart"])
    data.append(['"0", "1" or ..."9"', "Set 0, 1 or ... 9 polylines"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["PgUp", "Speed up"])
    data.append(["PgDn", "Speed down"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    data.append(["", ""])
    data.append(["click near a point", "Remove the point"])
    #
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


# РћСЃРЅРѕРІРЅР°СЏ РїСЂРѕРіСЂР°РјРјР°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    knot = Knot()

    working = True
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
                    knot.restart()
                number_keys = {
                    pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
                    pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9
                }
                if event.key in number_keys:
                    knot.number = number_keys[event.key]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.steps -= 1 if knot.steps > 1 else 0
                if event.key == pygame.K_UP:
                    knot.speed_up()
                if event.key == pygame.K_DOWN:
                    knot.speed_down()

            if event.type == pygame.MOUSEBUTTONDOWN:
                event_pos = Vec2d(event.pos)
                speed = Vec2d((random.random() * 2, random.random() * 2))

                remove_index = knot.get_remove_index(event_pos)
                if remove_index is not None:
                    knot.remove_point(remove_index)
                else:
                    knot.add_point(event_pos, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points(knot.points)
        knot.draw_points(knot.base_points, "line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help(knot.steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)