import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_a import afd_minimo


class TestEjercicioA(TestCase):

    def test_(self):
        input_regex_tree = 'a'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()
        afd_minimo(file_input, file_output)

if __name__ == '__main__':
    unittest.main()
