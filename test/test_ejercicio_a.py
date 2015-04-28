import unittest
from unittest import TestCase
from StringIO import StringIO

from models import Node, Automata
from ejercicio_a import minimize, nfa_to_dfa
from parsers import load_automata
#from writers import save_automata


class TestEjercicioA(TestCase):

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

        nfa_automata = Automata(initial, finals)

        dfa_automata = nfa_to_dfa(nfa_automata)

        self.assertEquals(dfa_automata.symbols(), nfa_automata.symbols())
        self.assertEquals(len(dfa_automata.states()), 3)
        self.assertTrue(dfa_automata.is_deterministic())
        dfa_state_q0q1 = dfa_automata.initial.transition('0')
        dfa_state_q0q2 = dfa_state_q0q1.transition('1')

        self.assertEquals(dfa_automata.initial.transition('1'), dfa_automata.initial)
        self.assertEquals(dfa_automata.initial.nfa_states, set([initial]))
        self.assertEquals(dfa_state_q0q1.nfa_states, set([initial, state_q1]))
        self.assertEquals(dfa_state_q0q2.nfa_states, set([state_q2, initial]))

        self.assertEquals(dfa_state_q0q1.transition('0'), dfa_state_q0q1)
        self.assertEquals(dfa_state_q0q1.transition('1'), dfa_state_q0q2)

        self.assertEquals(dfa_state_q0q1.transition('1'), dfa_state_q0q2)

        self.assertEquals(dfa_state_q0q2.transition('0'), dfa_state_q0q1)
        self.assertEquals(dfa_state_q0q2.transition('1'), dfa_automata.initial)

        self.assertTrue(dfa_state_q0q2 in dfa_automata.finals)
        self.assertEquals(len(dfa_automata.finals), 1)

    def test_minize_example_from_hopcroft(self):
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

        not_minimized = Automata(initial, finals)

        minimized = minimize(not_minimized)

        self.assertEquals(len(minimized.states()), 2)
        self.assertEquals(minimized.symbols(), not_minimized.symbols())
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

        #with open("files/wikipedia.aut", "w") as f:
        #    save_automata(automata, f)

        minimized = minimize(automata)

        #with open("files/wikipedia_min.aut", "w") as f:
        #    save_automata(minimized, f)

        self.assertEquals(len(minimized.states()), 3)
        self.assertTrue(minimized.initial.transition('0') == minimized.initial)
        self.assertTrue(minimized.initial.transition('1') in minimized.finals)
        self.assertTrue(minimized.initial.transition('1').transition('0') in minimized.finals)
        self.assertNotEquals(minimized.initial.transition('1').transition('1'), minimized.initial)
        self.assertFalse(minimized.initial.transition('1').transition('1') in minimized.finals)

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

        self.assertEquals(len(minimized.states()), 5)
        self.assertEquals(len(minimized.finals), 1)

        self.assertTrue(minimized.initial.transition('0').transition('1') in minimized.finals)
        self.assertTrue(minimized.initial.transition('1').transition('0') in minimized.finals)
        self.assertEquals(minimized.initial.transition('1').transition('1').transition('1'), minimized.initial)


if __name__ == '__main__':
    unittest.main()
