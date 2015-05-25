# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
from unittest import TestCase

from models import *

class TestNode(TestCase):
    def test_construccion_node__with_name(self):
        name = "q0"
        n = Node(name)

        self.assertEqual(name, n.name)
        self.assertEqual({}, n.transitions)

    def test_construccion_node__without_name(self):
        n = Node()

        self.assertEqual('q{0}'.format(Node.NODE_INDEX - 1), n.name)
        self.assertEqual({}, n.transitions)


    def test_add_transition__new_symbol(self):
        tested = Node()
        target = Node()
        s = 'a'

        self.assertFalse(tested.transitions.has_key(s))
        tested.add_transition(s, target)

        self.assertTrue(tested.transitions.has_key(s))
        self.assertEqual([target], tested.transitions[s])


    def test_add_transition__existing_symbol(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(s, target2)

        self.assertEqual(set([target1, target2]), set(tested.transitions[s]))

    def test_is_deterministic_node__lambda_not_det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        target3 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(LAMBDA, target2)
        tested.add_transition(s, target3)

        self.assertFalse(tested.is_deterministic())

    def test_is_deterministic_node__not_det(self):
        tested = Node()
        target1 = Node()
        target3 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(s, target3)

        self.assertFalse(tested.is_deterministic())

    def test_is_deterministic_node__lambda_det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(LAMBDA, target2)

        self.assertFalse(tested.is_deterministic())

    def test_is_deterministic_node__det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        s = 'a'
        s2 = 'b'

        tested.add_transition(s, target1)
        tested.add_transition(s2, target2)

        self.assertTrue(tested.is_deterministic())

    def test_is_lambda_deterministic_node__lambda_not_det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        target3 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(LAMBDA, target2)
        tested.add_transition(s, target3)

        self.assertFalse(tested.is_lambda_deterministic())

    def test_is_lambda_deterministic_node__not_det(self):
        tested = Node()
        target1 = Node()
        target3 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(s, target3)

        self.assertFalse(tested.is_lambda_deterministic())

    def test_is_lambda_deterministic_node__lambda_det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        s = 'a'

        tested.add_transition(s, target1)
        tested.add_transition(LAMBDA, target2)

        self.assertTrue(tested.is_lambda_deterministic())

    def test_is_lambda_deterministic_node__det(self):
        tested = Node()
        target1 = Node()
        target2 = Node()
        s = 'a'
        s2 = 'b'

        tested.add_transition(s, target1)
        tested.add_transition(s2, target2)

        self.assertTrue(tested.is_deterministic())

class TestAutomata(TestCase):
    def test_construction_automata__ok(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition(LAMBDA, final)

        states = [initial, final, other_node]
        symbols = ['a', LAMBDA]
        automata = Automata(states, symbols, initial, [final])


        self.assertEqual(states,  automata.states)
        self.assertEqual(symbols, automata.symbols)
        self.assertEqual(initial, automata.initial)
        self.assertEqual([final], automata.finals)

    def test_construction_automata__unexpected_symbol(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition('z', final)

        states = [initial, final, other_node]
        symbols = ['a']

        with self.assertRaises(UnexpectedSymbolOnStateException):
            automata = Automata(states, symbols, initial, [final])

    def test_construction_automata__invalid_final(self):
        initial = Node()
        final = Node()
        initial.add_transition('a', final)

        states = [initial, final]
        symbols = ['a']

        with self.assertRaises(FinalsNotInStatesException):
            automata = Automata(states, symbols, initial, [Node()])

    def test_construction_automata__extra_final(self):
        initial = Node()
        final = Node()
        initial.add_transition('a', final)

        states = [initial, final]
        symbols = ['a']

        with self.assertRaises(FinalsNotInStatesException):
            automata = Automata(states, symbols, initial, [final, Node()])

    def test_is_deterministic_automata__lambda_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition(LAMBDA, final)
        automata = Automata([initial, final, other_node], ['a', LAMBDA], initial, [final])

        self.assertFalse(automata.is_deterministic())

    def test_is_deterministic_automata__not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_deterministic())

    def test_is_deterministic_automata__lambda_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a', LAMBDA], initial, [final])

        self.assertFalse(automata.is_deterministic())

    def test_is_deterministic_automata__det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertTrue(automata.is_deterministic())

    def test_is_lambda_deterministic_automata__lambda_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition(LAMBDA, final)
        automata = Automata([initial, final, other_node], ['a', LAMBDA], initial, [final])

        self.assertFalse(automata.is_lambda_deterministic())

    def test_is_lambda_deterministic_automata_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_lambda_deterministic())

    def test_is_lambda_deterministic_automata__lambda_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a', LAMBDA], initial, [final])

        self.assertTrue(automata.is_lambda_deterministic())

    def test_is_lambda_deterministic_automata__det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a', LAMBDA], initial, [final])

        self.assertTrue(automata.is_lambda_deterministic())

    def test_get_by_name__existing(self):
        q0 = Node("q0")

        automata = Automata([q0], ['a'], q0, [q0])

        self.assertEqual(q0, automata.state_by_name("q0"))

    def test_get_by_name__existing(self):
        q0 = Node("q0")

        automata = Automata([q0], ['a'], q0, [q0])

        with self.assertRaises(ValueError):
            automata.state_by_name("42")

    def test_reachable_nodes(self):
        q0 = Node("q0")
        q1 = Node("q1")
        q2 = Node("q2")

        q0.add_transition(0, q1)
        q0.add_transition(1, q2)
        q2.add_transition(1, q1)

        self.assertEqual(set([q1, q2]), q0.reachable_nodes())
        self.assertEqual(set([]), q1.reachable_nodes())
        self.assertEqual(set([q1]), q2.reachable_nodes())

    def test_all_states_reachable_from(self):
        q0 = Node('q0')
        q1 = Node('q1')
        q2 = Node('q2')
        symbols = ['a', 'b', 'c', 'd', 'e', 'f']

        q0.add_transition('a', q1)
        q1.add_transition('b', q2)
        q1.add_transition('c', q1)
        q2.add_transition('f', q2)

        tested = Automata([q0, q1, q2], symbols, q0, [q1, q2])

        self.assertEqual(set([q1, q2]), tested.all_states_reachable_from(q0))
        self.assertEqual(set([q1, q2]), tested.all_states_reachable_from(q1))
        self.assertEqual(set([q2]), tested.all_states_reachable_from(q2))

    def test_prune_unreachable_states_simple(self):
        q00 = Node("q00")
        q01 = Node("q01")
        q10 = Node("q10")
        q11 = Node("q11")

        q00.add_transition(0, q11)
        q00.add_transition(1, q11)
        q01.add_transition(0, q10)
        q10.add_transition(0, q01)
        q11.add_transition(0, q00)

        automata = Automata([q00, q01, q10, q11], [0, 1], q00, [q11])

        automata.prune_unreachable_states()

        self.assertIn(q00, automata.states)
        self.assertIn(q11, automata.states)
        self.assertEqual(2, len(automata.states))


class TestModels(TestCase):
    def test_minimize__ejemplo_clase(self):
        q0 = Node('q0')
        q1 = Node('q1')
        q2 = Node('q2')
        q3 = Node('q3')
        q4 = Node('q4')
        q5 = Node('q5')

        q0.add_transition('a', q1)
        q0.add_transition('b', q0)
        q1.add_transition('a', q2)
        q1.add_transition('b', q0)
        q2.add_transition('a', q3)
        q2.add_transition('b', q0)
        q3.add_transition('a', q3)
        q3.add_transition('b', q4)
        q4.add_transition('a', q5)
        q4.add_transition('b', q4)
        q5.add_transition('a', q3)
        q5.add_transition('b', q4)

        symbols = ['a', 'b']
        automata = Automata([q0, q1, q2, q3, q4, q5], symbols, q0, [q3, q4, q5])

        minimized = minimize(automata)
        self.assertEqual(automata.symbols, minimized.symbols)
        self.assertEqual(4, len(minimized.states))

        # Assert implícito de que estas líneas no tiran excepciones
        q0 = minimized.state_by_name("q0")
        q1 = minimized.state_by_name("q1")
        q2 = minimized.state_by_name("q2")
        q3 = minimized.state_by_name("q3")

        self.assertEqual(q0, minimized.initial)
        self.assertEqual([q3], minimized.finals)

        self.assertEqual(symbols, q0.transitions.keys())
        self.assertEqual([q1], q0.transitions['a'])
        self.assertEqual([q0], q0.transitions['b'])
        self.assertEqual(symbols, q1.transitions.keys())
        self.assertEqual([q2], q1.transitions['a'])
        self.assertEqual([q0], q1.transitions['b'])
        self.assertEqual(symbols, q2.transitions.keys())
        self.assertEqual([q3], q2.transitions['a'])
        self.assertEqual([q0], q2.transitions['b'])
        self.assertEqual(symbols, q3.transitions.keys())
        self.assertEqual([q3], q3.transitions['a'])
        self.assertEqual([q3], q3.transitions['b'])

if __name__ == '__main__':
    unittest.main()
