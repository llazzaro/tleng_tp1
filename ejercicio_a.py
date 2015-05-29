# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Queue import Queue
from models import Automata, LAMBDA, Node, minimize
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


def nfa_to_dfa(automata):
    node_index = 0
    nfa_states = {}
    initial = Node("q{0}".format(node_index))
    nfa_states[initial] = lambda_closure(set([automata.initial]), automata)
    states_queue = Queue()
    states_queue.put(initial)
    states = [initial]
    # aca construimos el nuevo delta
    while not states_queue.empty():
        dfa_state = states_queue.get()
        for symbol in automata.symbols:
            state_closure=lambda_closure(automata.move_set(nfa_states[dfa_state], symbol), automata)
            new = True
            # me fijo si la clausura ya la encontre antes
            for used_state in nfa_states.keys():
                if state_closure == nfa_states[used_state]:
                    new_dfa_state = used_state
                    new = False
                    break

            if new:
                # la clausura es nueva, creo un nuevo estado.
                node_index += 1
                new_dfa_state=Node("q{0}".format(node_index))
                nfa_states[new_dfa_state] = state_closure
                states.append(new_dfa_state)
                states_queue.put(new_dfa_state)
            dfa_state.add_transition(symbol, new_dfa_state)

    res = Automata(list(set(states)), automata.symbols, initial, [])
    for state in res.states:
        for nfa_state in nfa_states[state]:
            if nfa_state in automata.finals and state not in res.finals:
                res.finals.append(state)

    return res


def afd_minimo(archivo_regex, archivo_automata):
    automata=regex_to_automata(archivo_regex)
    if not automata.is_deterministic():
        automata=nfa_to_dfa(automata)
    automata=minimize(automata)
    save_automata(automata, archivo_automata)
