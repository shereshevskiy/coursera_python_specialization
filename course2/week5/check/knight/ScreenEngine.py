import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
    "green": (0, 255, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill((0, 0, 0, 255))

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        super().connect_engine(engine)

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def draw_map(self):
        min_x = 0
        min_y = 0
        ps = self.game_engine.hero.position
        size = self.game_engine.sprite_size
        if ps[0] >= 8:
            min_x = (ps[0] - 7)
        if ps[1] >= 5:
            min_y = (ps[1] - 4)
        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][
                              0], (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size

        min_x = 0
        min_y = 0
        ps = self.game_engine.hero.position
        if ps[0] >= 8:
            min_x = (ps[0] - 7)

        if ps[1] >= 5:
            min_y = (ps[1] - 4)

        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def minimap(self):
        layer = pygame.transform.scale(self.copy(), (200, 200))
        self.blit(layer, (700, -10))

    def draw(self, canvas):  # Hero position
        size = self.game_engine.sprite_size

        min_x = 0
        min_y = 0
        ps = self.game_engine.hero.position
        if ps[0] >= 8:
            min_x = (ps[0] - 7)
        if ps[1] >= 5:
            min_y = (ps[1] - 4)

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                      (obj.position[1] - min_y) * self.game_engine.sprite_size))
        self.draw_hero()
        self.minimap()
        super().draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill((60, 60, 60, 255))

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        self.fill((60, 60, 60, 255))
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.engine.hero.hp / (self.engine.hero.max_hp + 0.1), 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{round(self.engine.hero.hp)}/{self.engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))

        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score}', True, colors["black"]),
                  (550, 70))

        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill((60, 60, 60, 255))
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 20)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))
        super().draw(canvas)

    def connect_engine(self, engine):
        engine.subscribe(self)
        engine.notify("Hello!")
        engine.notify("Take chests and rings and kill enemies!")
        engine.notify("Good luck!")
        super().connect_engine(engine)


class HelpWindow(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append(["Go with short track by more score and save your HP!", ""])
        self.data.append(["Take any chest. The are any random features may be in there!", ""])
        self.data.append(["For killed the Rat you give HP and some score, but lost a few soft skills experience!", ""])
        self.data.append(["For killed the Knight you lost HP, but give more score and exp!", ""])
        self.data.append(["For killed the Naga you lost HP, but give very exp and lost score!", ""])
        self.data.append(["For killed the Dragon you give more HP, but lost more exp!", ""])
        self.data.append(["If you suffered from Thunderbolt, you lost very HP, but give biggest score and Exp!", ""])
        self.data.append(["Start from Rats and Chests!", ""])

        self.data.append(["Save more other features on your trip!", ""])
        self.data.append(["", ""])
        self.data.append([" -> ", "Move Right"])
        self.data.append([" <- ", "Move Left"])
        self.data.append([" /\ ", "Move Top"])
        self.data.append([" \/ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, (128, 128, 255)),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, (128, 128, 255)),
                          (150, 50 + 30 * i))
        super().draw(canvas)


class GameOver(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.game_over:
            alpha = 255
        self.fill((0, 0, 0, alpha))
        font = pygame.font.SysFont("courier", 80)
        font1 = pygame.font.SysFont("comicsansms", 30)
        if self.engine.game_over:
            self.blit(font.render('GAME OVER', True, (255, 0, 0, 255)), (210, 260))
            self.blit(font1.render('Press R to restart', True, (255, 0, 0, 255)), (300, 350))
        super().draw(canvas)
