# -*- coding: utf-8 -*- 
#!/usr/bin/python


from parsers import load_automata
from models import Automata, Node
from ejercicio_a import minimize

class IncompatibleAlphabetsError(Exception):
	pass


def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
	automata1 = load_automata(archivo_automata1)
	automata2 = load_automata(archivo_automata2)

	if automata1.symbols != automata2.symbols:
		raise IncompatibleAlphabetsError

	symbols = automata1.symbols

	state_product = dict([((s1, s2), Node(name="(" + s1.name + ", " + s2.name + ")" )) for s2 in automata2.states for s1 in automata1.states])
	
	nodos_receptores = []
	for (s1, s2) in state_product.keys():
		for a in symbols:
			if a in s1.transitions and a in s2.transitions:
				state_product[(s1, s2)].add_transition(a, state_product[(s1.transitions[a], s2.transitions[a])])

	# Limpiar nodos que no tienen transiciones asociadas?

	intersection_finals = [state_product[(s1, s2)] for (s1, s2) in state_product.keys() if s1 in automata1.finals and s2 in automata2.finals]

	automata_interseccion = Automata(state_product[(automata1.initial, automata2.initial)], intersection_finals, symbols, state_product.values())

	return minimize(automata_interseccion)
