# -*- coding: utf-8 -*-
#!/usr/bin/python

from Queue import Queue
from parsers import load_automata
from ejercicio_a import minimize


def dfa_rename(automata):
    queue = Queue()
    initial = automata.initial
    queue.put(initial)
    marked = set()
    index = 0
    while not queue.empty():
        state = queue.get()
        if state not in marked:
            state.name = index
            index = index + 1
            marked.add(state)
            for symbol, to_states in state.transitions.iteritems():
                for to_state in to_states:
                    queue.put(to_state)


def identicos(automata_1, automata_2):
    for state_1 in automata_1.states():
        state_2 = filter(lambda state_2: state_2.name == state_1.name, automata_2.states())
        if state_2:
            for symbol in automata_1.symbols():
                # revisamos las transitions
                if state_1.transition(symbol).name != state_2[0].transition(symbol).name:
                    return False
        else:
            return False

    return True


def equivalentes(archivo_automata1, archivo_automata2):
    automata_1 = load_automata(archivo_automata1)
    automata_2 = load_automata(archivo_automata2)

    if automata_1.symbols() != automata_2.symbols():
        print 'FALSE'
        return False

    minimized_1 = minimize(automata_1)
    minimized_2 = minimize(automata_2)

    # ahora renombro los labels para ver si puedo ver que son iguales
    dfa_rename(minimized_1)
    dfa_rename(minimized_2)

    res = identicos(minimized_1, minimized_2)

    if res:
        print 'TRUE'
    else:
        print 'FALSE'

    return res
