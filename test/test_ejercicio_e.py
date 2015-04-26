import unittest
from unittest import TestCase
from StringIO import StringIO

from ejercicio_e import complemento

class TestEjercicioE(TestCase):

    def test_complemento_1(self):
        input_automata =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata += '\t'.join(['q1', '0', 'q0']) + '\n'

        file_input1 = StringIO(input_automata)
        file_output = StringIO()
        complemento(file_input1, file_output)

        expected =  '\t'.join(['q0', 'q1']) + '\n'
        expected += '\t'.join(['0', '1']) + '\n'
        expected += 'q0\n'
        expected += 'q0\n'
        expected += '\t'.join(['q0', '0', 'q1']) + '\n'
        expected += '\t'.join(['q0', '1', 'q1']) + '\n'
        expected += '\t'.join(['q1', '0', 'q0']) + '\n'
    
    

if __name__ == '__main__':
    unittest.main()
