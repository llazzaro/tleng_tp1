import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import load_automata
from ejercicio_d import afd_interseccion, interseccion, IncompatibleAlphabetsError, NonDeterministicAutomataError

class TestEjercicioD(TestCase):

    def test_interseccion_dos_automatas_iguales(self):
        input_automata =  '\t'.join(['q0', 'q1']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'q0\n'
        input_automata += 'q1\n'
        input_automata += '\t'.join(['q0', '0', 'q1']) + '\n'
        input_automata += '\t'.join(['q0', '1', 'q1']) + '\n'
        input_automata += '\t'.join(['q1', '0', 'q0']) + '\n'

        automata = load_automata(StringIO(input_automata))

        result = afd_interseccion(automata, automata)

        self.assertEqual(automata.symbols(), result.symbols())
        self.assertEqual(len(result.states()), len(automata.states()))
        self.assertEqual(result.initial.name, "(" + automata.initial.name + "," + automata.initial.name + ")")
        self.assertEqual(len(result.finals), len(automata.finals))
        
        automata_names = set(map(lambda s: s.name, automata.finals))
        result_names = set(map(lambda s: s.name, result.finals))

        for n in automata_names:
            self.assertIn("(" + n + "," + n + ")", result_names)


    
    #def test_interseccion_vacia(self):
        #input_automata1 = '\t'.join(['q0', 'q1']) + '\n'
        #input_automata1 += '\t'.join(['0', '1']) + '\n'
        #input_automata1 += 'q0\n'
        #input_automata1 += 'q1\n'
        #input_automata1 += '\t'.join(['q0', '0', 'q1']) + '\n'
        #input_automata1 += '\t'.join(['q0', '1', 'q0']) + '\n'

        #input_automata2 = '\t'.join(['q0', 'q1']) + '\n'
        #input_automata2 += '\t'.join(['0', '1']) + '\n'
        #input_automata2 += 'q0\n'
        #input_automata2 += 'q1\n'
        #input_automata2 += '\t'.join(['q0', '1', 'q1']) + '\n'
        #input_automata2 += '\t'.join(['q0', '0', 'q0']) + '\n'

        #automata1 = load_automata(StringIO(input_automata1))
        #automata2 = load_automat(StringIO(input_automata2))

        #interseccion_vacia = afd_interseccion(automata1, automata2)

        #expected =  '\t'.join(['(q0,q0)', '(q1,q1)']) + '\n'
        #expected += '\t'.join(['0', '1']) + '\n'
        #expected += '(q0,q0)\n'
        #expected += '(q1,q1)\n'

    
#    def test_interseccion_010(self):
#        i_automata_empieza_010 =  '\t'.join(["q" + str(i) for i in range(0, 4)]) + '\n'
#        i_automata_empieza_010 += '\t'.join(['0', '1']) + '\n'
#        i_automata_empieza_010 += 'q0' + '\n'
#        i_automata_empieza_010 += 'q3' + '\n'
#        i_automata_empieza_010 += '\t'.join(['q0', '0', 'q1']) + '\n'
#        i_automata_empieza_010 += '\t'.join(['q1', '1', 'q2']) + '\n'
#        i_automata_empieza_010 += '\t'.join(['q2', '0', 'q3']) + '\n'
#        i_automata_empieza_010 += '\t'.join(['q3', '0', 'q3']) + '\n'
#        i_automata_empieza_010 += '\t'.join(['q3', '1', 'q3']) + '\n'
#
#        i_automata_termina_010 =  '\t'.join(["q" + str(i) for i in range(0, 4)]) + '\n'
#        i_automata_termina_010 += '\t'.join(['0', '1']) + '\n'
#        i_automata_termina_010 += 'q0' + '\n'
#        i_automata_termina_010 += 'q3' + '\n'
#        i_automata_termina_010 += '\t'.join(['q0', '0', 'q1']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q0', '1', 'q0']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q1', '0', 'q1']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q1', '1', 'q2']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q2', '0', 'q3']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q2', '1', 'q0']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q3', '0', 'q0']) + '\n'
#        i_automata_termina_010 += '\t'.join(['q3', '1', 'q0']) + '\n'
#
#        file_input1 = StringIO(i_automata_empieza_010)
#        file_input2 = StringIO(i_automata_termina_010)
#        file_output = StringIO()
#        interseccion(file_input1, file_input2, file_output)
#
#
#        #expected = la cadena "010"
#        expected =  '\t'.join(["(q" + str(i) + ",q" + str(i) + ")" for i in range(0, 4)]) + '\n'
#        expected += '\t'.join(['0', '1']) + '\n'
#        expected += '(q0,q0)' + '\n'
#        expected += '(q3,q3)' + '\n'
#        expected += '\t'.join(['(q0,q0)', '0', '(q1,q1)']) + '\n'
#        expected += '\t'.join(['(q1,q1)', '1', '(q2,q2)']) + '\n'
#        expected += '\t'.join(['(q2,q2)', '0', '(q3,q3)']) + '\n'


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
        input_automata2 += '\t'.join(['q0', 'a', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q0', 'b', 'q1']) + '\n'
        input_automata2 += '\t'.join(['q1', 'a', 'q0']) + '\n'

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
