import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_a import afd_minimo


class TestEjercicioA(TestCase):

    def test_minimize_1(self):
        input_automata = 'a\tb\tc\td\te\tf\n'
        input_automata += '0\t1\n'
        input_automata += 'a\n'
        input_automata += 'c\t\d\te\n'
        input_automata += 'a\t0\tb\n'
        input_automata += 'b\t0\ta\n'
        input_automata += 'a\t1\tc\n'
        input_automata += 'b\t1\td\n'
        input_automata += 'd\t0\te\n'
        input_automata += 'c\t1\tf\n'
        input_automata += 'c\t0\te\n'
        input_automata += 'e\t0\te\n'
        input_automata += 'e\t1\tf\n'
        input_automata += 'f\t0\tf\n'
        input_automata += 'f\t1\tf\n'
        file_input = StringIO(input_automata)
        file_output = StringIO()
        afd_minimo(file_input, file_output)

        expected = 'q0\tq1\tq2\n'
        expected += '0\t1\n'
        expected += 'q1'
        expected += 'q0\t0\tq0\n'
        expected += 'q0\t1\tq1\n'
        expected += 'q1\t0\tq1\n'
        expected += 'q1\t1\tq2\n'
        expected += 'q2\t0\tq2\n'
        expected += 'q2\t1\tq2\n'

        import ipdb
        ipdb.set_trace()

if __name__ == '__main__':
    unittest.main()
