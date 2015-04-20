from models import Automata, Node, LAMBDA
from collections import defaultdict


def load_automata(automata_file):
    res = Automata()
    for index, line in enumerate(automata_file.readlines()):
        if index == 0:
            for state_name in line.split('\t'):
                state = Node(name=state_name)
                res.add_state(state)
        if index == 1:
            for symbol in line.split('\t'):
                res.add_symbol(symbol)
        if index == 2:
            res.initial = line.strip('\n')
        if index == 3:
            for final_state_name in line.split('\t'):
                res.set_final_state(final_state_name)
        if index > 4:
            # transitions
            state_1, symbol, state_2 = line.split('\t')
            node_1 = res.state_by_name(state_1)
            node_2 = res.state_by_name(state_2)
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
            tabs, number_of_operands = line.split('{START}')
            deep = len(tabs)
            res[deep].append(('{START}', number_of_operands))
        elif '{PLUS}' in line:
            tabs, number_of_operands = line.split('{PLUS}')
            deep = len(tabs)
            res[deep].append(('{PLUS}', number_of_operands))
            pass
        elif '{OPT}' in line:
            tabs, number_of_operands = line.split('{OPT}')
            deep = len(tabs)
            res[deep].append(('{OPT}', number_of_operands))
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
    elif '{START}' in current_operand_or_symbol[0]:
        raise NotImplementedError
    elif '{PLUS}' in current_operand_or_symbol[0]:
        raise NotImplementedError
    elif '{OPT}' in current_operand_or_symbol[0]:
        raise NotImplementedError
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
