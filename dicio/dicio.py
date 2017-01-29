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
        self.url = BASE_URL.format(Utils.remove_accents(self.word))
        self.meaning = meaning
        self.synonyms = synonyms
        self.extra = extra

    def load(self):
        found = Dicio().search(self.word)
        self.meaning = found.meaning
        self.synonyms = found.synonyms
        self.extra = found.extra

    def __repr__(self):
        return self.word

    def __str__(self):
        if self.meaning:
            return self.word + ': ' + self.meaning
        return self.word


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
        found.meaning = self.scrape_meaning(page)
        found.synonyms = self.scrape_synonyms(page)
        found.extra = self.scrape_extra(page)

        return found

    def scrape_meaning(self, page):
        """
        Return meaning.
        """
        _page = Utils.text_between(page, *TAG_MEANING, force_html=True)
        _page = Utils.remove_tags(_page)
        return Utils.remove_spaces(_page)

    def scrape_synonyms(self, page):
        """
        Return list of synonyms.
        """
        synonyms = []
        if page.find(TAG_SYNONYMS[0]) > -1:
            html = Utils.text_between(page, *TAG_SYNONYMS, force_html=True)
            while html.find(TAG_SYNONYMS_DELIMITER[0]) > -1:
                synonym, html = self.first_synonym(html)
                synonyms.append(synonym)
        return synonyms

    def first_synonym(self, html):
        """
        Return the first synonym found and html without his marking.
        """
        synonym = Utils.text_between(html, *TAG_SYNONYMS_DELIMITER, force_html=True)
        synonym = Utils.remove_spaces(synonym)
        _html = html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
        _html = _html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return Word(synonym), _html

    def scrape_extra(self, page):
        """
        Return a dictionary of extra information.
        """
        dict_extra = {}
        try:
            if page.find(TAG_EXTRA[0]) > -1:
                html = Utils.text_between(page, *TAG_EXTRA, force_html=True)
                extra_rows = Utils.split_html_tag(Utils.remove_spaces(html),
                                                  TAG_EXTRA_SEP)
                for row in extra_rows:
                    _row = Utils.remove_tags(row)
                    key, value = map(Utils.remove_spaces, _row.split(":"))
                    dict_extra[key] = value
        except:
            pass
        return dict_extra
