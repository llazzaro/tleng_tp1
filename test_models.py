import unittest
from unittest import TestCase

from models import Node, Automata


class TestParseRegex(TestCase):

    def test_is_deterministic_false(self):
        initial=Node()
        final=Node()
        initial.transitions['a'].append(Node())
        initial.transitions['a'].append(final)

        automata=Automata(initial, final)
        self.assertFalse(automata.is_deterministic())

    def test_is_deterministic_true(self):
        initial=Node()
        final=Node()

        initial.transitions['a'].append(final)

        automata=Automata(initial, final)
        self.assertTrue(automata.is_deterministic())

if __name__ == '__main__':
    unittest.main()
