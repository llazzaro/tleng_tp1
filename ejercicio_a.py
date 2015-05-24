# -*- coding: utf-8 -*-
#!/usr/bin/env python

import itertools
from Queue import Queue
from models import Automata, LAMBDA, Node
from parsers import regex_to_automata
from writers import save_automata


def lambda_closure(from_states, automata):
    res=set()
    queue=Queue()
    for state in from_states:
        queue.put(state)
        res.add(state)

    while not queue.empty():
        node=queue.get()
        for edge, nodes in node.transitions.iteritems():
            if edge == LAMBDA:
                for node in nodes:
                    queue.put(node)
                    res.add(node)
    return res

def copy_with_terminal_node(automata):
    return add_terminal_node(automata)

def add_terminal_node(automata):
    terminal=Node("qT")
    states = list(automata.states)
    finals = []
    initial = None

    #recorro los nodos, me fijo cuales son inicial/finales
    # y los modifico para que pasen al trampa cuando corresponda
    for state in states:
        if state in automata.finals:
            finals.append(state)
        if state == automata.initial:
            initial = state
        for symbol in automata.symbols:
            if not state.transitions.has_key(symbol):
                state.add_transition(symbol, terminal)

    for symbol in automata.symbols:
        terminal.add_transition(symbol, terminal)

    states.append(terminal)

    return Automata(states, automata.symbols, initial, finals)

#def add_terminal_node(automata):
#    """
#        CUIDADO: modifica la estructura del automata parametro
#    """
#    terminal=Node()
#    for state in automata.states:
#        for symbol in automata.symbols:
#            state.add_transition(symbol, terminal)
#
#    for symbol in automata.symbols:
#        terminal.add_transition(symbol, terminal)
#
#    return Automata(automata.initial, automata.finals)


def remover_nodos_redundantes(automata):
    to_remove = set()
    for state in automata.states:
        recheable_states = list(itertools.chain(*state.transitions.values()))
        if all(map(lambda to_state: state == to_state, recheable_states)) and state not in automata.finals:
            to_remove.add(state)

    if to_remove:
        for state in automata.states:
            for symbol in automata.symbols:
                to_states = state.transitions[symbol]
                state.transitions[symbol] = to_states - to_remove

    return Automata(automata.initial, automata.finals)


def nfa_to_dfa(automata):
    initial = Node(nfastates=lambda_closure(set([automata.initial]), automata))
    states_queue = Queue()
    states_queue.put(initial)
    used_states = set([initial])
    symbols = []
    states = []
    # aca construimos el nuevo delta
    while not states_queue.empty():
        dfa_state = states_queue.get()
        for symbol in automata.symbols:
            symbols.append(symbol)
            state_closure=lambda_closure(automata.move_set(dfa_state.nfastates, symbol), automata)

            new_dfa_state=Node(nfastates=state_closure)
            states.append(new_dfa_state)
            new = True
            for used_state in used_states:
                if state_closure == used_state.nfastates:
                    new_dfa_state = used_state
                    new = False
                    break

            if new:
                states_queue.put(new_dfa_state)
            dfa_state.add_transition(symbol, new_dfa_state)
            used_states.add(new_dfa_state)

    res = Automata(list(set(states)), list(set(symbols)), initial, [])
    for state in res.states:
        for nfa_state in state.nfastates:
            if nfa_state in automata.finals:
                res.finals.append(state)

    return res


def afd_minimo(archivo_regex, archivo_automata):
    automata=regex_to_automata(archivo_regex)
    if not automata.is_deterministic():
        automata=nfa_to_dfa(automata)
    automata=minimize(automata)
    save_automata(automata, archivo_automata)
