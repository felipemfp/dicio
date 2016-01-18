"""
Python API não oficial para Dicio.com.br
@autor Felipe Pontes
@email felipemfpontes@gmail.com
"""

from urllib import request
from utils import *

BASE_URL = "http://www.dicio.com.br/{}"
CHARSET = "iso-8859-1"
TAG_MEANING = ("id=\"significado\"", "</p>")
TAG_ENCHANT = ("id=\"enchant\"", "</div>")

class Word(object):
    def __init__(self, word, meaning = None):
        self.word = word
        self.url = BASE_URL.format(word)
        self.meaning = meaning

class Dicio(object):
    """
    Dicio API com significado.
    """
    def search(self, word):
        """
        Procura pela palavra.
        """
        if len(word.split()) > 1:
            return None

        word = remove_accents(word).strip().lower()
        url = request.urlopen(BASE_URL.format(word))
        page = url.read().decode(CHARSET)

        if page.find(TAG_ENCHANT[0]) > -1:
            return None

        found = Word(word)
        found.meaning = self.meaning(page)

        return found


    def meaning(self, page):
        """
        Retorna o significado encontrado.
        """
        return remove_tags(text_between(page, TAG_MEANING[0], TAG_MEANING[1], True))


if __name__ == "__main__":
    word = Dicio().search("Carambola")
    if word:
        print(word.word, word.url, "\n\t", word.meaning)
    else:
        print("Não encontrado.")