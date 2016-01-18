def remove_tags(str):
    """
    Retorna uma nova string sem as marcacoes do HTML

    >>> remove_tags("<a href='#'>Something</a>")
    'Something'
    """
    import re
    return re.sub('<[^>]*>', '', str)

def text_between(str, before, after, forceHTML = False):
    """
    Retorna o texto entre as string before e after

    >>> text_between("<a href='#'>Something</a>", "<a href='#'>", "</a>")
    'Something'
    """
    start = str.find(before) + len(before)
    if forceHTML:
        if before[-1] != ">":
            start = str.find(">", start) + 1
    end = str.find(after, start)
    if forceHTML:
        if after[0] != "<":
            end = str.find("<", start)
    if -1 < start < end:
        return str[start:end]
    return str

def remove_accents(str):
    """
    Retorna uma nova string sem os acentos da lingua portuguesa

    >>> remove_accents("trava-língua")
    'trava-lingua'
    """
    encode = ["á", "à", "â", "ã", "ä",
              "é", "è", "ê", "ë",
              "í", "ì", "î", "ï",
              "ó", "ò", "ô", "õ", "ö",
              "ú", "ù", "û", "ü"]

    decode = ["a", "a", "a", "a", "a",
              "e", "e", "e", "e",
              "i", "i", "i", "i",
              "o", "o", "o", "o", "o",
              "u", "u", "u", "u"]

    out = ""
    found = False

    for chr in str:
        for x, vgl in enumerate(encode):
            if chr == vgl:
                out += decode[x]
                found = True
                break
            else:
                found = False
        if not found:
            out += chr

    return out

if __name__ == "__main__":
    import doctest
    doctest.testmod()