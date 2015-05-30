#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase

from StringIO import StringIO
from models import (
    Node,
    LAMBDA,
    Automata,
    UnexpectedSymbolOnStateException,
    FinalsNotInStatesException,
    add_terminal_node,
    minimize,
)
from parsers import load_automata


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

        self.assertFalse(s in tested.transitions)
        tested.add_transition(s, target)

        self.assertTrue(s in tested.transitions)
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
        symbols = ['a']
        automata = Automata(states, symbols, initial, [final])

        self.assertEqual(states, automata.states)
        self.assertEqual(symbols, automata.symbols)
        self.assertEqual(initial, automata.initial)
        self.assertEqual([final], automata.finals)

        self.assertFalse(automata.is_deterministic())
        self.assertTrue(automata.has_lambda())

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
            Automata(states, symbols, initial, [final])

    def test_construction_automata__invalid_final(self):
        initial = Node()
        final = Node()
        initial.add_transition('a', final)

        states = [initial, final]
        symbols = ['a']

        with self.assertRaises(FinalsNotInStatesException):
            Automata(states, symbols, initial, [Node()])

    def test_construction_automata__extra_final(self):
        initial = Node()
        final = Node()
        initial.add_transition('a', final)

        states = [initial, final]
        symbols = ['a']

        with self.assertRaises(FinalsNotInStatesException):
            Automata(states, symbols, initial, [final, Node()])

    def test_is_deterministic_automata__lambda_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition(LAMBDA, final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_deterministic())
        self.assertTrue(automata.has_lambda())

    def test_is_deterministic_automata__not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_deterministic())
        self.assertFalse(automata.has_lambda())

    def test_is_deterministic_automata__lambda_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_deterministic())
        self.assertTrue(automata.has_lambda())

    def test_is_deterministic_automata__det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertTrue(automata.is_deterministic())
        self.assertFalse(automata.has_lambda())

    def test_is_lambda_deterministic_automata__lambda_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        other_node.add_transition(LAMBDA, final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_lambda_deterministic())
        self.assertTrue(automata.has_lambda())

    def test_is_lambda_deterministic_automata_not_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertFalse(automata.is_lambda_deterministic())
        self.assertFalse(automata.has_lambda())

    def test_is_lambda_deterministic_automata__lambda_det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertTrue(automata.is_lambda_deterministic())
        self.assertTrue(automata.has_lambda())

    def test_is_lambda_deterministic_automata__det(self):
        initial = Node()
        final = Node()
        other_node = Node()
        initial.add_transition(LAMBDA, other_node)
        initial.add_transition('a', final)
        automata = Automata([initial, final, other_node], ['a'], initial, [final])

        self.assertTrue(automata.is_lambda_deterministic())
        self.assertTrue(automata.has_lambda())

    def test_get_by_name__existing(self):
        q0 = Node("q0")

        automata = Automata([q0], ['a'], q0, [q0])

        self.assertEqual(q0, automata.state_by_name("q0"))

    def test_get_by_name__existing_2(self):
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
    def test_add_terminal_node__ejemplo_simple(self):
        q0 = Node('q0')
        q1 = Node('q1')
        q2 = Node('q2')

        q0.add_transition('a', q1)
        q1.add_transition('b', q2)
        q2.add_transition('a', q2)
        q2.add_transition('b', q2)

        symbols = ['a', 'b']
        automata = Automata([q0, q1, q2], symbols, q0, [q2])

        with_terminal_node = add_terminal_node(automata)

        self.assertEqual(automata.symbols, with_terminal_node.symbols)
        self.assertEqual(len(automata.states) + 1, len(with_terminal_node.states))

        q0T = with_terminal_node.state_by_name("q0")
        q1T = with_terminal_node.state_by_name("q1")
        q2T = with_terminal_node.state_by_name("q2")
        qT = with_terminal_node.state_by_name("qT")

        self.assertEqual(symbols, q0T.transitions.keys())
        self.assertEqual([q1T], q0T.transitions['a'])
        self.assertEqual([qT], q0T.transitions['b'])
        self.assertEqual(symbols, q1T.transitions.keys())
        self.assertEqual([qT], q1T.transitions['a'])
        self.assertEqual([q2T], q1T.transitions['b'])
        self.assertEqual(symbols, q2T.transitions.keys())
        self.assertEqual([q2T], q2T.transitions['a'])
        self.assertEqual([q2T], q2T.transitions['b'])
        self.assertEqual(symbols, qT.transitions.keys())
        self.assertEqual([qT], qT.transitions['a'])
        self.assertEqual([qT], qT.transitions['b'])


