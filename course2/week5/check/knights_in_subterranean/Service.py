import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    sprites = []
    for size in (sprite_size, 17):
        icon = pygame.transform.scale(icon, (size, size))
        sprite = pygame.Surface((size, size), pygame.HWSURFACE)
        sprite.blit(icon, (0, 0))
        sprites.append(sprite)
    return sprites


def reload_game(engine, hero):
    service_init(engine.sprite_size)
    level_list = load_levels()
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    generator = level_list[engine.level]
    _map = generator['map'].get_map()
    engine.load_map(_map)
    engine.add_hero(hero)
    engine.add_objects(generator['obj'].get_objects(_map))


def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


def intelligence_boost(engine, hero):
    hero.gold -= int(20 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
    engine.hero = Objects.Coursera(hero)
    engine.notify('You are smarter now')


def apply_blessing(engine, hero):
    if hero.gold >= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(hero)
            engine.notify("Blessing applied")
        else:
            engine.hero = Objects.Berserk(hero)
            engine.notify("Berserk applied")
    else:
        engine.notify('Not enough gold')
        engine.score -= 0.1


def remove_effect(engine, hero):
    if hero.gold >= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_HP()
        engine.notify("Effect removed")


def add_gold(engine, hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(hero)
        engine.notify("You were cursed")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")


class MapFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        _map = cls.Map()
        _obj = cls.Objects()
        _obj.config = data
        return {'map': _map, 'obj': _obj}

    @staticmethod
    def get_vacant(_map):
        _vacant = set()
        for i in range(1, len(_map)-1):
            for j in range(1, len(_map)-1):
                if _map[i][j] != wall:
                    _vacant.add((j, i))
        _vacant -= {(1, 1), (1, 2), (2, 1), (2, 2)}
        return _vacant

    @staticmethod
    def generate_template(map_size, empty=False):
        landscape = [floor1, floor2, floor3] if empty else \
            [wall, floor1, floor2, floor3, floor1, floor2, floor3, floor1, floor2, floor3]
        map_border = [0, map_size - 1]
        new_map = [[0 for _ in range(map_size)] for _ in range(map_size)]
        for i in range(map_size):
            for j in range(map_size):
                if i in map_border or j in map_border:
                    new_map[i][j] = wall
                else:
                    new_map[i][j] = random.choice(landscape)
        return new_map


class EndMap(MapFactory):
    yaml_tag = '!end_map'

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else floor1
         
        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:
        def __init__(self):
            self.Map = MapFactory.generate_template(map_size=25)

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):

            vacant = MapFactory.get_vacant(_map)
            for key in ['objects', 'ally']:
                for obj_name in object_list_prob[key]:
                    prop = object_list_prob[key][obj_name]
                    for i in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = random.choice(tuple(vacant))
                        self.objects.append(Objects.Ally(
                            prop['sprite'], prop['action'], coord))
                        vacant.remove(coord)

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 2)):
                    coord = random.choice(tuple(vacant))
                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, coord))
                    vacant.remove(coord)

            return self.objects


class EmptyMap(MapFactory):
    yaml_tag = '!empty_map'

    class Map:
        def __init__(self):
            self.Map = MapFactory.generate_template(map_size=11, empty=True)
            self.Map[5][5] = wall
            self.Map[5][6] = wall
            self.Map[5][7] = wall
            self.Map[9][9] = wall

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            stairs = object_list_prob['objects']['stairs']
            chest = object_list_prob['objects']['chest']
            npc = object_list_prob['ally']['bless']
            npc_r = object_list_prob['ally']['coursera']
            self.objects.append(Objects.Ally(
                stairs['sprite'], stairs['action'], (3, 2)))
            self.objects.append(Objects.Ally(
                chest['sprite'], chest['action'], (3, 1)))
            self.objects.append(Objects.Ally(
                npc['sprite'], npc['action'], (5, 1)))
            self.objects.append(Objects.Ally(
                npc_r['sprite'], npc_r['action'], (6, 1)))
            return self.objects


class SpecialMap(MapFactory):
    yaml_tag = '!special_map'

    class Map:
        def __init__(self):
            self.Map = MapFactory.generate_template(map_size=16)

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            vacant = MapFactory.get_vacant(_map)
            for key in ['objects', 'ally']:

                for obj_name in object_list_prob[key]:
                    prop = object_list_prob[key][obj_name]
                    for i in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = random.choice(tuple(vacant))
                        self.objects.append(Objects.Ally(
                            prop['sprite'], prop['action'], coord))
                        vacant.remove(coord)

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                prop.update({'name': obj_name})
                for i in range(random.randint(0, 5)):
                    coord = random.choice(tuple(vacant))
                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, coord))
                    vacant.remove(coord)

            return self.objects


wall = [0, 0]
floor1 = [0, 0]
floor2 = [0, 0]
floor3 = [0, 0]


def service_init(sprite_size, full=True):
    global object_list_prob

    global wall
    global floor1
    global floor2
    global floor3

    wall = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1 = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2 = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3 = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    with open("objects.yml", "r") as file:

        object_list_tmp = yaml.load(file.read())
        if full:
            object_list_prob = object_list_tmp

        object_list_actions = {'reload_game': reload_game,
                               'add_gold': add_gold,
                               'apply_blessing': apply_blessing,
                               'remove_effect': remove_effect,
                               'intelligence_boost': intelligence_boost,
                               'restore_hp': restore_hp}

        for obj in object_list_prob['objects']:
            prop = object_list_prob['objects'][obj]
            prop_tmp = object_list_tmp['objects'][obj]
            prop['sprite'] = create_sprite(
                os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
            prop['action'] = object_list_actions[prop_tmp['action']]

        for ally in object_list_prob['ally']:
            prop = object_list_prob['ally'][ally]
            prop_tmp = object_list_tmp['ally'][ally]
            prop['sprite'] = create_sprite(
                os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
            prop['action'] = object_list_actions[prop_tmp['action']]

        for enemy in object_list_prob['enemies']:
            prop = object_list_prob['enemies'][enemy]
            prop_tmp = object_list_tmp['enemies'][enemy]
            prop['sprite'] = create_sprite(
                os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)


def load_levels():
    with open("levels.yml", "r") as file:
        level_list = yaml.load(file.read())['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
    return level_list
