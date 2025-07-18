_LATIN_DIGRAPHS = {
    'sh': 'ш', 'ch': 'ч', 'ya': 'я', 'yu': 'ю', 'yo': 'ё', "o'": 'ў', "g'": 'ғ'}

_LATIN_SINGLE = {
    'a': 'а', 'b': 'б', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г',
    'h': 'ҳ', 'i': 'и', 'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м',
    'n': 'н', 'o': 'о', 'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с',
    't': 'т', 'u': 'у', 'v': 'в', 'x': 'х', 'y': 'й', 'z': 'з'
}

_CYRILLIC_TO_LATIN = {v: k for k, v in {**_LATIN_DIGRAPHS, **_LATIN_SINGLE}.items()}


def latin_to_cyrillic(text):
    t = text.lower()
    for dg, c in _LATIN_DIGRAPHS.items():
        t = t.replace(dg, c)
    for l, c in _LATIN_SINGLE.items():
        t = t.replace(l, c)
    return t


def cyrillic_to_latin(text):
    t = text.lower()
    for cyr, lat in _CYRILLIC_TO_LATIN.items():
        t = t.replace(cyr, lat)
    return t
