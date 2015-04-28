import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import load_automata
from ejercicio_e import afd_complemento

class TestEjercicioE(TestCase):

    def test_complemento_1(self):
        input_automata =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata += '\t'.join(['q1', '0', 'q0']) + '\n'

        automata = load_automata(StringIO(input_automata))

        automata_complemento = afd_complemento(automata)

        self.assertEqual(automata.states(), automata_complemento.states())
        self.assertEqual(automata.initial, automata_complemento.initial)
        self.assertEqual(set(automata.states()) - automata.finals, automata_complemento.finals)
    
    

if __name__ == '__main__':
    unittest.main()
