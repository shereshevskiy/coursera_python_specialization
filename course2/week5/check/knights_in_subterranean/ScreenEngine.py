import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            self.resolution = args[0]
            self.sprites_in_frame = None
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args)
        self.game_engine = None

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):
    def __init__(self, *args):
        super().__init__(*args)
        self.constant_offset = (0, 0)
        self.sprites_in_frame = (0, 0)
        self.sprite_size = (0, 0)
        self.size = 0  # normal icon size

    def connect_engine(self, engine):
        self.sprite_size = engine.sprite_size
        self.sprites_in_frame = (self.resolution[0] // engine.sprite_size,
                                 self.resolution[1] // engine.sprite_size)
        self.constant_offset = (self.sprites_in_frame[0] * engine.sprite_size // 2,
                                self.sprites_in_frame[1] * engine.sprite_size // 2)
        super().connect_engine(engine)

    def draw_hero(self):
        self.blit(self.game_engine.hero.icon[self.size], self.constant_offset)

    def draw_map(self):
        if self.game_engine.show_minimap:
            self.fill((0, 0, 0, 128))
        else:
            self.fill(colors["black"])
        for i in range(self.game_engine.map_size[0]):
            for j in range(self.game_engine.map_size[1]):
                # print(self.game_engine.map)
                self.draw_object(self.game_engine.map[j][i], (i, j))

    def draw_object(self, sprite, coord):
        self.blit(sprite[self.size], ((coord[0]-self.game_engine.hero.position[0]) *
                                      self.sprite_size + self.constant_offset[0],
                                      (coord[1]-self.game_engine.hero.position[1]) *
                                      self.sprite_size + self.constant_offset[1]))

    def draw(self, canvas):
        self.draw_map()
        for obj in self.game_engine.objects:
            self.draw_object(obj.icon, obj.position)
        self.draw_hero()
        if not self.game_engine.game_process:
            self.blit(pygame.font.SysFont("comicsansms", 140).render('GAME OVER', True, colors["red"]),
                      (20, 200))
        super().draw(canvas)


class MiniMap(GameSurface):
    def connect_engine(self, engine):
        self.game_engine = engine
        self.size = 1  # mini icon
        self.sprite_size = 17
        self.successor.connect_engine(engine)

    def draw_hero(self):
        self.blit(self.game_engine.hero.icon[self.size],
                  (self.game_engine.hero.position[0] * self.sprite_size,
                   self.game_engine.hero.position[1] * self.sprite_size))

    def draw_object(self, sprite, coord):
        self.blit(sprite[self.size], (coord[0] *
                                      self.sprite_size,
                                      coord[1] *
                                      self.sprite_size))

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_minimap:
            alpha = 128
        self.fill((255, 255, 255, alpha))
        if self.game_engine.show_minimap:
            super().draw(canvas)

        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)


class ProgressBar(ScreenHandle):
    def __init__(self, *args):
        super().__init__(*args)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors["red"],
                         (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.game_engine.hero.exp /
                                                 (100 * (2**(self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}',
                              True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.game_engine.hero.exp}/{self.game_engine.hero.max_exp}',
                              True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (550, 70))
        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args):
        super().__init__(*args)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])

        font = pygame.font.SysFont("comicsansms", 20)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))
        super().draw(canvas)

    def connect_engine(self, engine):
        engine.subscribe(self)
        super().connect_engine(engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args):
        super().__init__(*args)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append([" M ", "Show Mini-map"])
        self.data.append([" O ", "Zoom +"])
        self.data.append([" I ", "Zoom -"])
        self.data.append([" R ", "Restart Game"])

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        if self.game_engine.show_help:
            font1 = pygame.font.SysFont("courier", 24)
            font2 = pygame.font.SysFont("serif", 24)
            pygame.draw.lines(self, colors['white'], True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))
        # super().draw(canvas)
