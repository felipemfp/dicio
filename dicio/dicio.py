"""
Unofficial Python API for Dicio.com.br

@author Felipe Pontes
@email felipemfpontes@gmail.com
"""

import html
from urllib.request import urlopen
from dicio.utils import Utils

BASE_URL = 'http://www.dicio.com.br/{}'
CHARSET = 'utf-8'
TAG_MEANING = ('class="significado', '</p>')
TAG_ETYMOLOGY = ('class="etim', '</span>')
TAG_SYNONYMS = ('class="adicional sinonimos"', '</p>')
TAG_SYNONYMS_DELIMITER = ('<a', '</a>')
TAG_EXTRA = ('class="adicional"', '</p>')
TAG_EXTRA_SEP = 'br'
TAG_EXTRA_DELIMITER = ('<b>', '</b>')
TAG_PHRASE_DELIMITER = ('<div class="frase"', '</div>')


class Word(object):

    def __init__(self, word, meaning=None, etymology=None, synonyms=[], examples=[], extra={},
                 antonyms=[], masculine=None, feminine=None, singular=[], plural=[]):

        self.word = word.strip().lower()
        self.url = BASE_URL.format(Utils.remove_accents(self.word))
        self.meaning = meaning
        self.etymology = etymology
        self.synonyms = synonyms
        self.extra = extra
        self.examples = examples
        self.antonyms = antonyms
        self.masculine = masculine
        self.feminine = feminine
        self.singular = singular
        self.plural = plural

    def load(self, dicio=None, get=urlopen):
        if dicio:
            found = dicio.search(self.word)
        else:
            found = Dicio(get).search(self.word)

        if found is not None:
            self.word = found.word
            self.meaning = found.meaning
            self.etymology = found.etymology
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

        meaning, etymology = self.scrape_meaning(page)

        return Word(
            Utils.text_between(page, "<h1", "</h1>",  force_html=True).lower(),
            meaning=meaning,
            etymology=etymology,
            synonyms=self.scrape_synonyms(page),
            examples=self.scrape_examples(page),
            extra=self.scrape_extra(page),
        )

    def scrape_meaning(self, page):
        """
        Return meaning and etymology.
        """
        html = Utils.text_between(page, *TAG_MEANING, force_html=True)

        etymology = Utils.text_between(html, *TAG_ETYMOLOGY, force_html=True)
        etymology = Utils.remove_spaces(Utils.remove_tags(etymology))

        meanings = Utils.split_html_tag(html, 'br')
        meanings = [Utils.remove_spaces(Utils.remove_tags(x))
                    for x in meanings]
        meaning = '; '.join([x for x in meanings if x != etymology])

        return meaning, etymology

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


import re
import requests
import os
import pickle
from bs4 import BeautifulSoup

class DicioAPI(object):
    """
    Dicio API requests to official Dicio API with meaning, synonyms, antonyms, plural and gender-relative variation.
    There is no extra info. For this, use class Dicio.
    """

    def __init__(self) :

        self.api_dicio = 'https://www.dicio.com.br/api/indexv2.php?p={}'
        self.api_synon = 'https://www.sinonimos.com.br/api/?method=getSinonimos&palavra={}'
        self.api_anton = 'https://www.antonimos.com.br/api/?method=getAntonimos&palavra={}'


    def search(self, word):

        try:
            with requests.get(self.api_dicio.format(word)) as request:
                if 'error' in request.json():
                    suggestions = None
                    if request.json()['suggestions']:
                        suggestions = [item['palavra'] for item in request.json()['suggestions']]

                    suggestions_text = 'Suggestions: {}'.format(', '.join(suggestions)) if suggestions else ''
                    print('No word found. {}'.format(suggestions_text))
                    return None
                else:
                    valid_word = self.validate_word(request.json())
                    return self.format_word(valid_word)
        except:
            return None

    def format_word(self, json_word):

        meaning = self.get_meaning(json_word)

        return Word(
            json_word['palavra'],
            meaning=meaning,
            synonyms=self.get_synonyms(json_word),
            antonyms=self.get_antonyms(json_word),
            masculine=self.get_masculine_word(json_word),
            feminine=self.get_feminine_word(json_word),
            singular=self.get_singular(json_word),
            plural=self.get_plural(json_word),
            examples=self.get_examples(json_word),
        )

    def get_meaning(self, json_word):

        if 'definicao' in json_word:
            definitions = list()
            for d in json_word['definicao']:
                classification = dict()
                classification['classificacao'] = d['classificacao']
                classification['acepcoes'] = self.format_aceptions(d['acepcoes'])
                if 'etimologia' in d:
                    classification['etimologia'] = d['etimologia']

                definitions.append(classification)

            return definitions

        else:
            return None

    def format_aceptions(self, aceptions: list):

        if aceptions:
            dict_aceptions = dict()
            for i in aceptions:
                xml = BeautifulSoup(i, 'html.parser')
                context = xml.find('span')
                if context:
                    sentence_formatted = i.replace(str(xml.find('span')) + " ", "")
                    if context.text in dict_aceptions.keys():
                        dict_aceptions[context.text].append(sentence_formatted)
                    else:
                        dict_aceptions[context.text] = [sentence_formatted]
                else:
                    if "[Outros]" in dict_aceptions.keys():
                        dict_aceptions["[Outros]"].append(xml.text)
                    else:
                        dict_aceptions["[Outros]"] = [xml.text]

            return dict_aceptions
        else:
            return None

    def get_synonyms(self, json_word):
        return json_word['sinonimos'].split(';') if 'sinonimos' in json_word else None

    def get_antonyms(self, json_word):
        return json_word['antonimos'].split(';') if 'antonimos' in json_word else None

    def get_examples(self, json_word):
        return json_word['frase'].split(';') if 'frase' in json_word else None

    def get_singular(self, json_word):
        return json_word['singulares'].split(';') if 'singulares' in json_word else None

    def get_plural(self, json_word):
        return json_word['plurais'].split(';') if 'plurais' in json_word else None

    def get_synonyms_json(self, word):

        try:
            with requests.get(self.api_synon.format(word)) as request:
                return request.json()
        except:
            return None

    def get_antonyms_json(self, word):

        try:
            with requests.get(self.api_anton.format(word)) as request:
                return request.json()
        except:
            return None

    def get_inverse_gender_word(self, json_word, masculine = True):

        if 'femininos' in json_word:
            return json_word['femininos'] if masculine else json_word['palavra']
        elif 'masculinos' in json_word:
            return json_word['masculinos'] if not masculine else json_word['palavra']
        else:
            return None

    def get_masculine_word(self, json_word):
        return self.get_inverse_gender_word(json_word, False)

    def get_feminine_word(self, json_word) :
        return self.get_inverse_gender_word(json_word, True)

