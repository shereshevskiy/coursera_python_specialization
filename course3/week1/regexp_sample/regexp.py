def calculate(data, findall):
    regexp = r"([abc])([+-]?=)([abc]?)([+-]?\d+)?"
    matches = findall(regexp)  # Если придумать хорошую регулярку, будет просто
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        if s == "=":
            # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
            data[v1] = data.get(v2, 0) + int(n or 0)
        if s == "-=":
            data[v1] -= data.get(v2, 0) + int(n or 0)
        if s == "+=":
            data[v1] += data.get(v2, 0) + int(n or 0)

    return data


# решение от преподавателей
"""
def calculate(data, findall):
    matches = findall(r"([abc])([+-]?)=([abc])?([+-]?\d+)?")
    for a, sign, b, number in matches:
        right = data.get(b, 0) + int(number or 0)
        if sign == "-":
            data[a] -= right
        elif sign == "+":
            data[a] += right
        else:
            data[a] = right
    return data
"""
