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
        self.assertEquals(automata.states, set([initial, final, other_node]))
        self.assertEquals(automata.symbols, set(['a']))

    def test_is_deterministic_true(self):
        initial=Node()
        final=Node()

        initial.add_transition('a', final)

        automata=Automata(initial, final)
        self.assertTrue(automata.is_deterministic())

        self.assertEquals(initial.transition('a'), final)

if __name__ == '__main__':
    unittest.main()
