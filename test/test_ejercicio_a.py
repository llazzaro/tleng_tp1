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
        self.assertEquals(len(dfa_automata.states), 4)
        self.assertTrue(dfa_automata.initial.transition('a').transition('b') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('a') == dfa_automata.initial.transition('a'))
        self.assertTrue(dfa_automata.initial.transition('a').transition('b').transition('a') not in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('a').transition('b') in dfa_automata.finals)

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

        self.assertEquals(len(dfa_automata.states), 9)
        # revisar
        self.assertEquals(len(dfa_automata.finals), 5)
        self.assertTrue(dfa_automata.initial.transition('a') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('b') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('b').transition('b') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('b').transition('b').transition('b') in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('a') not in dfa_automata.finals)
        self.assertTrue(dfa_automata.initial.transition('a').transition('a').transition('b') in dfa_automata.finals)

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

    def test_minimize_example_from_hopcroft(self):
        """
            basado en la figura 4.10 del libro
        """
        initial = Node(name='c')
        state_d = Node(name='d')
        state_e = Node(name='e')

        initial.add_transition('0', state_d)
        initial.add_transition('1', state_e)

        state_d.add_transition('0', state_d)
        state_d.add_transition('1', state_e)

        state_e.add_transition('1', state_e)
        state_e.add_transition('0', initial)

        finals = [initial, state_d]

        states = [initial, state_d, state_e]
        symbols = ['0', '1']

        not_minimized = Automata(states, symbols, initial, finals)

        minimized = minimize(not_minimized)

        save_dot(minimized, open('hopcroft_410.dot', 'w'))

        self.assertEquals(len(minimized.states), 2)
        self.assertTrue(LAMBDA not in minimized.symbols)
        self.assertEquals(minimized.symbols, not_minimized.symbols)
        self.assertEquals(minimized.initial.transition('0'), minimized.initial)
        other_node = minimized.initial.transition('1')
        self.assertEquals(minimized.initial.transition('1').transition('0'), minimized.initial)
        self.assertEquals(minimized.initial.transition('1'), other_node)
        self.assertEquals(minimized.initial.transition('1').transition('1'), other_node)

    def test_wikipedia_example_minimization(self):
        input_automata = '\t'.join(['a', 'b', 'c', 'd', 'e', 'f']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'a\n'
        input_automata += '\t'.join(['c', 'd', 'e']) + '\n'
        input_automata += '\t'.join(['a', '0', 'b']) + '\n'
        input_automata += '\t'.join(['a', '1', 'c']) + '\n'
        input_automata += '\t'.join(['b', '0', 'a']) + '\n'
        input_automata += '\t'.join(['b', '1', 'd']) + '\n'
        input_automata += '\t'.join(['c', '0', 'e']) + '\n'
        input_automata += '\t'.join(['c', '1', 'f']) + '\n'
        input_automata += '\t'.join(['d', '0', 'e']) + '\n'
        input_automata += '\t'.join(['d', '1', 'f']) + '\n'
        input_automata += '\t'.join(['e', '0', 'e']) + '\n'
        input_automata += '\t'.join(['e', '1', 'f']) + '\n'
        input_automata += '\t'.join(['f', '0', 'f']) + '\n'
        input_automata += '\t'.join(['f', '1', 'f'])
        automata = load_automata(StringIO(input_automata))

        # with open("files/wikipedia.aut", "w") as f:
        #    save_automata(automata, f)

        minimized = minimize(automata)

        # with open("files/wikipedia_min.aut", "w") as f:
        #    save_automata(minimized, f)

        self.assertEquals(len(minimized.states), 2)
        self.assertTrue(LAMBDA not in minimized.symbols)
        self.assertTrue(minimized.initial.transition('0') == minimized.initial)
        self.assertTrue(minimized.initial.transition('1') in minimized.finals)
        self.assertTrue(minimized.initial.transition('1').transition('0') in minimized.finals)

    def test_minimize_hopcroft_figure_4_8(self):
        input_automata = '\t'.join(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) + '\n'
        input_automata += '0\t1\n'
        input_automata += 'a\n'
        input_automata += 'c\n'
        input_automata += 'a\t0\tb\n'
        input_automata += 'a\t1\tf\n'
        input_automata += 'b\t1\tc\n'
        input_automata += 'b\t0\tg\n'
        input_automata += 'c\t1\tc\n'
        input_automata += 'c\t0\ta\n'
        input_automata += 'd\t0\tc\n'
        input_automata += 'd\t1\tg\n'
        input_automata += 'e\t1\tf\n'
        input_automata += 'e\t0\th\n'
        input_automata += 'f\t0\tc\n'
        input_automata += 'f\t1\tg\n'
        input_automata += 'g\t0\tg\n'
        input_automata += 'g\t1\te\n'
        input_automata += 'h\t0\tg\n'
        input_automata += 'h\t1\tc\n'

        automata = load_automata(StringIO(input_automata))
        minimized = minimize(automata)

        self.assertEquals(len(minimized.states), 5)
        self.assertEquals(len(minimized.finals), 1)
        self.assertTrue(LAMBDA not in minimized.symbols)

        self.assertTrue(minimized.initial.transition('0').transition('1') in minimized.finals)
        self.assertTrue(minimized.initial.transition('1').transition('0') in minimized.finals)
        self.assertEquals(minimized.initial.transition('1').transition('1').transition('1'), minimized.initial)

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
