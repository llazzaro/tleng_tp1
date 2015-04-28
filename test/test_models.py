# -*- coding: utf-8 -*- 
#!/usr/bin/python

import unittest
from unittest import TestCase

from models import Node, Automata


class TestModels(TestCase):

    def test_is_deterministic_false(self):
        initial=Node()
        final=Node()
        other_node = Node()
        initial.add_transition('a', other_node)
        initial.add_transition('a', final)

        automata=Automata(initial, final)
        self.assertFalse(automata.is_deterministic())
        self.assertEqual(set(automata.states()), set([initial, final, other_node]))
        self.assertEqual(automata.symbols(), set(['a']))

    def test_is_deterministic_true(self):
        initial=Node()
        final=Node()

        initial.add_transition('a', final)

        automata=Automata(initial, final)
        self.assertTrue(automata.is_deterministic())

        self.assertEqual(initial.transition('a'), final)
    
    def test_reachable_states_from(self):
        q0 = Node("q0")
        q1 = Node("q1")

        q0.add_transition(0, q1)
        q0.add_transition(1, q1)
        q1.add_transition(0, q0)

        automata = Automata(q0, q1, set([0, 1]), [q0, q1])

        self.assertEqual(automata.reachable_states_from(q0), set([q1]))
        self.assertEqual(automata.reachable_states_from(q1), set([q0]))
    
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

        automata = Automata(q00, q11, set([0, 1]), [q00, q01, q10, q11])

        automata.prune_unreachable_states()

        self.assertIn(q00, automata.states())
        self.assertIn(q11, automata.states())
        self.assertEqual(2, len(automata.states()))


if __name__ == '__main__':
    unittest.main()
