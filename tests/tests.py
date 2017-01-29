import unittest

from dicio import Dicio, Word, Utils


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

    def test_text_after(self):
        expected = 'Something</a>'
        result = Utils.text_after(self.s, '<a href="#">')
        self.assertEqual(expected, result)

    def test_text_between(self):
        expected = 'Something'
        result = Utils.text_between(self.s, '<a href="#">', '</a>')
        result_force_html = Utils.text_between(self.s, '<a', '/a', True)
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
    w = ' Comilão '

    def test_init(self):
        expected_word = 'comilão'
        expected_url = 'http://www.dicio.com.br/comilao'
        word = Word(self.w)
        self.assertEqual(expected_word, word.word)
        self.assertEqual(expected_url, word.url)

    def test_load(self):
        expected = 'adj. e s.m. Que ou aquele que come muito; comedor voraz, glutão: é obeso porque é muito comilão.'
        word = Word(self.w)
        word.load()
        self.assertEqual(expected, word.meaning)


class TestDicio(unittest.TestCase):
    w = 'doce'

    def test_search(self):
        expected = Word(self.w)
        expected.load()

        dicio = Dicio()
        result = dicio.search(self.w)

        self.assertEqual(expected.word, result.word)
        self.assertEqual(expected.url, result.url)
        self.assertEqual(expected.meaning, result.meaning)
        self.assertEqual(expected.synonyms[0].word, result.synonyms[0].word)
        self.assertEqual(expected.synonyms[-1].word, result.synonyms[-1].word)
        self.assertEqual(len(expected.synonyms), len(result.synonyms))
        self.assertDictEqual(expected.extra, result.extra)

if __name__ == '__main__':
    unittest.main()
