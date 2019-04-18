from abc import ABC, abstractmethod


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display):
        pass


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):
    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_hp()
        self.hp = self.max_hp

    def calc_max_hp(self):
        self.max_hp = 5+ self.stats["endurance"] * 2


class Enemy(Creature, Interactive):
    def __init__(self, name, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp
        self.name = name

    def interact(self, engine, hero):
        if self.name == "rat":
            hero.hp += 5
            hero.exp -= 10
            engine.score += 20
            engine.notify(f"+ hp & score. - exp. You killed a {self.name}. More Extreme!")

        if self.name == "knight":
            hero.hp -= 20
            hero.exp += 10
            engine.score += 20
            engine.notify(f"-- hp. ++ exp & score. You killed a {self.name}")

        if self.name == "naga":
            hero.hp -= 15
            hero.exp += 20
            engine.score -= 20
            engine.notify(f"-- hp & score. ++ exp. You killed a {self.name}. More Extreme!")

        if self.name == "gragon":
            hero.hp += 25
            hero.exp -= 25
            engine.notify(f"-- hp. ++ exp. You killed a {self.name}")

        if self.name == "thunderbolt":
            hero.hp -= 40
            hero.exp += 40
            engine.score += 100
            engine.notify(f"---hp. +++ exp & score. {self.name}")


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.prop_exp = 0
        self.prop_hp = 45
        self.max_hp = self.prop_hp
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self, engine):
        if self.exp >= 100 * (2 ** (self.level - 1)):
            engine.notify("Level up!")
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_hp()
            self.hp = self.max_hp

    def draw(self, display):
        min_x = 0
        min_y = 0
        ps = self.position
        if ps[0] >= 8:
            min_x = (ps[0] - 7)
        if ps[1] >= 5:
            min_y = (ps[1] - 4)
        display.blit(self.sprite, [(ps[0] - min_x) * display.game_engine.sprite_size,
                                   (ps[1] - min_y) * display.game_engine.sprite_size]
                     )

    @property
    def hp(self):
        return self.prop_hp

    @hp.setter
    def hp(self, value):
        if value > self.max_hp:
            self.prop_hp = self.max_hp
        else:
            if value < 0:
                self.prop_hp = 0
            else:
                self.prop_hp = value

    @property
    def exp(self):
        return self.prop_exp

    @exp.setter
    def exp(self, value):
        self.prop_exp = value if value > 0 else 0


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats["strength"] += 3
        self.stats["endurance"] += 3
        self.stats["luck"] -= 1
        self.stats["intelligence"] -= 3


class Blessing(Effect):
    def apply_effect(self):
        self.stats["luck"] += 3
        self.stats["intelligence"] += 3


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 3
        self.stats["endurance"] -= 3


class Happy(Effect):
    def apply_effect(self):
        self.stats["strength"] += 5
        self.stats["endurance"] += 5
        self.stats["luck"] += 5
        self.stats["intelligence"] += 5



