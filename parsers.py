# -*- coding: utf-8 -*-

import string
from models import Automata, Node, LAMBDA


def is_valid_char(char):
    return char == '\\t' or char in string.letters + string.digits + '([,:;.¿?!¡()"\&-]' + "'"


def parse_transition_line(transition_line, states):
    transition = transition_line.split('\t')
    tr_src_name = transition[0]
    tr_sym = transition[1]
    tr_tgt_name = transition[2].strip('\n')

    tr_src_state = None
    tr_tgt_state = None

    for state in states:
        if tr_src_state is None and state.name == tr_src_name:
            tr_src_state = state
        if tr_tgt_state is None and state.name == tr_tgt_name:
            tr_tgt_state = state

    if tr_src_state is None:
        raise Exception('Formato invalido. La transición {0} --{1}--> {2} parte de un estado que no está en la lista: {3}'.format(tr_src_name, tr_sym, tr_tgt_name, states))
    if tr_tgt_state is None:
        raise Exception('Formato invalido. La transición {0} --{1}--> {2} va a un estado que no está en la lista: {3}'.format(tr_src_name, tr_sym, tr_tgt_name, states))

    tr_src_state.add_transition(tr_sym, tr_tgt_state)


def load_automata(automata_file):
    states_line = automata_file.readline()
    states = []
    for state_name in states_line.split('\t'):
        state = Node(name=state_name.strip('\n'))
        states.append(state)
        states = list(set(states))

    valid_state_names = map(lambda state: state.name, states)

    symbol_line = automata_file.readline()
    symbols = []
    for symbol in symbol_line.split('\t'):
        symbols.append(symbol.strip('\n'))

    initial_line = automata_file.readline()
    initial = None
    initial_name = initial_line.strip('\n')
    if initial_name not in valid_state_names:
        raise Exception('El estado inicial {0} no es valido. no se encuentra en la lista de estados validos {1}'.format(initial_name, states))

    for state in states:
        if state.name == initial_name:
            initial = state

    finals_line = automata_file.readline()
    finals = []
    for final_state_name in finals_line.split('\t'):
        final_state_name = final_state_name.strip('\n')
        if final_state_name not in valid_state_names:
            if is_valid_char(final_state_name):
                # No hay finales y es la primer transición!!
                parse_transition_line(finals_line, states)
                finals = []
                break
            else:
                raise Exception('Formato invalido. Estado final {0} esta en la lista de estados validos {1}'.format(final_state_name, states))
        else:
            for state in states:
                if state.name == final_state_name.strip('\n'):
                    finals.append(state)

    for transition_line in automata_file:
        parse_transition_line(transition_line, states)

    return Automata(states, symbols, initial, finals)


class Tree():
    def __init__(self, content):
        self.content = content

    def to_automata(self):
        pass


class Symbol(Tree):
    def __init__(self, content):
        if not isinstance(content, str):
            raise TypeError
        if len(content) > 1 and content[0] != '\\':
            raise ValueError
        if not is_valid_char(content):
            raise ValueError

        Tree.__init__(self, content)

    def to_automata(self):
        q0 = Node()
        q1 = Node()
        q0.add_transition(self.content, q1)
        return Automata([q0, q1], [self.content], q0, [q1])


class Star(Tree):
    def __init__(self, content):
        if not isinstance(content, Tree):
            raise TypeError

        Tree.__init__(self, content)

    def to_automata(self):
        content_automata = self.content.to_automata()
        q0 = Node()
        qf = Node()

        q0.add_transition(LAMBDA, content_automata.initial)
        q0.add_transition(LAMBDA, qf)

        for q in content_automata.finals:
            q.add_transition(LAMBDA, qf)
            q.add_transition(LAMBDA, content_automata.initial)

        return Automata([q0, qf] + content_automata.states, content_automata.symbols, q0, [qf])


