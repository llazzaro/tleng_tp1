import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_c import grafo


class TestEjercicioC(TestCase):

    def test_save_dot_(self):
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

        expected = 'strict digraph {\n'
        expected += 'rankdir=LR;\n'
        expected += 'node [shape = none, label = "", width = 0, height = 0]; qd;\n'
        expected += 'node [label="\N", width = 0.5, height = 0.5];\n'
        expected += 'node [shape = doublecircle]; "q1";\n'
        expected += 'node [shape = circle];\n'
        expected += 'qd -> "q0"\n'
        expected += '"q0" -> "q1" [label="a, b"]\n'
        expected += '"q1" -> "q1" [label="a, b"]\n'
        expected += '}'

        file_out.seek(0)
        self.assertEquals(expected, file_out.read())


if __name__ == '__main__':
    unittest.main()
