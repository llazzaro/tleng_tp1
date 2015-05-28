# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from StringIO import StringIO

from parsers import *
from models import LAMBDA, minimize
from ejercicio_a import nfa_to_dfa


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

    def test_archivo_automata__sin_estados_finales(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\ta\tq0'

        file_input = StringIO(input_text)

        automata = load_automata(file_input)

        self.assertEqual(len(automata.states), 1)
        self.assertEqual(automata.symbols, ['a'])

        q0 = automata.state_by_name("q0")

        self.assertEqual(automata.initial, q0)
        self.assertEqual(automata.finals, [])

        self.assertEqual(q0.transitions.keys(), ['a'])
        self.assertEqual(q0.transitions['a'], [q0])

    def test_archivo_automata__sin_transiciones(self):
        input_text = 'q0\n'
        input_text += 'a\n'
        input_text += 'q0\n'
        input_text += 'q0\n'

        file_input = StringIO(input_text)

        automata = load_automata(file_input)

        self.assertEqual(len(automata.states), 1)
        self.assertEqual(automata.symbols, ['a'])

        q0 = automata.state_by_name("q0")

        self.assertEqual(automata.initial, q0)
        self.assertEqual(automata.finals, [q0])

        self.assertEqual(q0.transitions.keys(), [])


class TestBuildOperandTree(TestCase):
    def test_only_symbol(self):
        input_regex_tree = 'a'

        tree = build_operand_tree(StringIO(input_regex_tree))
        
        self.assertTrue(isinstance(tree, Symbol))
        self.assertEqual('a', tree.content)

    def test_only_concat(self):
        input_regex_tree = "{CONCAT}2\n"
        input_regex_tree += "\ta\n"
        input_regex_tree += "\tb\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Concat))
        self.assertTrue(isinstance(tree.content, list))
        self.assertEqual(2, len(tree.content))
        content = tree.content
        self.assertTrue(isinstance(content[0], Symbol))
        self.assertEqual('a', content[0].content)
        self.assertTrue(isinstance(content[1], Symbol))
        self.assertEqual('b', content[1].content)

    def test_only_or(self):
        input_regex_tree = "{OR}2\n"
        input_regex_tree += "\ta\n"
        input_regex_tree += "\tb\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Or))
        self.assertTrue(isinstance(tree.content, list))
        self.assertEqual(2, len(tree.content))
        content = tree.content
        self.assertTrue(isinstance(content[0], Symbol))
        self.assertEqual('a', content[0].content)
        self.assertTrue(isinstance(content[1], Symbol))
        self.assertEqual('b', content[1].content)

    def test_only_star(self):
        input_regex_tree = "{STAR}\n"
        input_regex_tree += "\ta\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Star))
        self.assertTrue(isinstance(tree.content, Symbol))
        self.assertEqual('a', tree.content.content)

    def test_only_plus(self):
        input_regex_tree = "{PLUS}\n"
        input_regex_tree += "\ta\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Plus))
        self.assertTrue(isinstance(tree.content, Symbol))
        self.assertEqual('a', tree.content.content)
    
    def test_only_plus(self):
        input_regex_tree = "{OPT}\n"
        input_regex_tree += "\ta\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Opt))
        self.assertTrue(isinstance(tree.content, Symbol))
        self.assertEqual('a', tree.content.content)
    
    def test_ejemplo_uno_enunciado(self):
        input_regex_tree = "{CONCAT}3\n"
        input_regex_tree += "\t{STAR}\n"
        input_regex_tree += "\t\t{OR}3\n"
        input_regex_tree += "\t\t\ta\n"
        input_regex_tree += "\t\t\tb\n"
        input_regex_tree += "\t\t\tc\n"
        input_regex_tree += "\t{PLUS}\n"
        input_regex_tree += "\t\t{CONCAT}2\n"
        input_regex_tree += "\t\t\td\n"
        input_regex_tree += "\t\t\te\n"
        input_regex_tree += "\tf\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Concat))
        self.assertTrue(isinstance(tree.content, list))
        self.assertEqual(3, len(tree.content))
        concat_content = tree.content
        self.assertTrue(isinstance(concat_content[0], Star))
        self.assertTrue(isinstance(concat_content[1], Plus))
        self.assertTrue(isinstance(concat_content[2], Symbol))
        
        star_content = concat_content[0].content
        self.assertTrue(isinstance(star_content, Or))

        or_content = star_content.content
        self.assertTrue(isinstance(or_content, list))
        self.assertEqual(3, len(or_content))
        self.assertTrue(isinstance(or_content[0], Symbol))
        self.assertTrue(isinstance(or_content[1], Symbol))
        self.assertTrue(isinstance(or_content[2], Symbol))
        self.assertEqual('a', or_content[0].content)
        self.assertEqual('b', or_content[1].content)
        self.assertEqual('c', or_content[2].content)

        plus_content = concat_content[1].content
        self.assertTrue(isinstance(plus_content, Concat))
        concat2_content = plus_content.content
        self.assertEqual(2, len(concat2_content))
        self.assertTrue(isinstance(concat2_content[0], Symbol))
        self.assertTrue(isinstance(concat2_content[1], Symbol))
        self.assertEqual('d', concat2_content[0].content)
        self.assertEqual('e', concat2_content[1].content)

        self.assertEqual('f', concat_content[2].content)
    
    def test_ejemplo_dos_enunciado(self):
        input_regex_tree = "{CONCAT}3\n"
        input_regex_tree += "\t{OPT}\n"
        input_regex_tree += "\t\t{CONCAT}4\n"
        input_regex_tree += "\t\t\t-\n"
        input_regex_tree += "\t\t\tA\n"
        input_regex_tree += "\t\t\tB\n"
        input_regex_tree += "\t\t\tC\n"
        input_regex_tree += "\t{PLUS}\n"
        input_regex_tree += "\t\t{OR}2\n"
        input_regex_tree += "\t\t\t0\n"
        input_regex_tree += "\t\t\t1\n"
        input_regex_tree += "\t{STAR}\n"
        input_regex_tree += "\t\t\\t\n"

        tree = build_operand_tree(StringIO(input_regex_tree))

        self.assertTrue(isinstance(tree, Concat))
        self.assertTrue(isinstance(tree.content, list))
        self.assertEqual(3, len(tree.content))
        concat_content = tree.content
        self.assertTrue(isinstance(concat_content[0], Opt))
        self.assertTrue(isinstance(concat_content[1], Plus))
        self.assertTrue(isinstance(concat_content[2], Star))
        
        opt_content = concat_content[0].content
        self.assertTrue(isinstance(opt_content, Concat))

        concat2_content = opt_content.content
        self.assertTrue(isinstance(concat2_content, list))
        self.assertEqual(4, len(concat2_content))
        self.assertTrue(isinstance(concat2_content[0], Symbol))
        self.assertTrue(isinstance(concat2_content[1], Symbol))
        self.assertTrue(isinstance(concat2_content[2], Symbol))
        self.assertTrue(isinstance(concat2_content[3], Symbol))
        self.assertEqual('-', concat2_content[0].content)
        self.assertEqual('A', concat2_content[1].content)
        self.assertEqual('B', concat2_content[2].content)
        self.assertEqual('C', concat2_content[3].content)

        plus_content = concat_content[1].content
        self.assertTrue(isinstance(plus_content, Or))
        or_content = plus_content.content
        self.assertEqual(2, len(or_content))
        self.assertTrue(isinstance(or_content[0], Symbol))
        self.assertTrue(isinstance(or_content[1], Symbol))
        self.assertEqual('0', or_content[0].content)
        self.assertEqual('1', or_content[1].content)

        star_content = concat_content[2].content
        self.assertTrue(isinstance(star_content, Symbol))
        self.assertEqual('\\t', star_content.content)

    def test__too_many_characters(self):
        input_regex_tree = '*s'
        
        with self.assertRaises(ValueError):
            tree = build_operand_tree(StringIO(input_regex_tree))
    
    def test__invalid_characters(self):
        input_regex_tree = '*'
        
        with self.assertRaises(ValueError):
            tree = build_operand_tree(StringIO(input_regex_tree))

    def test__too_many_subexpressions_single_expected_eof(self):
        input_regex_tree = "{STAR}\n"
        input_regex_tree += "\tA\n"
        input_regex_tree += "\tB\n"

        with self.assertRaises(Exception):
            tree = build_operand_tree(StringIO(input_regex_tree))

    def test__too_many_subexpressions_than_expected_no_EOF(self):
        input_regex_tree = "{CONCAT}2\n"
        input_regex_tree += "\t{STAR}\n"
        input_regex_tree += "\t\tA\n"
        input_regex_tree += "\t\tB\n"
        input_regex_tree += "\tC\n"

        with self.assertRaises(Exception):
            tree = build_operand_tree(StringIO(input_regex_tree))

    def test__not_enough_subexpressions(self):
        input_regex_tree = "{CONCAT}1\n"
        input_regex_tree += "\tA\n"

        with self.assertRaises(Exception):
            tree = build_operand_tree(StringIO(input_regex_tree))

    def test__less_subexpressions_than_expected_EOF(self):
        input_regex_tree = "{CONCAT}3\n"
        input_regex_tree += "\tA\n"
        input_regex_tree += "\tB\n"

        with self.assertRaises(Exception):
            tree = build_operand_tree(StringIO(input_regex_tree))

    def test__less_subexpressions_than_expected_no_EOF(self):
        input_regex_tree = "{CONCAT}2\n"
        input_regex_tree += "\t{CONCAT}3\n"
        input_regex_tree += "\t\tA\n"
        input_regex_tree += "\t\tB\n"
        input_regex_tree += "\tC\n"

        with self.assertRaises(Exception):
            tree = build_operand_tree(StringIO(input_regex_tree))

class TestRegexTreeToNFA(TestCase):
    def test_symbol_to_automata(self):
        tree = Symbol('a')

        tested = tree.to_automata()

        self.assertEqual(['a'], tested.symbols)
        self.assertEqual(2, len(tested.states))
        self.assertEqual([tested.initial.transition('a')], tested.finals)

    def test_star_to_automata(self):
        tree = Star(Symbol('a'))

        tested = tree.to_automata()
        self.assertEqual(['a'], tested.symbols)
        self.assertEqual(4, len(tested.states))

        # FIXME: Mal testeo 
        dfa_tested = nfa_to_dfa(tested)
        self.assertTrue(dfa_tested.accepts(""))
        self.assertTrue(dfa_tested.accepts("a"))
        self.assertTrue(dfa_tested.accepts("aa"))
        self.assertTrue(dfa_tested.accepts("aaa"))

    def test_plus_to_automata(self):
        tree = Plus(Symbol('a'))

        tested = tree.to_automata()
        self.assertEqual(['a'], tested.symbols)
        #self.assertEqual(4, len(tested.states))

        # FIXME: Mal testeo
        dfa_tested = nfa_to_dfa(tested)
        self.assertFalse(dfa_tested.accepts(""))
        self.assertTrue(dfa_tested.accepts("a"))
        self.assertTrue(dfa_tested.accepts("aa"))
        self.assertTrue(dfa_tested.accepts("aaa"))

    def test_opt_to_automata(self):
        tree = Opt(Symbol('a'))

        tested = tree.to_automata()
        self.assertEqual(['a'], tested.symbols)
        #self.assertEqual(4, len(tested.states))

        # FIXME: Mal testeo
        dfa_tested = nfa_to_dfa(tested)
        self.assertTrue(dfa_tested.accepts(""))
        self.assertTrue(dfa_tested.accepts("a"))
        self.assertFalse(dfa_tested.accepts("aa"))
        self.assertFalse(dfa_tested.accepts("aaa"))

    def test_concat_to_automata(self):
        tree = Concat([Symbol('a'), Symbol('b')])

        tested = tree.to_automata()
        self.assertEqual(['a', 'b'], tested.symbols)
        self.assertEqual(4, len(tested.states))

        # FIXME: Mal testeo
        dfa_tested = nfa_to_dfa(tested)
        self.assertTrue(dfa_tested.accepts("ab"))
        self.assertFalse(dfa_tested.accepts("ba"))
        self.assertFalse(dfa_tested.accepts(""))
        self.assertFalse(dfa_tested.accepts("a"))
        self.assertFalse(dfa_tested.accepts("aa"))
        self.assertFalse(dfa_tested.accepts("aaa"))
        self.assertFalse(dfa_tested.accepts("b"))
        self.assertFalse(dfa_tested.accepts("bb"))
        self.assertFalse(dfa_tested.accepts("bbb"))

    def test_or_to_automata(self):
        tree = Or([Symbol('a'), Symbol('b')])

        tested = tree.to_automata()
        self.assertEqual(['a', 'b'], tested.symbols)


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
