"""
Python API não oficial para Dicio.com.br

@autor Felipe Pontes
@email felipemfpontes@gmail.com
"""

import html
from urllib import request
from utils import *

BASE_URL = "http://www.dicio.com.br/{}"
CHARSET = "iso-8859-1"
TAG_MEANING = ("id=\"significado\"", "</p>")
TAG_SYNONYMS = ("class=\"adicional sinonimos\"", "</p>")
TAG_SYNONYMS_DELIMITER = ("<a", "</a>")
TAG_ENCHANT = ("id=\"enchant\"", "</div>")
TAG_EXTRA = ("class=\"adicional\"", "</p>")
TAG_EXTRA_SEP = "br"
TAG_EXTRA_DELIMITER = ("<b>", "</b>")

class Word(object):
    def __init__(self, word, meaning = None, synonyms = [], extra = {}):
        self.word = word
        self.url = BASE_URL.format(remove_accents(word).strip().lower())
        self.meaning = meaning
        self.synonyms = synonyms
        self.extra = extra

    def __repr__(self):
        return self.word

    def load(self):
        found = Dicio().search(self.word)
        self.meaning = found.meaning
        self.synonyms = found.synonyms
        self.extra = found.extra

class Dicio(object):
    """
    Dicio API com significado, sinônimos e adicionais.
    """
    def search(self, word):
        """
        Procura pela palavra.
        """
        if len(word.split()) > 1:
            return None

        _word = remove_accents(word).strip().lower()
        url = request.urlopen(BASE_URL.format(_word))
        page = html.unescape(url.read().decode(CHARSET))

        if page.find(TAG_ENCHANT[0]) > -1:
            return None

        found = Word(word)
        found.meaning = self.meaning(page)
        found.synonyms = self.synonyms(page)
        found.extra = self.extra(page)

        return found


    def meaning(self, page):
        """
        Retorna o significado encontrado.
        """
        return remove_spaces(remove_tags(text_between(page, TAG_MEANING[0], TAG_MEANING[1], True)))

    def synonyms(self, page):
        """
        Retorna os sinônimos encontrados.
        """
        synonyms = []
        if page.find(TAG_SYNONYMS[0]) > -1:
            synonyms_html = text_between(page, TAG_SYNONYMS[0], TAG_SYNONYMS[1], True)
            while synonyms_html.find(TAG_SYNONYMS_DELIMITER[0]) > -1:
                synonym = text_between(synonyms_html, TAG_SYNONYMS_DELIMITER[0], TAG_SYNONYMS_DELIMITER[1], True)
                synonyms.append(Word(remove_spaces(synonym)))
                synonyms_html = synonyms_html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
                synonyms_html = synonyms_html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return synonyms


    def extra(self, page):
        """
        Retorna os adicionais encontrados.
        """
        dic_extra = {}
        if page.find(TAG_EXTRA[0]) > -1:
            extra_html = text_between(page, TAG_EXTRA[0], TAG_EXTRA[1], True)
            extra_rows = split_html_tag(remove_spaces(extra_html), TAG_EXTRA_SEP)
            for row in extra_rows:
                _row = remove_tags(row)
                key, value = _row.split(":")
                dic_extra[remove_spaces(key)] = remove_spaces(value)
        return dic_extra


if __name__ == "__main__":
    word = Dicio().search("Doce")
    if word:
        print(word, word.url, "\n\t", word.meaning)
        print("Sinônimos")
        for item in word.synonyms:
            item.load()
            print("\t", item, item.url, item.meaning)
        print("Extras")
        for key, value in word.extra.items():
            print("\t", key, "=>", value)
    else:
        print("Não encontrado.")
