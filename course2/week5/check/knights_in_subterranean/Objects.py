from abc import ABC, abstractmethod
import random


class AbstractObject(ABC):
    def __init__(self, icon, position):
        self.position = position
        self.icon = icon

    def draw(self, display):
        display.blit(self.icon, self.position)


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.icon = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.icon = icon
        self.stats = stats
        self.position = position
        self.max_hp = self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        return 5 + self.stats["endurance"] * 2


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = None
        self.level = 1
        self.exp = 0
        self.max_exp = self.calc_max_exp()
        self.gold = 0
        super().__init__(icon, stats, pos)

    def calc_max_exp(self):
        return 100*(2**(self.level-1))

    def level_up(self, exp, engine):
        if self.exp + exp >= self.max_exp:
            engine.notify("level up!")
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.exp = self.exp + exp - self.max_exp
            self.max_exp = self.calc_max_exp()
            self.max_hp = self.calc_max_HP()
            self.hp = self.max_hp

        else:
            self.exp += exp


class Enemy(Creature):
    def __init__(self, icon, stats, position):
        super().__init__(icon, stats, position)
        self.roulette = self.stats['luck'] * [1] + [0] * 5
        print(self.stats)

    def interact(self, engine, hero):
        while hero.hp > 0 and self.hp > 0:
            roulette = [1] * hero.stats['luck'] + [0] * 5
            if random.choice(roulette) == 1:
                self.hp -= hero.stats['strength']
                engine.notify('You hit the {}!'.format(self.stats['name']))
            elif random.choice(self.roulette):
                hero.hp -= self.stats['strength']
                engine.notify('The {} hit you!'.format(self.stats['name']))
        if hero.hp > 0:
            print('win!')
            hero.level_up(self.stats['experience'], engine)
        else:
            engine.notify('Game over')
            engine.game_process = False


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
    def max_exp(self):
        return self.base.max_exp

    @max_exp.setter
    def max_exp(self, value):
        self.base.max_exp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def icon(self):
        return self.base.icon

    @abstractmethod
    def apply_effect(self):
        pass


class Blessing(Effect):
    def apply_effect(self):
        for key in self.stats:
            self.stats[key] += 1
        print(self.stats)


class Coursera(Effect):
    def apply_effect(self):
        self.stats['intelligence'] += 1
        print(self.stats)


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5
        self.stats['intelligence'] -= 1
        print(self.stats)


class Weakness(Effect):
    def apply_effect(self):
        for key in self.stats:
            self.stats[key] -= 1
        print(self.stats)



