import unittest
from unittest import TestCase
from StringIO import StringIO

from models import Node, Automata
from ejercicio_a import afd_minimo, minimize, nfa_to_dfa


class TestEjercicioA(TestCase):

    def test_convert_nfa_to_dfa_from_hopcroft(self):
        initial = Node(name='q0')
        state_q1 = Node(name='q1')
        state_q2 = Node(name='q2')

        initial.add_transition('0', initial)
        initial.add_transition('1', initial)
        initial.add_transition('0', state_q1)

        state_q1.add_transition('1', state_q2)

        finals = [state_q2]

        nfa_automata = Automata(initial, finals)

        import ipdb
        ipdb.set_trace()
        dfa_automata = nfa_to_dfa(nfa_automata)

    def test_minize_example_from_hopcroft(self):
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
        self.assertEquals(minimized.initial.transition('0'), minimized.initial)
        other_node = minimized.initial.transition('1')
        self.assertEquals(minimized.initial.transition('1').transition('0'), minimized.initial)
        self.assertEquals(minimized.initial.transition('1'), other_node)
        self.assertEquals(minimized.initial.transition('1').transition('1'), other_node)

    def test_minimize_1(self):
        input_automata = 'a\tb\tc\td\te\tf\n'
        input_automata += '0\t1\n'
        input_automata += 'a\n'
        input_automata += 'c\t\d\te\n'
        input_automata += 'a\t0\tb\n'
        input_automata += 'b\t0\ta\n'
        input_automata += 'a\t1\tc\n'
        input_automata += 'b\t1\td\n'
        input_automata += 'd\t0\te\n'
        input_automata += 'c\t1\tf\n'
        input_automata += 'c\t0\te\n'
        input_automata += 'e\t0\te\n'
        input_automata += 'e\t1\tf\n'
        input_automata += 'f\t0\tf\n'
        input_automata += 'f\t1\tf\n'
        file_input = StringIO(input_automata)
        file_output = StringIO()
        afd_minimo(file_input, file_output)

        expected = 'q0\tq1\tq2\n'
        expected += '0\t1\n'
        expected += 'q1'
        expected += 'q0\t0\tq0\n'
        expected += 'q0\t1\tq1\n'
        expected += 'q1\t0\tq1\n'
        expected += 'q1\t1\tq2\n'
        expected += 'q2\t0\tq2\n'
        expected += 'q2\t1\tq2\n'

if __name__ == '__main__':
    unittest.main()