class TestMinimize(TestCase):
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

    # FIXME: reescribir evitando el load_automata y rechequeando
    def test_minimize__example_from_hopcroft(self):
        """
            basado en la figura 4.10 del libro
        """
        state_c = Node(name='c')
        state_d = Node(name='d')
        state_e = Node(name='e')

        state_c.add_transition('0', state_d)
        state_c.add_transition('1', state_e)

        state_d.add_transition('0', state_d)
        state_d.add_transition('1', state_e)

        state_e.add_transition('1', state_e)
        state_e.add_transition('0', state_c)

        finals = [state_c, state_d]

        states = [state_c, state_d, state_e]
        symbols = ['0', '1']

        not_minimized = Automata(states, symbols, state_c, finals)

        minimized = minimize(not_minimized)

        # save_dot(minimized, open('hopcroft_410.dot', 'w'))

        self.assertEquals(len(minimized.states), 2)
        self.assertTrue(LAMBDA not in minimized.symbols)
        self.assertEquals(minimized.symbols, not_minimized.symbols)
        self.assertEquals(minimized.initial.transition('0'), minimized.initial)
        other_node = minimized.initial.transition('1')
        self.assertEquals(minimized.initial.transition('1').transition('0'), minimized.initial)
        self.assertEquals(minimized.initial.transition('1'), other_node)
        self.assertEquals(minimized.initial.transition('1').transition('1'), other_node)

    def test_wikipedia_example_minimization(self):
        state_a = Node(name='a')
        state_b = Node(name='b')
        state_c = Node(name='c')
        state_d = Node(name='d')
        state_e = Node(name='e')
        state_f = Node(name='f')

        state_a.add_transition('0', state_b)
        state_a.add_transition('1', state_c)
        state_b.add_transition('0', state_a)
        state_b.add_transition('1', state_d)
        state_c.add_transition('0', state_e)
        state_c.add_transition('1', state_f)
        state_d.add_transition('0', state_e)
        state_d.add_transition('1', state_f)
        state_e.add_transition('0', state_e)
        state_e.add_transition('1', state_f)
        state_f.add_transition('0', state_f)
        state_f.add_transition('1', state_f)

        automata = Automata([state_a, state_b, state_c, state_d, state_e, state_f], ['0', '1'], state_a, [state_c, state_d, state_e])
        minimized = minimize(automata)

        self.assertEqual(automata.symbols, minimized.symbols)
        self.assertEqual(2, len(minimized.states))

        q0 = minimized.state_by_name("q0")
        q1 = minimized.state_by_name("q1")

        self.assertEqual(q0, minimized.initial)
        self.assertEqual([q1], minimized.finals)

        self.assertEqual(q0, q0.transition('0'))
        self.assertEqual(q1, q0.transition('1'))
        self.assertEqual(q1, q1.transition('0'))

    # FIXME: reescribir evitando el load_automata y rechequeando
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

    def test_minimize__con_nodo_trampa(self):
        q0 = Node('q0')
        q1 = Node('q1')
        qT = Node('qT')

        q0.add_transition('0', q1)
        q0.add_transition('0', qT)
        q0.add_transition('1', qT)
        q1.add_transition('0', qT)
        q1.add_transition('0', qT)
        qT.add_transition('0', qT)
        qT.add_transition('1', qT)

        automata = Automata([q0, q1, qT], ['0', '1'], q0, [q1])
        minimized = minimize(automata)

        self.assertEquals(set(minimized.symbols), set(automata.symbols))
        self.assertEquals(len(minimized.states), 2)

        q0 = minimized.state_by_name('q0')
        q1 = minimized.state_by_name('q1')

        self.assertEquals(q0.transition('0'), q1)
        self.assertEquals(q0.transitions.keys(), ['0'])
        self.assertEquals(q1.transitions.keys(), [])


if __name__ == '__main__':
    unittest.main()
