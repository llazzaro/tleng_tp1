# -*- coding: utf-8 -*-

import string
from models import Automata, Node, LAMBDA
from collections import defaultdict


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
            raise Exception('Formato invalido. Estado final {0} esta en la lista de estados validos {1}'.format(final_state_name, states))
        else:
            for state in states:
                if state.name == final_state_name.strip('\n'):
                    finals.append(state)

    for transition_line in automata_file:
        transition = transition_line.split('\t')
        tr_src_name = transition[0]
        tr_sym = transition[1]
        tr_tgt_name = transition[2].strip('\n')

        tr_src_state = None
        tr_tgt_state = None

        for state in states:
            # aprint state.name
            if tr_src_state is None and state.name == tr_src_name:
                tr_src_state = state
            if tr_tgt_state is None and state.name == tr_tgt_name:
                tr_tgt_state = state

        if tr_src_state is None:
            raise Exception('Formato invalido. La transición {0} --{1}--> {2} parte de un estado que no está en la lista: {3}'.format(tr_src_name, tr_sym, tr_tgt_name, states))
        if tr_tgt_state is None:
            raise Exception('Formato invalido. La transición {0} --{1}--> {2} va a un estado que no está en la lista: {3}'.format(tr_src_name, tr_sym, tr_tgt_name, states))

        tr_src_state.add_transition(tr_sym, tr_tgt_state)

    return Automata(states, symbols, initial, finals)

class Tree():
	def __init__(self, content):
		self.content = content

	def to_automata(self):
		pass

class Symbol(Tree):
	def __init__(self, content):
		assert(isinstance(content, str))
		Tree.__init__(self, content)

	def to_automata(self):
		q0 = Node()
		q1 = Node()
		q0.add_transition(self.content, q1)
		return Automata([q0, q1], [self.content], q0, [q1])

class Star(Tree):
	def __init__(self, content):
		assert(isinstance(content, Tree))
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
		assert(isinstance(content, Tree))
		Tree.__init__(self, content)

	def to_automata(self):
		return Concat([self.content, Star(self.content)]).to_automata()

class Opt(Tree):
	def __init__(self, content):
		assert(isinstance(content, Tree))
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
		assert(isinstance(content, list))
		assert(len(content) >= 2)
		for t in content:
			assert(isinstance(t, Tree))
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
		assert(isinstance(content, list))
		assert(len(content) >= 2)
		for t in content:
			assert(isinstance(t, Tree))
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
					final.add_transition(LAMBDA, content_automatas[i+1].initial)

		return Automata(states, list(set(symbols)), content_automatas[0].initial, content_automatas[-1].finals)

def build_operand_tree(tree_file):
	line = tree_file.readline()
	if '{CONCAT}' in line:
		tabs, number_of_operands = line.split('{CONCAT}')
		content = []
		for i in range(int(number_of_operands)):
			content.append(build_operand_tree(tree_file))
		return Concat(content)
	elif '{OR}' in line:
		tabs, number_of_operands = line.split('{OR}')
		content = []
		for i in range(int(number_of_operands)):
			content.append(build_operand_tree(tree_file))
		return Or(content)
	elif '{OPT}' in line:
		return Opt(build_operand_tree(tree_file))
	elif '{PLUS}' in line:
		return Plus(build_operand_tree(tree_file))
	elif '{STAR}' in line:
		depth = line.count('\t')
		return Star(build_operand_tree(tree_file))
	else:
		return Symbol(line.strip())

def verify_integrity(res):
    """
        Revisa si para los op que tienen numero de operandos,
        este numero es valido (si hay dos param hay dos ni mas ni menos)

        si encuentra algo que esta mal lanza exception
    """

    for deep, list_of_op in res.iteritems():
        for op, number_of_operands in list_of_op:
            if op in ['{CONCAT}', '{OR}']:
                if len(res[deep + 1]) < number_of_operands:
                    raise Exception('{2} requiere {1} paramteros, se encontro solamente {0} parametros'.format(len(res[deep + 1]), number_of_operands, op))


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
            current_line = line.strip('\t').strip('\n')
            if len(current_line) == 0:
                current_line = '\t'
                deep = deep - 1

            res[deep].append(('{SYMBOL}', current_line))
    verify_integrity(res)
    return res


