#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest import TestCase

from models import Node, Automata, LAMBDA, minimize
from ejercicio_a import nfa_to_dfa, afd_minimo
from parsers import load_automata

from StringIO import StringIO


class TestEjercicioASimples(TestCase):

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
        q2 = dfa_automata.state_by_name("q2")  # Este básicamente es trampa
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
        q2 = dfa_automata.state_by_name("q2")  # Este básicamente es trampa
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


class TestEjercicioADesdeArchivo(TestCase):

    def test_only_symbol(self):
        input_regex_tree = 'a'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

        import ipdb
        ipdb.set_trace()

    def test_regex_rompe(self):
        """
            caso de prueba de la correccion
        """
        input_regex = '{CONCAT}2\n'
        input_regex += '\ta\n'
        input_regex += '\ta\n'
        file_input = StringIO(input_regex)
        file_output = StringIO()

        # aca reviso el resultado del ejercicio a.
        # user load_automata no es lo ideal
        file_input.seek(0)
        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

        #self.assertEquals(len(result.states), 3)

    def test_other_symbols(self):
        for symbol in '([,:;.¿?!¡()"\'\&-]':
            input_regex_tree = symbol
            file_input = StringIO(input_regex_tree)
            file_output = StringIO(input_regex_tree)

            afd_minimo(file_input, file_output)
            file_output.seek(0)
            result = load_automata(file_output)

    def test_simple_or(self):
        input_regex_tree = '{OR}2\n\ta\n\tb'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

    def test_simple_concat(self):
        input_regex_tree = '{CONCAT}2\n\ta\n\tb'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()
        afd_minimo(file_input, file_output)

        file_output.seek(0)
        result = load_automata(file_output)

    def test_other_simple_concat(self):
        input_regex_tree = '{CONCAT}3\n\tc\n\tb\n\ta'
        file_input = StringIO(input_regex_tree)

        file_output = StringIO()
        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

        raise Exception

    def test_simple_plus(self):
        input_regex_tree = '{PLUS}\n\ta'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

       # from_two = result.initial.transitions[LAMBDA].pop()

    def test_simple_star(self):
        input_regex_tree = '{STAR}\n\ta'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

        self.assertEquals(len(result.states), 1)

    def test_simple_opt(self):
        input_regex_tree = '{OPT}\n\ta'
        file_input = StringIO(input_regex_tree)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

    def test_regex_enunciado_1(self):
        # '(a|b|c)*(de)+f'
        file_input = '{CONCAT}3\n'
        file_input += '\t{STAR}\n'
        file_input += '\t\t{OR}3\n'
        file_input += '\t\t\ta\n'
        file_input += '\t\t\tb\n'
        file_input += '\t\t\tc\n'
        file_input += '\t{PLUS}\n'
        file_input += '\t\t{CONCAT}2\n'
        file_input += '\t\t\td\n'
        file_input += '\t\t\te\n'
        file_input += '\tf'

        file_input = StringIO(file_input)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

        self.assertTrue(result.symbols, set(['a', 'b', 'c', 'd', 'e', 'f']))

    def test_bug_simple(self):
        """
            El segundo OR usa los param del primero. este test verifica que no pase esto
        """
        file_input = '{CONCAT}2\n'
        file_input += '\t{OR}2\n'
        file_input += '\t\ta\n'
        file_input += '\t\tb\n'
        file_input += '\t{OR}2\n'
        file_input += '\t\tc\n'
        file_input += '\t\td'
        file_input = StringIO(file_input)
        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)

    def test_regex_enunciado_2(self):
        # '(-ABC)?(0|1)+\t*'
        # file_input = StringIO('(-ABC)?(0|1)+\t*')
        # result = afd_minimo(file_input)
        file_input = '{CONCAT}3\n'
        file_input += '\t{OPT}\n'
        file_input += '\t\t{CONCAT}4\n'
        file_input += '\t\t\t-\n'
        file_input += '\t\t\tA\n'
        file_input += '\t\t\tB\n'
        file_input += '\t\t\tC\n'
        file_input += '\t{PLUS}\n'
        file_input += '\t\t{OR}2\n'
        file_input += '\t\t\t0\n'
        file_input += '\t\t\t1\n'
        file_input += '\t{STAR}\n'
        file_input += '\t\t\t'

        file_input = StringIO(file_input)

        file_output = StringIO()

        afd_minimo(file_input, file_output)
        file_output.seek(0)
        result = load_automata(file_output)


if __name__ == '__main__':
    unittest.main()
