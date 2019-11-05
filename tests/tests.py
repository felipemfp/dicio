import unittest
from dicio import Dicio, Word, Utils, dicio
from urllib.error import URLError
import os
from urllib.request import urlopen

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

comilao = {
    'meaning': 'substantivo masculino Aquele que come muito, de maneira exagerada; glutão.; [Pejorativo] Indivíduo que ganha dinheiro ilicitamente; concussionário.; adjetivo Que come muito ou ganha dinheiro ilegalmente.',
    'etymology': 'Etimologia (origem da palavra comilão ). Do latim comedone.',
    'synonyms': [
        Word(word='regalão'),
        Word(word='glutão'),
        Word(word='guloso'),
        Word(word='lambão'),
        Word(word='concussionário'),
    ],
    'word': 'comilão',
    'url': 'http://www.dicio.com.br/comilao',
    'examples': [
        '"Em geral, quem consome carne é um bom comilão , come batata, não gosta muito de peixe e bebe mais. Folha de S.Paulo, 11/08/2011',
        'O urso mais comilão dos desenhos e seu amigo Catatau ganharam uma versão "live action" (com atores) na tela grande. Folha de S.Paulo, 21/01/2011',
        'Ringo consegue ainda mais comilão e destrói de tudo na casa Eurides Nascimento, em Matão (SP). Folha de S.Paulo, 14/10/2011'
    ],
    'extra': {
        'Classe gramatical': 'adjetivo e substantivo masculino',
        'Separação silábica': 'co-mi-lão',
        'Plural': 'comilões',
        'Feminino': 'comilona',
    }
}


def getFromFile(*args, **kwargs):
    if 'raiseerror' in args[0]:
        raise URLError('404: Not found')
    return urlopen(*args, **kwargs)
    # return open(os.path.join(CURRENT_DIR, 'samples/20191027-comilao.html'),
    #             mode='rb')


class TestUtils(unittest.TestCase):
    s = '<a href="#">Something</a>'

    def test_remove_tags(self):
        expected = 'Something'
        result = Utils.remove_tags(self.s)
        self.assertEqual(expected, result)

    def test_text_before(self):
        expected = '<a href="#">Something'
        result = Utils.text_before(self.s, '</a>')
        self.assertEqual(expected, result)

    def test_text_before_not_found(self):
        expected = self.s
        result = Utils.text_before(self.s, '</br>')
        self.assertEqual(expected, result)

    def test_text_after(self):
        expected = 'Something</a>'
        result = Utils.text_after(self.s, '<a href="#">')
        self.assertEqual(expected, result)

    def test_text_after_not_found(self):
        expected = self.s
        result = Utils.text_after(self.s, '<h1>')
        self.assertEqual(expected, result)

    def test_text_between(self):
        expected = 'Something'
        result = Utils.text_between(self.s, '<a href="#">', '</a>')
        result_force_html = Utils.text_between(self.s, '<a', '/a', True)
        self.assertEqual(expected, result)
        self.assertEqual(expected, result_force_html)

    def test_text_between_not_found(self):
        expected = self.s
        result = Utils.text_between(self.s, '<h1>', '</h1>')
        result_force_html = Utils.text_between(self.s, '<h1', '/h1', True)
        self.assertEqual(expected, result)
        self.assertEqual(expected, result_force_html)

    def test_remove_spaces(self):
        text = 'Something  else\nand another thing  '
        expected = 'Something else and another thing'
        result = Utils.remove_spaces(text)
        self.assertEqual(expected, result)

    def test_remove_accents(self):
        text = 'trava-língua'
        expected = 'trava-lingua'
        result = Utils.remove_accents(text)
        self.assertEqual(expected, result)

    def test_split_html_tag(self):
        html = 'Something<br>else<br />and<br/>another<br></br>thing'
        expected = ['Something', 'else', 'and', 'another', 'thing']
        result = Utils.split_html_tag(html, 'br')
        self.assertListEqual(expected, result)


class TestWord(unittest.TestCase):

    def setUp(self):
        self.dicio = Dicio(getFromFile)

    def test_init(self):
        # arrange
        expected_word, expected_url = comilao['word'], comilao['url']

        # act
        word = Word(' Comilão ')

        # assert
        self.assertEqual(expected_word, word.word)
        self.assertEqual(expected_url, word.url)

    def test_load(self):
        # arrange
        expected = comilao['meaning']
        word = Word(comilao['word'])

        # act
        word.load(self.dicio)

        # assert
        self.assertEqual(expected, word.meaning)

    def test_load_with_custom_get(self):
        # arrange
        expected = comilao['meaning']
        word = Word(comilao['word'])

        # act
        word.load(get=getFromFile)

        # assert
        self.assertEqual(expected, word.meaning)

    def test_repr(self):
        # arrange
        instance = Word(comilao['word'])
        expected = instance.__dict__

        # assert
        self.assertDictEqual(expected, eval(repr(instance)).__dict__)

    def test_str(self):
        # arrange
        instance = Word(comilao['word'])
        instance_with_meaning = Word(comilao['word'],
                                     meaning=comilao['meaning'])
        expected = '{}'.format(comilao['word'])
        expected_with_meaning = '{}: {}'.format(comilao['word'],
                                                comilao['meaning'])

        # assert
        self.assertEqual(expected, str(instance))
        self.assertEqual(expected_with_meaning, str(instance_with_meaning))


class TestDicio(unittest.TestCase):

    def setUp(self):
        self.dicio = Dicio(getFromFile)

    def test_search(self):
        # arrange
        expected = Word(comilao['word'])
        expected.meaning = comilao['meaning']
        expected.etymology = comilao['etymology']
        expected.synonyms = comilao['synonyms']
        expected.examples = comilao['examples']
        expected.extra = comilao['extra']

        # act
        result = self.dicio.search('comilao')

        # assert
        self.assertEqual(expected.word, result.word)
        self.assertEqual(expected.url, result.url)
        self.assertEqual(expected.meaning, result.meaning)
        self.assertEqual(expected.etymology, result.etymology)
        self.assertListEqual(list(map(str, expected.synonyms)),
                             list(map(str, result.synonyms)))
        self.assertListEqual(expected.examples, result.examples)
        self.assertDictEqual(expected.extra, result.extra)

    def test_search_with_invalid_word(self):
        # arrange
        word = 'frases são inválidas'

        # act
        result = self.dicio.search(word)

        # assert
        self.assertIsNone(result)

    def test_search_with_not_real_word_or_not_found(self):
        # arrange
        word = 'raiseerror'

        # act
        result = self.dicio.search(word)

        # assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
