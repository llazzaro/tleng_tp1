# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import regex_to_automata, load_automata
from ejercicio_a import minimize
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

        self.assertEqual(len(result.states), 3)
        self.assertEqual(result.symbols, ['a', 'b', 'c', 'd', 'e', 'f'])

        # Assert implícito de que estas tres líneas no tiran excepciones
        q0 = result.state_by_name("q0")
        q1 = result.state_by_name("q1")
        q2 = result.state_by_name("q2")

        self.assertEqual(result.initial, q0)
        self.assertEqual(result.finals, [q1, q2])

        self.assertEqual(q0.transitions.keys(), ['a'])
        self.assertEqual(q0.transitions['a'], [q1])
        #Convierto a set para ignorar el orden en la lista
        self.assertEqual(set(q1.transitions.keys()), set(['b', 'c']))
        self.assertEqual(q1.transitions['b'], [q2])
        self.assertEqual(q1.transitions['c'], [q1])
        self.assertEqual(q2.transitions.keys(), ['f'])
        self.assertEqual(q2.transitions['f'], [q2])


    def test_archivo_automata__transicion_estado_invalido(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\n'
        input_text += 'q0\ta\tq1'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

    def test_archivo_automata__inicial_invalido(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q1\n'
        input_text += 'q0\n'
        input_text += 'q0\ta\tq0'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

    def test_archivo_automata__final_invalido(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\tq1\n'
        input_text += 'q0\ta\tq0'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)

    def test_archivo_automata__simbolo_transicion_invalido(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\n'
        input_text += 'q0\tz\tq1'

        file_input = StringIO(input_text)

        with self.assertRaises(Exception):
            load_automata(file_input)


#class TestParseRegex(TestCase):
#
#    def test_only_symbol(self):
#        input_regex_tree = 'a'
#        file_input = StringIO(input_regex_tree)
#
#        result = regex_to_automata(file_input)
#        self.assertEquals(result.finals.pop(), result.initial.transitions['a'].pop())
#
#    def test_other_symbols(self):
#        for symbol in '([,:;.¿?!¡()"\'\&-]':
#            input_regex_tree = symbol
#            file_input = StringIO(input_regex_tree)
#
#            result = regex_to_automata(file_input)
#            self.assertEquals(result.finals.pop(), result.initial.transitions[symbol].pop())
#
#    def test_simple_or(self):
#        input_regex_tree = '{OR}2\n\ta\n\tb'
#        file_input = StringIO(input_regex_tree)
#
#        result = regex_to_automata(file_input)
#        final = result.finals.pop()
#        node = result.initial.transitions[LAMBDA].pop()
#        node = node.transitions['a'].pop()
#        final_node = node.transitions[LAMBDA].pop()
#        self.assertEquals(final, final_node)
#
#        node = result.initial.transitions[LAMBDA].pop()
#        node = node.transitions['b'].pop()
#        self.assertEquals(final, node.transitions[LAMBDA].pop())
#
#    def test_simple_concat(self):
#        input_regex_tree = '{CONCAT}2\n\ta\n\tb'
#        file_input = StringIO(input_regex_tree)
#        result = regex_to_automata(file_input)
#        input_regex_tree = '{CONCAT}3\n\tc\n\tb\n\ta'
#        file_input = StringIO(input_regex_tree)
#
#        result = regex_to_automata(file_input)
#        final = result.finals.pop()
#        node = result.initial
#        node = node.transitions['c'].pop()
#        node = node.transitions[LAMBDA].pop()
#        node = node.transitions['b'].pop()
#        node = node.transitions[LAMBDA].pop()
#        self.assertEquals(final, node.transitions['a'].pop())
#
#    def test_simple_plus(self):
#        input_regex_tree = '{PLUS}\n\ta'
#        file_input = StringIO(input_regex_tree)
#
#        result = regex_to_automata(file_input)
#        self.assertEquals(result.symbols(), set(['a']))
#        self.assertEquals(len(result.states()), 4)
#        self.assertEquals(len(result.initial.transitions[LAMBDA]), 1)
#        # from_one = result.initial.transitions[LAMBDA].pop()
#
#        # from_two = result.initial.transitions[LAMBDA].pop()
#
#    def test_simple_star(self):
#        input_regex_tree = '{STAR}\n\ta'
#        file_input = StringIO(input_regex_tree)
#        result = regex_to_automata(file_input)
#        self.assertEquals(result.symbols(), set(['a']))
#        self.assertEquals(len(result.states()), 4)
#        self.assertEquals(len(result.initial.transitions[LAMBDA]), 2)
#        self.assertTrue(result.initial.transition('@') in result.initial.transition('@').transition('a').transitions.values()[0])
#
#    def test_simple_opt(self):
#        input_regex_tree = '{OPT}\n\ta'
#        file_input = StringIO(input_regex_tree)
#        result = regex_to_automata(file_input)
#
#        self.assertEquals(result.symbols(), set(['a']))
#        self.assertEquals(len(result.initial.transitions[LAMBDA]), 2)
#
#    def test_regex_enunciado_1(self):
#        # '(a|b|c)*(de)+f'
#        file_input = '{CONCAT}3\n'
#        file_input += '\t{STAR}\n'
#        file_input += '\t\t{OR}3\n'
#        file_input += '\t\t\ta\n'
#        file_input += '\t\t\tb\n'
#        file_input += '\t\t\tc\n'
#        file_input += '\t{PLUS}\n'
#        file_input += '\t\t{CONCAT}2\n'
#        file_input += '\t\t\td\n'
#        file_input += '\t\t\te\n'
#        file_input += '\tf'
#
#        file_input = StringIO(file_input)
#
#        result = regex_to_automata(file_input)
#        self.assertTrue(result.symbols, set(['a', 'b', 'c', 'd', 'e', 'f']))
#
#    def test_bug_simple(self):
#        """
#            El segundo OR usa los param del primero. este test verifica que no pase esto
#        """
#        file_input = '{CONCAT}2\n'
#        file_input += '\t{OR}2\n'
#        file_input += '\t\ta\n'
#        file_input += '\t\tb\n'
#        file_input += '\t{OR}2\n'
#        file_input += '\t\tc\n'
#        file_input += '\t\td'
#        file_input = StringIO(file_input)
#        result = regex_to_automata(file_input)
#        self.assertEquals(len(result.states()), 12)
#        self.assertEquals(len(result.finals), 1)
#        minimized = minimize(result)
#        self.assertEquals(result.symbols(), minimized.symbols())
#
#    def test_regex_enunciado_2(self):
#        # '(-ABC)?(0|1)+\t*'
#        # file_input = StringIO('(-ABC)?(0|1)+\t*')
#        # result = regex_to_automata(file_input)
#        file_input = '{CONCAT}3\n'
#        file_input += '\t{OPT}\n'
#        file_input += '\t\t{CONCAT}4\n'
#        file_input += '\t\t\t-\n'
#        file_input += '\t\t\tA\n'
#        file_input += '\t\t\tB\n'
#        file_input += '\t\t\tC\n'
#        file_input += '\t{PLUS}\n'
#        file_input += '\t\t{OR}2\n'
#        file_input += '\t\t\t0\n'
#        file_input += '\t\t\t1\n'
#        file_input += '\t{STAR}\n'
#        file_input += '\t\t\t'
#
#        file_input = StringIO(file_input)
#        result = regex_to_automata(file_input)
#        self.assertEquals(len(result.states()), 22)
#        minimized = minimize(result)
#        self.assertTrue(LAMBDA not in minimized.symbols())
#        self.assertEquals(result.symbols(), minimized.symbols())
#
#    def test_simple_invalid_or(self):
#        input_regex_tree = '{OR}3\n\ta\n\tb'
#        file_input = StringIO(input_regex_tree)
#
#        with self.assertRaises(Exception):
#            regex_to_automata(file_input)
#
#    def test_invalid_symbol(self):
#        input_regex_tree = 'á'
#        file_input = StringIO(input_regex_tree)
#
#        with self.assertRaises(Exception):
#            regex_to_automata(file_input)


if __name__ == '__main__':
    unittest.main()
