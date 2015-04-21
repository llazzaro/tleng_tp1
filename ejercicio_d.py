# -*- coding: utf-8 -*- 
#!/usr/bin/python


from parsers import load_automata
from writers import save_automata
from models import Automata, Node
from ejercicio_a import minimize

class IncompatibleAlphabetsError(Exception):
	pass

class NonDeterministicAutomataError(Exception):
	pass

def getElementFromSet(A):
	return A.copy().pop()

def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
	automata1 = load_automata(archivo_automata1)
	automata2 = load_automata(archivo_automata2)

	save_automata(afd_interseccion(automata1, automata2), archivo_automata)


def afd_interseccion(automata1, automata2):
	if automata1.symbols() != automata2.symbols():
		raise IncompatibleAlphabetsError

	for s in automata1.states():
		for c in automata1.symbols():
			if len(s.transitions[c]) > 1:
				raise NonDeterministicAutomataError

	for s in automata2.states():
		for c in automata2.symbols():
			if len(s.transitions[c]) > 1:
				raise NonDeterministicAutomataError

	symbols = automata1.symbols()

	state_product = dict([((s1, s2), Node(name="(" + s1.name + "," + s2.name + ")" )) for s2 in automata2.states() for s1 in automata1.states()])
	
	targeted_nodes = []
	for (s1, s2) in state_product.keys():
		for a in symbols:
			# Hay uno solo porque son determinísticos.
			if len(s1.transitions[a]) == 1 and len(s2.transitions[a]) == 1:
				# FIXME set.copy().pop(), única forma de obtener el target sin desarmar el Nodo :/
				for target1 in s1.transitions[a]:
					for target2 in s2.transitions[a]:
						state_product[(s1, s2)].add_transition(a, state_product[(target1, target2)])
						targeted_nodes.append(state_product[(target1, target2)])

	intersection_finals = set([state_product[(s1, s2)] for (s1, s2) in state_product.keys() if s1 in automata1.finals and s2 in automata2.finals])
	intersection_states = [s for s in state_product.values() if len(s.transitions) > 0 or s in targeted_nodes]

	intersection_automata = Automata(state_product[(automata1.initial, automata2.initial)], intersection_finals, symbols, intersection_states)

	return intersection_automata
	#return minimize(intersection_automata)
