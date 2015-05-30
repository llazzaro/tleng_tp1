import unittest
from unittest import TestCase

from models import Node, Automata


class TestEjercicioA(TestCase):
    def test_accept__ejemplo_enunciado(self):
        q0 = Node('q0')
        q1 = Node('q1')
        q2 = Node('q2')
        symbols = ['a', 'b', 'c', 'd', 'e', 'f']

        q0.add_transition('a', q1)
        q1.add_transition('b', q2)
        q1.add_transition('c', q1)
        q2.add_transition('f', q2)

        tested = Automata([q0, q1, q2], symbols, q0, [q1, q2])

        self.assertTrue(tested.accepts("a"))
        self.assertTrue(tested.accepts("ac"))
        self.assertTrue(tested.accepts("accc"))
        self.assertTrue(tested.accepts("ab"))
        self.assertTrue(tested.accepts("acccb"))
        self.assertTrue(tested.accepts("acccbf"))
        self.assertTrue(tested.accepts("acccbfff"))
        self.assertFalse(tested.accepts(""))
        self.assertFalse(tested.accepts("b"))
        self.assertFalse(tested.accepts("c"))
        self.assertFalse(tested.accepts("d"))
        self.assertFalse(tested.accepts("e"))
        self.assertFalse(tested.accepts("f"))
        self.assertFalse(tested.accepts("Z"))
        self.assertFalse(tested.accepts("abb"))
        self.assertFalse(tested.accepts("af"))
        self.assertFalse(tested.accepts("acca"))

if __name__ == '__main__':
    unittest.main()
