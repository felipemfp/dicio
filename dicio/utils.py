def remove_tags(str):
    """
    Retorna uma nova string sem as marcacoes do HTML

    >>> remove_tags("<a href='#'>Something</a>")
    'Something'
    """
    import re
    return re.sub('<[^>]*>', ' ', str).strip()

def text_before(str, after):
    """
    Retorna o texto antes da string after

    >>> text_before("<a href='#'>Something</a>", "</a>")
    "<a href='#'>Something"
    """
    index = str.find(after)
    if index > -1:
        return str[:index]
    return str

def text_after(str, before):
    """
    Retorna o texto depois da string before

    >>> text_after("<a href='#'>Something</a>", "<a href='#'>")
    'Something</a>'
    """
    index = str.find(before)
    if index > -1:
        index += len(before)
        return str[index:]
    return str

def text_between(str, before, after, forceHTML = False):
    """
    Retorna o texto entre as string before e after

    >>> text_between("<a href='#'>Something</a>", "<a href='#'>", "</a>")
    'Something'
    """
    start = str.find(before)
    if start > -1:
        start += len(before)
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

def remove_spaces(str):
    """
    Retorna uma nova string com todos os espaços duplos, tabulações
    e quebras de linha removidos

    >>> remove_spaces("Something  else")
    'Something else'
    """
    str = str.replace("\t", " ")
    str = str.replace("\n", " ")
    str = str.replace("\r", " ")
    while str.find("  ") > -1:
        str = str.replace("  ", " ")
    return str.strip()

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
              "ú", "ù", "û", "ü",
              "ç"]

    decode = ["a", "a", "a", "a", "a",
              "e", "e", "e", "e",
              "i", "i", "i", "i",
              "o", "o", "o", "o", "o",
              "u", "u", "u", "u",
              "c"]

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

def split_html_tag(str, tag):
    """
    Retorna split para determinada tag html dentro dos formatos possíveis

    >>> str = "Something<br>else<br />and<br/>another<br></br>thing"
    >>> split_html_tag(str, "br")
    ['Something', 'else', 'and', 'another', 'thing']
    """
    TEMPLATE = "<{0} />"
    templates = ["<{0}></{0}>",
               "<{0}></ {0}>",
               "<{0} ></{0}>",
               "<{0} ></ {0}>",
               "<{0}>",
               "<{0}/>",
               "<{0} >"]

    new_str = str
    for template in templates:
        new_str = new_str.replace(template.format(tag), TEMPLATE.format(tag))
    return list(filter(None, new_str.split(TEMPLATE.format(tag))))

if __name__ == "__main__":
    import doctest
    doctest.testmod()