class Plus(Tree):
    def __init__(self, content):
        if not isinstance(content, Tree):
            raise TypeError

        Tree.__init__(self, content)

    def to_automata(self):
        return Concat([self.content, Star(self.content)]).to_automata()


class Opt(Tree):
    def __init__(self, content):
        if not isinstance(content, Tree):
            raise TypeError

        Tree.__init__(self, content)

    def to_automata(self):
        content_automata = self.content.to_automata()
        q0 = Node()
        qf = Node()
        states = [q0, qf] + content_automata.states

        q0.add_transition(LAMBDA, qf)
        q0.add_transition(LAMBDA, content_automata.initial)
        for q in content_automata.finals:
            q.add_transition(LAMBDA, qf)

        return Automata(states, content_automata.symbols, q0, [qf])


class Or(Tree):
    def __init__(self, content):
        if not isinstance(content, list):
            raise TypeError

        if not len(content) >= 2:
            raise Exception("Or without enough operands")

        for t in content:
            if not isinstance(t, Tree):
                raise TypeError

        Tree.__init__(self, content)

    def to_automata(self):
        content_automatas = [tree.to_automata() for tree in self.content]
        q0 = Node()
        qf = Node()
        states = [q0, qf]
        symbols = []

        for automata in content_automatas:
            states += automata.states
            symbols += automata.symbols

            q0.add_transition(LAMBDA, automata.initial)
            for finals in automata.finals:
                finals.add_transition(LAMBDA, qf)

        return Automata(states, list(set(symbols)), q0, [qf])


class Concat(Tree):
    def __init__(self, content):
        if not isinstance(content, list):
            raise TypeError

        if not len(content) >= 2:
            raise Exception("Concat without enough operands")

        for t in content:
            if not isinstance(t, Tree):
                raise TypeError

        Tree.__init__(self, content)

    def to_automata(self):
        content_automatas = [tree.to_automata() for tree in self.content]
        states = []
        symbols = []

        for i in range(len(content_automatas)):
            states += content_automatas[i].states
            symbols += content_automatas[i].symbols
            if i < len(content_automatas) - 1:
                for final in content_automatas[i].finals:
                    final.add_transition(LAMBDA, content_automatas[i + 1].initial)

        return Automata(states, list(set(symbols)), content_automatas[0].initial, content_automatas[-1].finals)


def build_operand_tree(tree_file):
    tree = build_operand_tree_with_depth(tree_file, 0)
    if tree_file.readline() != '':
        raise Exception("Cargué un árbol sin leer todo el archivo.")
    return tree


def build_operand_tree_with_depth(tree_file, depth):
    line = tree_file.readline()
    if len('line') == '':
        raise Exception("Fin de archivo inesperado")
    if line.count("\t") != depth:
        raise Exception("Árbol mal definido, esperaba {0} tabs y encontré {1}".format(depth, line.count("\t")))

    if '{CONCAT}' in line:
        tabs, number_of_operands = line.split('{CONCAT}')
        number_of_operands = int(number_of_operands.strip())
        content = []
        for i in range(int(number_of_operands)):
            content.append(build_operand_tree_with_depth(tree_file, depth + 1))
        return Concat(content)
    elif '{OR}' in line:
        tabs, number_of_operands = line.split('{OR}')
        number_of_operands = int(number_of_operands.strip())
        content = []
        for i in range(int(number_of_operands)):
            content.append(build_operand_tree_with_depth(tree_file, depth + 1))
        return Or(content)
    elif '{OPT}' in line:
        return Opt(build_operand_tree_with_depth(tree_file, depth + 1))
    elif '{PLUS}' in line:
        return Plus(build_operand_tree_with_depth(tree_file, depth + 1))
    elif '{STAR}' in line:
        depth = line.count('\t')
        return Star(build_operand_tree_with_depth(tree_file, depth + 1))
    else:
        return Symbol(line.strip())


def regex_to_automata(tree_file):
    operand_tree = build_operand_tree(tree_file)
    return operand_tree.to_automata()
