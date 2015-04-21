from models import Automata, Node, LAMBDA
from collections import defaultdict


def load_automata(automata_file):
    states = set()
    for index, line in enumerate(automata_file.readlines()):
        if index == 0:
            for state_name in line.split('\t'):
                state = Node(name=state_name.strip('\n'))
                states.add(state)
        if index == 1:
            symbols = set()
            for symbol in line.split('\t'):
                symbols.add(symbol.strip('\n'))
        if index == 2:
            initial = line.strip('\n')
        if index == 3:
            finals = set()
            for final_state_name in line.split('\t'):
                for state in states:
                    if state.name == final_state_name:
                        finals.add(state)
        if index > 4:
            res = Automata(initial, finals, symbols, states)
            # transitions
            state_1, symbol, state_2 = line.split('\t')
            node_1 = res.state_by_name(state_1)
            node_2 = res.state_by_name(state_2.strip('\n'))
            node_1.add_transition(symbol, node_2)
    return res


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
            deep = len(tabs)
            res[deep].append(('{CONCAT}', number_of_operands))
        elif '{START}' in line:
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
            deep = len(tabs)
            res[deep].append(('{OR}', number_of_operands))
        else:
            deep = line.count('\t')
            res[deep].append(('{SYMBOL}', line.strip('\t').strip('\n')))
    return res


def regex_to_automata(tree_file):
    operand_dict = build_operand_dict(tree_file)

    return build_automata(operand_dict[0][0], 0, operand_dict)


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
        operand = operand_or_symbol_dict[deep + 1]
        operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        operand_automata.final.add_transition(LAMBDA, final)
        operand_automata.final.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, operand_automata.final)

        return Automata(initial, set([final]))
    elif '{PLUS}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        operand = operand_or_symbol_dict[deep + 1]
        operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        operand_automata.final.add_transition(LAMBDA, final)
        operand_automata.final.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, operand_automata.initial)

        return Automata(initial, set([final]))
    elif '{OPT}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        operand = operand_or_symbol_dict[deep + 1]
        operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
        operand_automata.final.add_transition(LAMBDA, final)
        operand_automata.final.add_transition(LAMBDA, initial)
        initial.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, operand_automata.final)

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
        initial=Node()
        final=Node()
        initial.add_transition(symbol, final)
        return Automata(initial, [final])
