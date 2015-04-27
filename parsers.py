# -*- coding: utf-8 -*-

import string
from models import Automata, Node, LAMBDA
from collections import defaultdict


def load_automata(automata_file):
    states = set()
    res = None
    for index, line in enumerate(automata_file.readlines()):
        if index == 0:
            # se cargan los states
            for state_name in line.split('\t'):
                state = Node(name=state_name.strip('\n'))
                states.add(state)
            valid_state_names = map(lambda state: state.name, states)
        if index == 1:
            # symbols
            symbols = set()
            for symbol in line.split('\t'):
                symbols.add(symbol.strip('\n'))
        if index == 2:
            # linea correspondiente al estado inicial
            initial_name = line.strip('\n')
            if initial_name not in map(lambda state: state.name, states):
                raise Exception('El estado inicial no es valido. no se encuentra en la lista de estados validos')
        if index == 3:
            # estados finales
            finals = set()
            for final_state_name in line.split('\t'):
                final_state_name = final_state_name.strip('\n')
                if final_state_name not in valid_state_names:
                    raise Exception('Formato invalido. Estado final esta en la lista de estados validos')
                for state in states:
                    if state.name == final_state_name.strip('\n'):
                        finals.add(state)
        if index >= 4:
            # ejes del grafo
            for state in states:
                if initial_name == state.name:
                    initial = state
                    break
            res = Automata(initial, finals, symbols, states)
            # transitions
            state_1, symbol, state_2 = line.split('\t')
            state_1 = state_1.strip('\n')
            state_2 = state_2.strip('\n')

            if state_1 not in valid_state_names or state_2 not in valid_state_names:
                raise Exception('Se detecto un estado invalido en la informaci\'on de ejes')
            if symbol not in symbols:
                raise Exception('Simbolo {0} en la transici\'on es invalido'.format(symbol))

            node_1 = res.state_by_name(state_1)
            node_2 = res.state_by_name(state_2.strip('\n'))

            node_1.add_transition(symbol, node_2)
    return res


def verify_integrity(res):
    """
        Revisa si para los op que tienen numero de operandos,
        este numero es valido (si hay dos param hay dos ni mas ni menos)

        si encuentra algo que esta mal lanza exception
    """

    for deep, list_of_op in res.iteritems():
        for op, number_of_operands in list_of_op:
            if op in ['{CONCAT}', '{OR}']:
                if len(res[deep + 1]) != number_of_operands:
                    raise Exception('{2} requiere {0} paramteros, se encontro solamente {1} parametros'.format(len(res[deep + 1]), number_of_operands, op))


def build_operand_dict(tree_file):
    """
        this function will return a list of "new" files
        that will we used for recurive calls with smaller
        tree.
    """
    res = defaultdict(list)
    for line in tree_file.readlines():
        if '{CONCAT}' in line:
            tabs, number_of_operands = line.split('{CONCAT}')
            number_of_operands = int(number_of_operands.strip('\n'))
            deep = len(tabs)
            res[deep].append(('{CONCAT}', number_of_operands))
        elif '{STAR}' in line:
            tabs, _ = line.split('{STAR}')
            deep = len(tabs)
            res[deep].append(('{STAR}', None))
        elif '{PLUS}' in line:
            tabs, _ = line.split('{PLUS}')
            deep = len(tabs)
            res[deep].append(('{PLUS}', None))
        elif '{OPT}' in line:
            tabs, _ = line.split('{OPT}')
            deep = len(tabs)
            res[deep].append(('{OPT}', None))
        elif '{OR}' in line:
            tabs, number_of_operands = line.split('{OR}')
            number_of_operands = int(number_of_operands.strip('\n'))
            deep = len(tabs)
            res[deep].append(('{OR}', number_of_operands))
        else:
            deep = line.count('\t')
            res[deep].append(('{SYMBOL}', line.strip('\t').strip('\n')))
    verify_integrity(res)
    return res


def regex_to_automata(tree_file):
    operand_dict = build_operand_dict(tree_file)
    res = build_automata(operand_dict[0][0], 0, operand_dict)

    return res


def build_automata(current_operand_or_symbol, deep, operand_or_symbol_dict):
    if '{CONCAT}' == current_operand_or_symbol[0]:
        initial = Node()
        next_node = None
        operand_or_symbols = operand_or_symbol_dict[deep + 1]
        operand_or_symbols.reverse()
        for operand in operand_or_symbols:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            if next_node:
                for final in operand_automata.finals:
                    final.add_transition(LAMBDA, next_node)
            else:
                finals = operand_automata.finals
            next_node = operand_automata.initial

        initial.add_transition(LAMBDA, next_node)
        return Automata(initial, finals)
    elif '{STAR}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        for operand in operand_or_symbol_dict[deep + 1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
            dfa_final.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, operand_automata.initial)
        for final in operand_automata.finals:
            initial.add_transition(LAMBDA, final)

        return Automata(initial, set([final]))
    elif '{PLUS}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        for operand in operand_or_symbol_dict[deep + 1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
            initial.add_transition(LAMBDA, dfa_final)

        initial.add_transition(LAMBDA, operand_automata.initial)

        return Automata(initial, set([final]))
    elif '{OPT}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()

        for operand in operand_or_symbol_dict[deep + 1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
            dfa_final.add_transition(LAMBDA, initial)
        initial.add_transition(LAMBDA, operand_automata.initial)
        for final in operand_automata.finals:
            initial.add_transition(LAMBDA, final)

        return Automata(initial, set([final]))
    elif '{OR}' in current_operand_or_symbol[0]:
        initial = Node()
        new_final = Node()

        for operand in operand_or_symbol_dict[deep + 1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            initial.add_transition(LAMBDA, operand_automata.initial)
            for final in operand_automata.finals:
                final.add_transition(LAMBDA, new_final)

        return Automata(initial, set([new_final]))
    else:
        # simbolo alfabeto
        assert current_operand_or_symbol[0] == '{SYMBOL}'
        symbol=current_operand_or_symbol[1]
        assert symbol in string.letters + '([,:;.¿?!¡()"’\&-] \t'
        initial=Node()
        final=Node()
        initial.add_transition(symbol, final)
        return Automata(initial, [final])
