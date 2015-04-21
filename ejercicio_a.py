# -*- coding: utf-8 -*-
#!/usr/bin/python

from Queue import Queue
from models import Automata, FromNFANode, LAMBDA
from parsers import regex_to_automata
from writers import save_automata


def lambda_closure(from_states, automata):
    res = set()
    queue = Queue()
    for state in from_states:
        queue.put(state)

    while not queue.empty():
        node = queue.get()
        for edge, nodes in node.transitions.iteritems():
            if edge == LAMBDA:
                for node in nodes:
                    queue.put(node)
                    res.add(node)
    return res


def minimize(automata):
    pass


def nfa_to_dfa(automata):
    sigma = automata.egdes()
    res = Automata()

    res.initial = FromNFANode(lambda_closure(set([automata.initial])))
    unmarked_states = set([res.initial])

    while not unmarked_states.empty():
        node = unmarked_states.pop()
        for symbol in sigma:
            state_closure = lambda_closure(set([node]))
            dfa_candidate_node = FromNFANode(state_closure)
            if dfa_candidate_node not in res.states():
                unmarked_states.put(dfa_candidate_node)
            node.transitions.append(dfa_candidate_node)

    for state in res.states():
        for nfa_state in state.nfa_states:
            if nfa_state in automata.finals:
                res.finals.append(state)

    return res


def afd_minimo(archivo_regex, archivo_automata):
    automata = regex_to_automata(archivo_regex)
    if not automata.is_deterministic():
        automata = nfa_to_dfa(automata)
    automata = minimize(automata)
    save_automata(automata, archivo_automata)
