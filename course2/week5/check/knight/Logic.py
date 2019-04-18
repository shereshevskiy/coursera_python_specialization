import Service
import random


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0
    game_process = True
    show_help = False
    game_over = False

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        self.score -= 1
        if random.randint(0, 3) == 2:
            self.hero.hp = self.hero.hp - 1
            self.hero.exp -= 1
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)
                if self.hero.hp <= 0:
                    self.game_over = not self.game_over
                    self.game_process = False

    def move_up(self):
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] -= 1
        self.interact()
        if self.hero.exp >= 100 * (2 ** (self.level - 1)):
            self.hero.level_up(self)

    def move_down(self):
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] += 1
        self.interact()
        if self.hero.exp >= 100 * (2 ** (self.level - 1)):
            self.hero.level_up(self)

    def move_left(self):
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position[0] -= 1
        self.interact()
        if self.hero.exp >= 100 * (2 ** (self.level - 1)):
            self.hero.level_up(self)

    def move_right(self):
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()
        if self.hero.exp >= 100 * (2 ** (self.level - 1)):
            self.hero.level_up(self)

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
