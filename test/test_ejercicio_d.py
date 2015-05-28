#!/usr/bin/python
# -*- coding: utf-8 -*- 

import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import load_automata
from models import *
from ejercicio_d import afd_interseccion, interseccion, IncompatibleAlphabetsError, NonDeterministicAutomataError


class TestEjercicioD(TestCase):

    def test_interseccion_dos_automatas_iguales(self):
        q0 = Node("q0")
        q1 = Node("q1")
        q0.add_transition('0', q1)
        q0.add_transition('1', q1)
        q1.add_transition('0', q0)

        automata = Automata([q0, q1], ['0', '1'], q0, [q1])

        result = afd_interseccion(automata, automata)

        self.assertEqual(set(automata.symbols), set(result.symbols))
        self.assertEqual(len(automata.states), len(result.states))
        self.assertEqual(len(automata.finals), len(result.finals))

        qI = result.initial
        qII = result.finals[0]
        self.assertEqual(qII, qI.transition('0'))
        self.assertEqual(qII, qI.transition('1'))
        self.assertEqual(qI, qII.transition('0'))


    def test_interseccion_vacia(self):
        q0 = Node("q0")
        q1 = Node("q1")
        q0.add_transition('0', q1)
        q0.add_transition('1', q0)

        automata1 = Automata([q0, q1], ['0', '1'], q0, [q1])

        q2 = Node("q2")
        q3 = Node("q3")
        q2.add_transition('1', q3)
        q2.add_transition('0', q2)

        automata2 = Automata([q2, q3], ['0', '1'], q2, [q3])

        interseccion = afd_interseccion(automata1, automata2)

        self.assertEqual(set(automata1.symbols), set(interseccion.symbols))
        self.assertEqual(0, len(interseccion.states))

    
    def test_interseccion_010(self):
        q0_e = Node("q0")
        q1_e = Node("q1")
        q2_e = Node("q2")
        q3_e = Node("q3")
        q0_e.add_transition('0', q1_e)
        q1_e.add_transition('1', q2_e)
        q2_e.add_transition('0', q3_e)
        q3_e.add_transition('0', q3_e)
        q3_e.add_transition('1', q3_e)

        q0_t = Node("q0")
        q1_t = Node("q1")
        q2_t = Node("q2")
        q3_t = Node("q3")
        q0_t.add_transition('0', q1_t)
        q0_t.add_transition('1', q0_t)
        q1_t.add_transition('0', q1_t)
        q1_t.add_transition('1', q2_t)
        q2_t.add_transition('0', q3_t)
        q2_t.add_transition('1', q0_t)
        q3_t.add_transition('0', q0_t)
        q3_t.add_transition('1', q0_t)

        automata_empieza_010 = Automata([q0_e, q1_e, q2_e, q3_e], ['0', '1'], q0_e, [q3_e])
        automata_termina_010 = Automata([q0_t, q1_t, q2_t, q3_t], ['0', '1'], q0_t, [q3_t])

        automata_empieza_termina_010  = afd_interseccion(automata_empieza_010, automata_termina_010)

        self.assertEqual(set(automata_empieza_010.symbols), set(automata_empieza_termina_010.symbols))
        self.assertEqual(7, len(automata_empieza_termina_010.states))
        self.assertEqual(1, len(automata_empieza_termina_010.finals))

        # Voy a usar este método porque el minimzar le pone los nombres de cualquier manera.
        q0 = automata_empieza_termina_010.initial
        with self.assertRaises(KeyError):
            q0.transition('1')

        q1 = q0.transition('0')
        with self.assertRaises(KeyError):
            q1.transition('0')

        q2 = q1.transition('1')
        with self.assertRaises(KeyError):
            q2.transition('1')

        q3 = q2.transition('0')
        self.assertIn(q3, automata_empieza_termina_010.finals)

        q4 = q3.transition('0')
        self.assertEqual(q4, q3.transition('1'))
        self.assertEqual(q4, q4.transition('1'))

        q5 = q4.transition('0')
        self.assertEqual(q5, q5.transition('0'))

        q6 = q5.transition('1')
        self.assertEqual(q3, q6.transition('0'))
        self.assertEqual(q4, q6.transition('1'))

    def test_alfabetos_disjuntos(self):
        q0_1 = Node("q0")
        q1_1 = Node("q1")
        q0_1.add_transition('0', q1_1)
        q0_1.add_transition('1', q1_1)
        q1_1.add_transition('0', q0_1)

        automata1 = Automata([q0_1, q1_1], ['0', '1'], q0_1, [q1_1])

        q0_2 = Node("q0")
        q1_2 = Node("q1")
        q0_2.add_transition('a', q1_2)
        q0_2.add_transition('b', q1_2)
        q1_2.add_transition('a', q0_2)

        automata2 = Automata([q0_2, q1_2], ['a', 'b'], q0_2, [q1_2])

        interseccion = afd_interseccion(automata1, automata2)

        self.assertEqual(set(automata1.symbols) | set(automata2.symbols), set(interseccion.symbols))
        self.assertEqual(0, len(interseccion.states))

    def test_alfabetos_solapados(self):
        q0_1 = Node("q0")
        q1_1 = Node("q1")
        q0_1.add_transition('0', q1_1)
        q0_1.add_transition('1', q1_1)
        q1_1.add_transition('0', q0_1)

        automata1 = Automata([q0_1, q1_1], ['0', '1'], q0_1, [q1_1])

        q0_2 = Node("q0")
        q1_2 = Node("q1")
        q0_2.add_transition('a', q1_2)
        q0_2.add_transition('1', q1_2)
        q1_2.add_transition('a', q0_2)

        automata2 = Automata([q0_2, q1_2], ['a', '1'], q0_2, [q1_2])

        interseccion = afd_interseccion(automata1, automata2)

        self.assertEqual(set(automata1.symbols) | set(automata2.symbols), set(interseccion.symbols))
        self.assertEqual(2, len(interseccion.states))
        self.assertEqual(1, len(interseccion.finals))

        q0 = interseccion.initial
        q1 = interseccion.finals[0]

        self.assertEqual(q1, q0.transition('1'))
        with self.assertRaises(KeyError):
            q0.transition('0')
        with self.assertRaises(KeyError):
            q0.transition('a')
        with self.assertRaises(KeyError):
            q1.transition('0')
        with self.assertRaises(KeyError):
            q1.transition('1')
        with self.assertRaises(KeyError):
            q1.transition('a')


    def test_no_determinismo(self):
        q0_1 = Node("q0")
        q1_1 = Node("q1")
        q0_1.add_transition('0', q1_1)
        q0_1.add_transition('1', q1_1)
        q1_1.add_transition('0', q0_1)

        automata1 = Automata([q0_1, q1_1], ['0', '1'], q0_1, [q1_1])

        q0_2 = Node("q0")
        q1_2 = Node("q1")
        q0_2.add_transition('0', q1_2)
        q0_2.add_transition('1', q1_2)
        q1_2.add_transition('0', q0_2)
        q1_2.add_transition('0', q1_2)
        q1_2.add_transition('1', q1_2)

        automata2 = Automata([q0_2, q1_2], ['0', '1'], q0_2, [q1_2])

        with self.assertRaises(NonDeterministicAutomataError):
            afd_interseccion(automata1, automata2)



if __name__ == '__main__':
    unittest.main()
