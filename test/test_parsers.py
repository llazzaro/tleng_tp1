import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import regex_to_automata, load_automata
from models import LAMBDA


class TestParseAutomata(TestCase):

    def test_automata_enunciado(self):
        input_text = 'q0\tq1\tq2\n'
        input_text += 'a\tb\tc\td\te\tf\n'
        input_text += 'q0\n'
        input_text += 'q1\tq2\n'
        input_text += 'q0\ta\tq1\n'
        input_text += 'q1\tb\tq2\n'
        input_text += 'q1\tc\tq1\n'
        input_text += 'q2\tf\tq2'

        file_input = StringIO(input_text)

        result = load_automata(file_input)
        q0 = result.initial
        self.assertEquals(q0.transitions.keys(), ['a'])
        q1 = result.initial.transition('a')
        self.assertEquals(set(q1.transitions.keys()), set(['b', 'c']))
        q2 = result.initial.transition('a').transition('b')
        self.assertEquals(q2.transitions.keys(), ['f'])

        self.assertEquals(result.symbols(), set(['a', 'b', 'c', 'd', 'e', 'f']))
        self.assertEquals(set(result.states()), set([q0, q1, q2]))

    def test_archivo_automata_invalido_lanza_exception_transicion_estado_invalido(self):

        # caso con estados invalivos en transicion
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\n'
        input_text += 'q0\ta\tq1'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

    def test_archivo_automata_invalido_lanza_exception_inicial_final_invalido(self):
        # caso con estado inicial invalido
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q1\n'
        input_text += 'q0\n'
        input_text += 'q0\ta\tq0'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

        # caso con estado final invalido
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\tq1\n'
        input_text += 'q0\ta\tq0'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

    def test_archivo_automata_invalido_lanza_exception_simbolo_transicion_invalido(self):

        # caso con estados invalivos en transicion
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\n'
        input_text += 'q0\tz\tq1'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)


class TestParseRegex(TestCase):

    def test_only_symbol(self):
        input_regex_tree = 'a'
        file_input = StringIO(input_regex_tree)

        result = regex_to_automata(file_input)
        self.assertEquals(result.finals.pop(), result.initial.transitions['a'].pop())

    def test_simple_or(self):
        input_regex_tree = '{OR}2\n\ta\n\tb'
        file_input = StringIO(input_regex_tree)

        result = regex_to_automata(file_input)
        final = result.finals.pop()
        node = result.initial.transitions[LAMBDA].pop()
        node = node.transitions['a'].pop()
        final_node = node.transitions[LAMBDA].pop()
        self.assertEquals(final, final_node)

        node = result.initial.transitions[LAMBDA].pop()
        node = node.transitions['b'].pop()
        self.assertEquals(final, node.transitions[LAMBDA].pop())

    def test_simple_concat(self):
        input_regex_tree = '{CONCAT}2\n\ta\n\tb'
        file_input = StringIO(input_regex_tree)
        result = regex_to_automata(file_input)
        input_regex_tree = '{CONCAT}3\n\tc\n\tb\n\ta'
        file_input = StringIO(input_regex_tree)

        result = regex_to_automata(file_input)
        final = result.finals.pop()
        node = result.initial.transitions[LAMBDA].pop()
        node = node.transitions['c'].pop()
        node = node.transitions[LAMBDA].pop()
        node = node.transitions['b'].pop()
        node = node.transitions[LAMBDA].pop()
        self.assertEquals(final, node.transitions['a'].pop())

    def test_simple_plus(self):
        input_regex_tree = '{PLUS}\n\ta'
        file_input = StringIO(input_regex_tree)

        result = regex_to_automata(file_input)
        self.assertEquals(result.symbols(), set(['a', LAMBDA]))
        self.assertEquals(len(result.states()), 4)
        self.assertEquals(len(result.initial.transitions[LAMBDA]), 2)
        # from_one = result.initial.transitions[LAMBDA].pop()

        # from_two = result.initial.transitions[LAMBDA].pop()

    def test_simple_star(self):
        input_regex_tree = '{STAR}\n\ta'
        file_input = StringIO(input_regex_tree)
        result = regex_to_automata(file_input)
        self.assertEquals(result.symbols(), set(['a', LAMBDA]))
        self.assertEquals(len(result.states()), 4)
        self.assertEquals(len(result.initial.transitions[LAMBDA]), 2)

    def test_simple_opt(self):
        input_regex_tree = '{OPT}\n\ta'
        file_input = StringIO(input_regex_tree)
        result = regex_to_automata(file_input)

        self.assertEquals(result.symbols(), set(['a', LAMBDA]))

    def test_regex_enunciado_1(self):
        pass

    def test_regex_enunciado_2(self):
        pass

if __name__ == '__main__':
    unittest.main()