def regex_to_automata(tree_file):
    operand_dict = build_operand_dict(tree_file)
    res = build_automata(operand_dict[0][0], 0, operand_dict)

    return res


def build_automata(current_operand_or_symbol, deep, operand_or_symbol_dict):
    if '{CONCAT}' == current_operand_or_symbol[0]:
        number_of_operands = current_operand_or_symbol[1]
        initial = None
        finals = None
        states = []
        symbols = []
        operand_or_symbols = operand_or_symbol_dict[deep + 1]
        operand_or_symbols = operand_or_symbols[:number_of_operands]
        operand_automatas = []
        for operand in operand_or_symbols:
            operand_automatas.append(build_automata(operand, deep + 1, operand_or_symbol_dict))

        initial = operand_automatas[0].initial
        for index, operand_automata in enumerate(operand_automatas):
            states += operand_automata.states
            symbols += operand_automata.symbols
            if index > len(operand_automatas) - 2:
                # es el ultimo operando
                continue
            for final in operand_automata.finals:
                final.add_transition(LAMBDA, operand_automatas[index + 1].initial)

        operand_or_symbol_dict[deep + 1] = operand_or_symbol_dict[deep + 1][number_of_operands:]
        finals = operand_automatas[-1:][0].finals

        return Automata(states, symbols, initial, finals)
    elif '{STAR}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        states = [initial, final]
        symbols = []
        for operand in operand_or_symbol_dict[deep + 1][:1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            states += operand_automata.states
            symbols += operand_automata.symbols
        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
            dfa_final.add_transition(LAMBDA, operand_automata.initial)

        initial.add_transition(LAMBDA, operand_automata.initial)
        initial.add_transition(LAMBDA, final)
        operand_or_symbol_dict[deep + 1] = operand_or_symbol_dict[deep + 1][1:]
        return Automata(states, symbols, initial, [final])
    elif '{PLUS}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        symbols = []
        states = [initial, final]
        for operand in operand_or_symbol_dict[deep + 1][:1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            states += operand_automata.states
            symbols += operand_automata.symbols
        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
            dfa_final.add_transition(LAMBDA, operand_automata.initial)

        initial.add_transition(LAMBDA, operand_automata.initial)

        operand_or_symbol_dict[deep + 1] = operand_or_symbol_dict[deep + 1][1:]
        return Automata(states, symbols, initial, [final])
    elif '{OPT}' in current_operand_or_symbol[0]:
        initial = Node()
        final = Node()
        states = [initial, final]
        symbols = []
        initial.add_transition(LAMBDA, final)

        for operand in operand_or_symbol_dict[deep + 1][:1]:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            states += operand_automata.states
            symbols += operand_automata.symbols

        for dfa_final in operand_automata.finals:
            dfa_final.add_transition(LAMBDA, final)
        initial.add_transition(LAMBDA, operand_automata.initial)

        operand_or_symbol_dict[deep + 1] = operand_or_symbol_dict[deep + 1][1:]
        return Automata(states, symbols, initial, [final])
    elif '{OR}' in current_operand_or_symbol[0]:
        number_of_operands = current_operand_or_symbol[1]
        initial = Node()
        new_final = Node()
        states = [initial, new_final]
        symbols = []
        operand_or_symbols = operand_or_symbol_dict[deep + 1][:number_of_operands]

        for operand in operand_or_symbols:
            operand_automata=build_automata(operand, deep + 1, operand_or_symbol_dict)
            states += operand_automata.states
            symbols += operand_automata.symbols
            initial.add_transition(LAMBDA, operand_automata.initial)
            for final in operand_automata.finals:
                final.add_transition(LAMBDA, new_final)

        operand_or_symbol_dict[deep + 1] = operand_or_symbol_dict[deep + 1][number_of_operands:]
        return Automata(states, symbols, initial, [new_final])
    else:
        # simbolo alfabeto
        assert current_operand_or_symbol[0] == '{SYMBOL}'
        symbol=current_operand_or_symbol[1]
        if symbol not in string.letters + '([,:;.¿?!¡()"\'\&-] \t' + '0123456789':
            raise Exception('El simbolo {0} no esta permitido'.format(symbol))
        initial=Node()
        final=Node()
        states = [initial, final]
        symbols = [symbol]
        initial.add_transition(symbol, final)
        return Automata(states, symbols, initial, [final])
