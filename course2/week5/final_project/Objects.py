from abc import ABC, abstractmethod

import numpy as np
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):

    def __init__(self):
        self.sprite = None
        self.position = None
        self.min_x = 0
        self.min_y = 0

    def draw(self, display):
        sprite_size = self.sprite.get_size()[0]
        display.blit(self.sprite, [(self.position[0] - self.min_x) * sprite_size,
                                   (self.position[1] - self.min_y) * sprite_size])



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
        old_stats = hero.stats

        self.action(engine, hero)

        engine.notify("The interaction with Ally")
        engine.notify("   The changes in status:")
        for stat in hero.stats:
            engine.notify(f"{stat}: from {old_stats[stat]} to {engine.hero.stats[stat]}")
        engine.notify("****************")



class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2



class Hero(Creature):

    def __init__(self, stats, icon):
        position = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, position)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            # yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        self.xp = xp
        super().__init__(icon, stats, position)

    def interact(self, engine, hero):

        engine.notify("The interaction with Enemy")
        engine.notify("   The changes in status:")
        old_stat = hero.stats.copy()

        hero_stats_sum = np.sum(list(hero.stats.values()))
        enemy_stats_sum = np.sum([self.stats[stat] for stat in hero.stats])
        if hero_stats_sum >= enemy_stats_sum:
            for stat in hero.stats:
                hero.stats[stat] += int(self.stats[stat] / 1.5)
                hero.exp += self.xp
        else:
            for stat in hero.stats:
                hero.stats[stat] //= 2

        for stat in hero.stats:
            engine.notify(f"{stat}: from {old_stat[stat]} to {hero.stats[stat]}")
        engine.notify("****************")
        hero.level_up()


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
        for stat in ["strength", "endurance", "luck"]:
            self.stats[stat] += 7
        self.stats["intelligence"] -= 3


class Blessing(Effect):
    def apply_effect(self):
        for stat in self.stats:
            self.stats[stat] += 2


class Weakness(Effect):
    def apply_effect(self):
        for stat in ["strength", "endurance"]:
            self.stats[stat] -= 7


class RemoveEvilEye(Effect):
    def apply_effect(self):
        self.stats["luck"] += 10

