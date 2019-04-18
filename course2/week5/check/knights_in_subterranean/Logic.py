import Service


class GameEngine:
    def __init__(self, sprite_size=11):
        self.sprite_size = sprite_size
        self.objects = []
        self.map = None
        self.map_size = (0, 0)
        self.hero = None
        self.level = -1
        self.working = True
        self.subscribers = set()
        self.score = 0.
        self.game_process = True
        self.show_help = False
        self.show_minimap = False

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
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if self.show_minimap or self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position = [self.hero.position[0], self.hero.position[1] - 1]
        self.interact()

    def move_down(self):
        self.score -= 0.02
        if self.show_minimap or self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position = [self.hero.position[0], self.hero.position[1] + 1]
        self.interact()

    def move_left(self):
        self.score -= 0.02
        if self.show_minimap or self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position = [self.hero.position[0] - 1, self.hero.position[1]]
        self.interact()

    def move_right(self):
        self.score -= 0.02
        if self.show_minimap or self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position = [self.hero.position[0] + 1, self.hero.position[1]]
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map
        self.map_size = (len(game_map[0]), len(game_map))

    def change_scale(self, add):
        self.sprite_size += add

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
