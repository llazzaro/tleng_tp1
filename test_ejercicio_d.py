import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_d import interseccion, IncompatibleAlphabetsError

class TestEjercicioD(TestCase):

    def test_automatas_iguales(self):
        input_automata = 'q0\tq1\n'
        input_automata += '0\t1\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += 'q0\t0\tq1\n'
        input_automata += 'q0\t1\tq1\n'
        input_automata += 'q1\t0\tq0\n'
        file_input1 = StringIO(input_automata)
        file_input2 = StringIO(input_automata)
        file_output = StringIO()
        interseccion(file_input1, file_input2, file_output)

        expected = '(q0,q0)\t(q1,q1)\n'
        expected += '0\t1\n'
        expected += '(q0,q0)\n'
        expected += '(q1,q1)\n'
        expected += '(q0,q0)\t0\t(q1,q1)\n'
        expected += '(q0,q0)\t1\t(q1,q1)\n'
        expected += '(q1,q1)\t0\t(q0,q0)\n'

        import ipdb
        ipdb.set_trace()

    def test_alfabetos_disjuntos(self):
        input_automata1 = 'q0\tq1\n'
        input_automata1 += '0\t1\n'
        input_automata1 += 'q0\n'
        input_automata1 += 'q1\n'
        input_automata1 += 'q0\t0\tq1\n'
        input_automata1 += 'q0\t1\tq1\n'
        input_automata1 += 'q1\t0\tq0\n'

        input_automata2 = 'q0\tq1\n'
        input_automata2 += 'a\tb\n'
        input_automata2 += 'q0\n'
        input_automata2 += 'q1\n'
        input_automata2 += 'q0\ta\tq1\n'
        input_automata2 += 'q0\tb\tq1\n'
        input_automata2 += 'q1\ta\tq0\n'

        file_input1 = StringIO(input_automata1)
        file_input2 = StringIO(input_automata2)
        file_output = StringIO()
        with self.assertRaises(IncompatibleAlphabetsError):
            interseccion(file_input1, file_input2, file_output)


if __name__ == '__main__':
    unittest.main()
