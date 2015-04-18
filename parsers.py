from models import Automata, Node, LAMBDA
from collections import defaultdict


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
                    final.transitions[LAMBDA].append(next_node)
            else:
                finals = operand_automata.finals
            next_node = operand_automata.initial

        initial.transitions[LAMBDA].append(next_node)
        return Automata(initial, finals)
    elif '{START}' in current_operand_or_symbol[0]:
        pass
    elif '{PLUS}' in current_operand_or_symbol[0]:
        pass
    elif '{OPT}' in current_operand_or_symbol[0]:
        pass
    elif '{OR}' in current_operand_or_symbol[0]:
        initial = Node()
        new_final = Node()

        for operand in operand_or_symbol_dict[deep + 1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            initial.transitions[LAMBDA].append(operand_automata.initial)
            for final in operand_automata.finals:
                final.transitions[LAMBDA].append(new_final)

        return Automata(initial, [new_final])
    else:
        # simbolo alfabeto
        assert current_operand_or_symbol[0] == '{SYMBOL}'
        symbol=current_operand_or_symbol[1]
        initial=Node()
        final=Node()
        initial.transitions[symbol].append(final)
        return Automata(initial, [final])
