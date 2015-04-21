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
    P = set(automata.finals, automata.states() - automata.finals)
    W = set(automata.finals)
    while not W.empty():
        X = set()
        for symbol in automata.symbols():
            for from_state, transition_symbol, to_state in automata.transitions:
                if symbol == transition_symbol:
                    X.add(from_state)

            for Y in P:
                if not (X.intersection(Y)).empty() and not (Y.difference(X)).empty():
                    P.add(X.intersection(Y))
                    P.add(Y.difference(X))

                    if Y in W:
                        W.add(X.intersection(Y))
                        W.add(Y.difference(X))
                        W.remove(Y)
                    else:
                        if len(X.intersection(Y)) <= len(Y.difference(X)):
                            W.append(X.intersection(Y))
                        else:
                            W.append(Y.difference(X))
                P.remove(Y)
    return P, W


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
