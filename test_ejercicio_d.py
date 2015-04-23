import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_d import interseccion, IncompatibleAlphabetsError, NonDeterministicAutomataError

class TestEjercicioD(TestCase):

    def test_automatas_iguales(self):
        input_automata =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata += '\t'.join(['q1', '0', 'q0']) + '\n'
        file_input1 = StringIO(input_automata)
        file_input2 = StringIO(input_automata)
        file_output = StringIO()
        interseccion(file_input1, file_input2, file_output)

        expected =  '\t'.join(['(q0,q0)', '(q1,q1)']) + '\n'
        expected += '\t'.join(['0', '1']) + '\n'
        expected += '(q0,q0)\n'
        expected += '(q1,q1)\n'
        expected +=  '\t'.join(['(q0,q0)', '0', '(q1,q1)']) + '\n'
        expected +=  '\t'.join(['(q0,q0)', '1', '(q1,q1)']) + '\n'
        expected +=  '\t'.join(['(q1,q1)', '0', '(q0,q0)']) + '\n'


    def test_alfabetos_disjuntos(self):
        input_automata1 =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata1 += '\t'.join(['0', '1']) + '\n'
        input_automata1 += 'q0\n'
        input_automata1 += 'q1\n'
        input_automata1 += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata1 += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata1 += '\t'.join(['q1', '0', 'q0']) + '\n'

        input_automata2 =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata2 += '\t'.join(['a', 'b']) + '\n'
        input_automata2 += 'q0\n'
        input_automata2 += 'q1\n'
        input_automata2 += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q1', '0', 'q0']) + '\n'

        file_input1 = StringIO(input_automata1)
        file_input2 = StringIO(input_automata2)
        file_output = StringIO()

        with self.assertRaises(IncompatibleAlphabetsError):
            interseccion(file_input1, file_input2, file_output)

    def test_no_determinismo(self):
        input_automata1 =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata1 += '\t'.join(['0', '1']) + '\n'
        input_automata1 += 'q0\n'
        input_automata1 += 'q1\n'
        input_automata1 += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata1 += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata1 += '\t'.join(['q1', '0', 'q0']) + '\n'

        input_automata2 =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata2 += '\t'.join(['0', '1']) + '\n'
        input_automata2 += 'q0\n'
        input_automata2 += 'q1\n'
        input_automata2 += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q1', '0', 'q0']) + '\n'
        input_automata2 += '\t'.join(['q1', '0', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q1', '1', 'q1']) + '\n'

        file_input1 = StringIO(input_automata1)
        file_input2 = StringIO(input_automata2)
        file_output = StringIO()
        with self.assertRaises(NonDeterministicAutomataError):
            interseccion(file_input1, file_input2, file_output)



if __name__ == '__main__':
    unittest.main()
