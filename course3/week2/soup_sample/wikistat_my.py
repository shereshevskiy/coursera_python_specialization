from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path), False)  # Словарь вида {"filename1": None, "filename2": None, ...}
    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    current_links = [start]
    while current_links:
        new_links = []
        for name in current_links:
            with open("{}{}".format(path, name), encoding="utf-8") as data:
                links = re.findall(link_re, data.read())
            for link in links:
                if files.get(link) is False:
                    files[link] = name
                    if link == end:
                        return files
                    new_links.append(link)
        current_links = new_links


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []
    # TODO Добавить нужные страницы в bridge
    current_link, bridge = end, [end]
    while current_link != start:
        current_link = files[current_link]
        bridge.append(current_link)
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]
    # bridge = [start, end]  # TODO to look for the all list from start to end

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file), encoding="utf-8") as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        # imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        # imgs = len([item["width"] for item in body.find_all(name="img") if int(item["width"] or 0) >= 200])
        imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
        # headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        # headers = len([item.text for item in body.find_all(name=re.compile(r"h[1-6]"), text=re.compile(r"[ETC][\w()/]+"))])
        headers = len([item.text for item in body.find_all(name=re.compile(r"h[1-6]")) if item.text[0] in ["E", "T", "C"]])

        # linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        raw_items_a = [a_item.find_next_siblings() for a_item in body.find_all("a")]
        length_list = []
        for raw_item in raw_items_a:
            a_list = [item.name for item in raw_item]
            # разбиваем каждый item по "не а" и вычисляем длину каждой части (добавляем единицу за счет самой точки,
            # от которой считаем)
            local_length_list = [len(token) + 1 for token in
                                 ("".join([item if item == "a" else " " for item in a_list])).split(" ")]
            length_list.extend(local_length_list) # собираем все это в список
        linkslen = max(length_list)

        # lists = 20  # Количество списков, не вложенных в другие списки
        ul_ol_lists = body.find_all(["ul", "ol"])
        lists = [{"ul", "ol"}.isdisjoint({item.name for item in lst.find_parents()}) for lst in ul_ol_lists].count(True)

        out[file] = [imgs, headers, linkslen, lists]
        print(out)

    return out
