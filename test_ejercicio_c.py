import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_c import grafo


class TestEjercicioC(TestCase):

    def test_save_dot_(self):
        input_regex = '{CONCAT}2\n'
        input_regex += '\t{OR}2\n'
        input_regex += '\t\ta\n'
        input_regex += '\t\tb\n'
        input_regex += '\t{START}\n'
        input_regex += '\t\t{OR}2\n'
        input_regex += '\t\t\ta\n'
        input_regex += '\t\t\tb\n'

        input_automata = 'q0\tq1\n'
        input_automata += 'a\tb\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += 'q0\ta\tq1\n'
        input_automata += 'q0\tb\tq1\n'
        input_automata += 'q1\ta\tq1\n'
        input_automata += 'q1\tb\tq1\n'

        file_in = StringIO(input_automata)
        file_out = StringIO()
        grafo(file_in, file_out)

        expected = 'strict digraph {'
        expected += 'rankdir=LR;'
        expected += 'node [shape = none, label = "", width = 0, height = 0]; qd;'
        expected += 'node [label="\N", width = 0.5, height = 0.5];'
        expected += 'node [shape = doublecircle]; q1;'
        expected += 'node [shape = circle]'
        expected += 'qd -> q0'
        expected += 'q0 -> q1 [label="a, b"]'
        expected += 'q1 -> q1 [label="a, b"]'
        expected += '}'

        import ipdb
        ipdb.set_trace()
        file_out.seek(0)
        self.assertEquals(expected, file_out.read())


if __name__ == '__main__':
    unittest.main()
