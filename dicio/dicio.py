"""
Unofficial Python API for Dicio.com.br

@author Felipe Pontes
@email felipemfpontes@gmail.com
"""

import html
from urllib.request import urlopen
from dicio.utils import Utils

BASE_URL = 'http://www.dicio.com.br/{}'
CHARSET = 'iso-8859-1'
TAG_MEANING = ('class="significado', '</p>')
TAG_SYNONYMS = ('class="adicional sinonimos"', '</p>')
TAG_SYNONYMS_DELIMITER = ('<a', '</a>')
TAG_EXTRA = ('class="adicional"', '</p>')
TAG_EXTRA_SEP = 'br'
TAG_EXTRA_DELIMITER = ('<b>', '</b>')
TAG_PHRASE_DELIMITER = ('<div class="frase"', '</div>')


class Word(object):

    def __init__(self, word, meaning=None, synonyms=[], examples=[], extra={}):
        self.word = word.strip().lower()
        self.url = BASE_URL.format(Utils.remove_accents(self.word))
        self.meaning = meaning
        self.synonyms = synonyms
        self.extra = extra
        self.examples = examples

    def load(self, dicio=None, get=urlopen):
        if dicio:
            found = dicio.search(self.word)
        else:
            found = Dicio(get).search(self.word)

        if found is not None:
            self.word = found.word
            self.meaning = found.meaning
            self.synonyms = found.synonyms
            self.extra = found.extra
            self.examples = found.examples

    def __repr__(self):
        return 'Word({!r})'.format(self.word)

    def __str__(self):
        if self.meaning:
            return self.word + ': ' + self.meaning
        return self.word


class Dicio(object):
    """
    Dicio API with meaning, synonyms and extra information.
    """

    def __init__(self, get=urlopen):
        self.get = get

    def search(self, word):
        """
        Search for word.
        """
        if len(word.split()) > 1:
            return None

        _word = Utils.remove_accents(word).strip().lower()
        try:
            with self.get(BASE_URL.format(_word)) as request:
                page = html.unescape(request.read().decode(CHARSET))
        except:
            return None

        return Word(
            Utils.text_between(page, "<h1", "</h1>",  force_html=True).lower(),
            meaning=self.scrape_meaning(page),
            synonyms=self.scrape_synonyms(page),
            examples=self.scrape_examples(page),
            extra=self.scrape_extra(page),
        )

    def scrape_meaning(self, page):
        """
        Return meaning.
        """
        html = Utils.text_between(page, *TAG_MEANING, force_html=True)
        text = Utils.remove_tags(html)
        return Utils.remove_spaces(text)

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
        synonym = Utils.text_between(html, *TAG_SYNONYMS_DELIMITER,
                                     force_html=True)
        synonym = Utils.remove_spaces(synonym)
        _html = html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
        _html = _html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return Word(synonym), _html

    def scrape_examples(self, page):
        """
        Return a list of examples.
        """
        examples = []
        html = page
        index = html.find(TAG_PHRASE_DELIMITER[0])
        while index > -1:
            example_html = Utils.text_between(
                html, *TAG_PHRASE_DELIMITER, force_html=True)
            examples += [Utils.remove_spaces(Utils.remove_tags(example_html))]
            html = html[index+len(TAG_PHRASE_DELIMITER[0]):]
            index = html.find(TAG_PHRASE_DELIMITER[0])
        return examples

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
