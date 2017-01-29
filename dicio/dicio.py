"""
Unofficial Python API for Dicio.com.br

@author Felipe Pontes
@email felipemfpontes@gmail.com
"""

import html
from urllib import request
from dicio.utils import Utils

BASE_URL = 'http://www.dicio.com.br/{}'
CHARSET = 'iso-8859-1'
TAG_MEANING = ('class="significado', '</p>')
TAG_SYNONYMS = ('class="adicional sinonimos"', '</p>')
TAG_SYNONYMS_DELIMITER = ('<a', '</a>')
TAG_ENCHANT = ('id="enchant"', '</div>')
TAG_EXTRA = ('class="adicional"', '</p>')
TAG_EXTRA_SEP = 'br'
TAG_EXTRA_DELIMITER = ('<b>', '</b>')


class Word(object):
    def __init__(self, word, meaning=None, synonyms=[], extra={}):
        self.word = word.strip().lower()
        self.url = BASE_URL.format(Utils.remove_accents(word).strip().lower())
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
    Dicio API with meaning, synonyms and extra information.
    """

    def search(self, word):
        """
        Search for word.
        """
        if len(word.split()) > 1:
            return None

        _word = Utils.remove_accents(word).strip().lower()
        try:
            url = request.urlopen(BASE_URL.format(_word))
        except:
            return None
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
        Return meaning.
        """
        return Utils.remove_spaces(Utils.remove_tags(Utils.text_between(page, TAG_MEANING[0], TAG_MEANING[1], True)))

    def synonyms(self, page):
        """
        Return list of synonyms.
        """
        synonyms = []
        if page.find(TAG_SYNONYMS[0]) > -1:
            synonyms_html = Utils.text_between(page, TAG_SYNONYMS[0], TAG_SYNONYMS[1], True)
            while synonyms_html.find(TAG_SYNONYMS_DELIMITER[0]) > -1:
                synonym = Utils.text_between(synonyms_html, TAG_SYNONYMS_DELIMITER[0], TAG_SYNONYMS_DELIMITER[1], True)
                synonyms.append(Word(Utils.remove_spaces(synonym)))
                synonyms_html = synonyms_html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
                synonyms_html = synonyms_html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return synonyms

    def extra(self, page):
        """
        Return a dictionary of extra information.
        """
        dic_extra = {}
        try:
            if page.find(TAG_EXTRA[0]) > -1:
                extra_html = Utils.text_between(page, TAG_EXTRA[0], TAG_EXTRA[1], True)
                extra_rows = Utils.split_html_tag(Utils.remove_spaces(extra_html), TAG_EXTRA_SEP)
                for row in extra_rows:
                    _row = Utils.remove_tags(row)
                    key, value = _row.split(":")
                    dic_extra[Utils.remove_spaces(key)] = Utils.remove_spaces(value)
        except:
            pass
        return dic_extra
