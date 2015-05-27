#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest import TestCase
from StringIO import StringIO

from models import Node, Automata, LAMBDA, minimize
from ejercicio_a import nfa_to_dfa
from parsers import load_automata
from writers import save_dot


class TestEjercicioA(TestCase):

    def test_simple_nfa_to_dfa(self):
        initial = Node(name='1')
        state_2 = Node(name='2')
        state_3 = Node(name='3')

        initial.add_transition('a', state_2)
        state_2.add_transition(LAMBDA, initial)
        state_2.add_transition('b', state_3)

        nfa_automata = Automata([initial, state_2, state_3], ['a', 'b'], initial, [state_3])

        dfa_automata = nfa_to_dfa(nfa_automata)

        self.assertTrue(dfa_automata.is_deterministic())
        self.assertFalse(nfa_automata.is_deterministic())

        self.assertEqual(nfa_automata.symbols, dfa_automata.symbols)
        self.assertEqual(len(dfa_automata.states), 4)

        q0 = dfa_automata.state_by_name("q0")
        q1 = dfa_automata.state_by_name("q1")
        q2 = dfa_automata.state_by_name("q2") # Este básicamente es trampa
        q3 = dfa_automata.state_by_name("q3")

        self.assertEqual(q0, dfa_automata.initial)
        self.assertEqual([q3], dfa_automata.finals)

        self.assertEqual(q1, q0.transition('a'))
        self.assertEqual(q2, q0.transition('b'))
        self.assertEqual(q1, q1.transition('a'))
        self.assertEqual(q3, q1.transition('b'))
        self.assertEqual(q2, q2.transition('a'))
        self.assertEqual(q2, q2.transition('b'))
        self.assertEqual(q2, q3.transition('a'))
        self.assertEqual(q2, q3.transition('b'))


    def test_simple_nfa_to_dfa_other(self):
        """
            ultimo ejemplo de http://www.cs.umd.edu/class/spring2011/cmsc330/s4/nfa-to-dfa.pdf
        """
        initial = Node(name='1')
        state_2 = Node(name='2')
        state_3 = Node(name='3')
        state_4 = Node(name='4')
        state_5 = Node(name='5')
        state_6 = Node(name='6')

        initial.add_transition(LAMBDA, state_2)
        initial.add_transition(LAMBDA, state_5)
        state_2.add_transition('a', state_3)
        state_3.add_transition('b', state_4)
        state_4.add_transition('b', state_5)
        state_5.add_transition('a', state_6)
        state_5.add_transition('a', state_2)
        state_6.add_transition('b', state_6)
        state_6.add_transition(LAMBDA, state_2)

        nfa_automata = Automata([initial, state_2, state_3, state_4, state_5, state_6], ['a', 'b'], initial, [state_4, state_6])
        dfa_automata = nfa_to_dfa(nfa_automata)

        self.assertTrue(dfa_automata.is_deterministic())

        self.assertEqual(nfa_automata.symbols, dfa_automata.symbols)
        self.assertEqual(len(dfa_automata.states), 9)

        q0 = dfa_automata.state_by_name("q0")
        q1 = dfa_automata.state_by_name("q1")
        q2 = dfa_automata.state_by_name("q2") # Este básicamente es trampa
        q3 = dfa_automata.state_by_name("q3")
        q4 = dfa_automata.state_by_name("q4")
        q5 = dfa_automata.state_by_name("q5")
        q6 = dfa_automata.state_by_name("q6")
        q7 = dfa_automata.state_by_name("q7")
        q8 = dfa_automata.state_by_name("q8")

        self.assertEqual(q0, dfa_automata.initial)
        self.assertEqual(set([q1, q4, q5, q6, q8]), set(dfa_automata.finals))

        self.assertEqual(q1, q0.transition('a'))
        self.assertEqual(q2, q0.transition('b'))
        self.assertEqual(q3, q1.transition('a'))
        self.assertEqual(q4, q1.transition('b'))
        self.assertEqual(q2, q2.transition('a'))
        self.assertEqual(q2, q2.transition('b'))
        self.assertEqual(q2, q3.transition('a'))
        self.assertEqual(q5, q3.transition('b'))
        self.assertEqual(q3, q4.transition('a'))
        self.assertEqual(q6, q4.transition('b'))
        self.assertEqual(q2, q5.transition('a'))
        self.assertEqual(q7, q5.transition('b'))
        self.assertEqual(q1, q6.transition('a'))
        self.assertEqual(q8, q6.transition('b'))
        self.assertEqual(q8, q7.transition('a'))
        self.assertEqual(q2, q7.transition('b'))
        self.assertEqual(q3, q8.transition('a'))
        self.assertEqual(q8, q8.transition('b'))


    def test_convert_nfa_to_dfa_from_hopcroft(self):
        """
            el automata corresponde a la figura 2.9 del libro.
            el resultado es la firgura 2.14 (pagina 63)
        """
        initial = Node(name='q0')
        state_q1 = Node(name='q1')
        state_q2 = Node(name='q2')

        initial.add_transition('0', initial)
        initial.add_transition('1', initial)
        initial.add_transition('0', state_q1)

        state_q1.add_transition('1', state_q2)

        finals = [state_q2]

        states = [initial, state_q1, state_q2]
        symbols = ['0', '1']

        nfa_automata = Automata(states, symbols, initial, finals)

        dfa_automata = nfa_to_dfa(nfa_automata)

        # FIXME reescribir
        self.assertEquals(set(dfa_automata.symbols), set(nfa_automata.symbols))
        self.assertEquals(len(dfa_automata.states), 3)
        self.assertTrue(dfa_automata.is_deterministic())
        dfa_state_q0q1 = dfa_automata.initial.transition('0')
        dfa_state_q0q2 = dfa_state_q0q1.transition('1')

        self.assertEquals(dfa_automata.initial.transition('1'), dfa_automata.initial)

        self.assertEquals(dfa_state_q0q1.transition('0'), dfa_state_q0q1)
        self.assertEquals(dfa_state_q0q1.transition('1'), dfa_state_q0q2)

        self.assertEquals(dfa_state_q0q1.transition('1'), dfa_state_q0q2)

        self.assertEquals(dfa_state_q0q2.transition('0'), dfa_state_q0q1)
        self.assertEquals(dfa_state_q0q2.transition('1'), dfa_automata.initial)

        self.assertTrue(dfa_state_q0q2 in dfa_automata.finals)
        self.assertEquals(len(dfa_automata.finals), 1)

    def test_convert_nfa_to_dfa_con_lambda(self):
        """
            el ejemplo lo saque de aca
            http://condor.depaul.edu/glancast/444class/docs/nfa2dfa.html
        """
        initial = Node(name='1')
        state_2 = Node(name='2')
        state_3 = Node(name='3')
        state_4 = Node(name='4')
        state_5 = Node(name='5')

        initial.add_transition(LAMBDA, state_2)
        initial.add_transition('a', state_3)
        state_2.add_transition('a', state_5)
        state_2.add_transition('a', state_4)
        state_3.add_transition('b', state_4)
        state_4.add_transition('a', state_5)
        state_4.add_transition('b', state_5)

        nfa_automata = Automata([initial, state_2, state_3, state_4, state_5], ['a', 'b'], initial, [state_5])

        dfa_automata = nfa_to_dfa(nfa_automata)

        # FIXME reescribir
        self.assertEquals(len(dfa_automata.states), 5)
        self.assertEquals(dfa_automata.symbols, nfa_automata.symbols)
        self.assertEquals(len(dfa_automata.finals), 3)
        self.assertFalse(dfa_automata.has_lambda())
        self.assertTrue(dfa_automata.is_deterministic())
        self.assertTrue(dfa_automata.initial.transition('a') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('b') not in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('a') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('b') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a') != dfa_automata.initial.transition('a').transition('a'))
        self.assertTrue(dfa_automata.initial.transition('a') != dfa_automata.initial.transition('a').transition('b'))
        self.assertTrue(dfa_automata.initial.transition('a').transition('a') != dfa_automata.initial.transition('a').transition('b'))
        self.assertTrue(dfa_automata.initial.transition('a').transition('b').transition('a') == dfa_automata.initial.transition('a').transition('a'))
        self.assertTrue(dfa_automata.initial.transition('a').transition('b').transition('b') == dfa_automata.initial.transition('a').transition('a'))

    def test_minimize_caso_regex_enunciado(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = open(os.path.join(current_dir, 'automata_pruebas.aut'), 'r')

        automata = load_automata(input_file)

        self.assertEquals(len(automata.states), 12)

        minimized = minimize(automata)

        self.assertEquals(minimized.symbols, automata.symbols)
        self.assertEquals(len(minimized.states), 8)
        self.assertTrue(LAMBDA not in minimized.symbols)


if __name__ == '__main__':
    unittest.main()
