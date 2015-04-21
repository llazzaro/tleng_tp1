import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_b import pertenece_al_lenguaje


class TestEjercicioA(TestCase):

    def test_pertenece(self):

        input_text = 'q0\tq1\tq2\n'
        input_text += 'a\tb\tc\td\te\tf\n'
        input_text += 'q0\n'
        input_text += 'q1\tq2\n'
        input_text += 'q0\ta\tq1\n'
        input_text += 'q1\tb\tq2\n'
        input_text += 'q1\tc\tq1\n'
        input_text += 'q2\tf\tq2'

        file_input = StringIO(input_text)
        self.assertTrue(pertenece_al_lenguaje(file_input, 'ac'))
        file_input = StringIO(input_text)
        self.assertTrue(pertenece_al_lenguaje(file_input, 'ab'))
        file_input = StringIO(input_text)
        self.assertTrue(pertenece_al_lenguaje(file_input, 'acccbfff'))
        file_input = StringIO(input_text)
        self.assertFalse(pertenece_al_lenguaje(file_input, 'af'))
        file_input = StringIO(input_text)
        self.assertFalse(pertenece_al_lenguaje(file_input, 'accca'))

if __name__ == '__main__':
    unittest.main()
