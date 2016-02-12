import unittest
from dicio import Dicio, utils

class TestUtilsMethods(unittest.TestCase):
    def test_remove_tags(self):
        s = '<a href="#">Something</a>'
        self.assertEqual('Something', utils.remove_tags(s))

if __name__ == '__main__':
    unittest.main()
