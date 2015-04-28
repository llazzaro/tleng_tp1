from unittest import TestCase
from StringIO import StringIO

from ejercicio_f import equivalentes


class TestEjercicioF(TestCase):

    def test_equivalentes_hopcroft_figure_410(self):
        input_automata = '\t'.join(['c', 'd', 'e']) + '\n'
        input_automata += '\t'.join(['0', '1']) + '\n'
        input_automata += 'c\n'
        input_automata += '\t'.join(['c', 'd']) + '\n'
        input_automata += '\t'.join(['c', '0', 'd']) + '\n'
        input_automata += '\t'.join(['c', '1', 'e']) + '\n'
        input_automata += '\t'.join(['d', '0', 'd']) + '\n'
        input_automata += '\t'.join(['d', '1', 'e']) + '\n'
        input_automata += '\t'.join(['e', '1', 'e']) + '\n'
        input_automata += '\t'.join(['e', '0', 'c'])

        other_aut = '\t'.join(['a', 'b']) + '\n'
        other_aut += '\t'.join(['0', '1']) + '\n'
        other_aut += 'a\n'
        other_aut += 'a\n'
        other_aut += '\t'.join(['a', '1', 'b']) + '\n'
        other_aut += '\t'.join(['a', '0', 'a']) + '\n'
        other_aut += '\t'.join(['b', '1', 'b']) + '\n'
        other_aut += '\t'.join(['b', '0', 'a'])

        res = equivalentes(StringIO(input_automata), StringIO(other_aut))

        self.assertTrue(res)
