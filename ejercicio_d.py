#!/usr/bin/python
# -*- coding: utf-8 -*- 

from itertools import product

from parsers import load_automata
from writers import save_automata
from models import *

class IncompatibleAlphabetsError(Exception):
    pass

class NonDeterministicAutomataError(Exception):
    pass

def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
    automata1 = load_automata(archivo_automata1)
    automata2 = load_automata(archivo_automata2)

    save_automata(afd_interseccion(automata1, automata2), archivo_automata)


def afd_interseccion(automata1, automata2):
    if not (automata1.is_deterministic() and automata2.is_deterministic()):
        raise NonDeterministicAutomataError

    symbols = list(set(automata1.symbols + automata2.symbols))

    #Creo un estado para cada par de estados en los dos autómatas originales
    state_product_list = list(product(automata1.states, automata2.states))
    state_product = dict(zip(state_product_list, map(lambda (i, j): Node(name="(" + str(i) + "," + str(j) + ")"), state_product_list)))

    #Creo transiciones entre los nodos creados
    for (s1, s2) in state_product.keys():
        for a in symbols:
            # Hay uno solo porque son determinísticos.
            if s1.transitions.has_key(a) and s2.transitions.has_key(a):
                for target1 in s1.transitions[a]:
                    for target2 in s2.transitions[a]:
                        state_product[(s1, s2)].add_transition(a, state_product[(target1, target2)])

    intersection_finals = [state_product[(s1, s2)] for (s1, s2) in state_product.keys() if s1 in automata1.finals and s2 in automata2.finals]

    intersection_automata = Automata(state_product.values(), symbols, state_product[(automata1.initial, automata2.initial)], intersection_finals)
    intersection_automata.prune_unreachable_states()

    #return intersection_automata
    intersection_with_terminal = add_terminal_node(intersection_automata)
    return minimize(intersection_with_terminal)
