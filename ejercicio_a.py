# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Queue import Queue
from collections import defaultdict
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


def add_terminal_node(automata):
    terminal=Node()
    for state in automata.states():
        for symbol in automata.symbols():
            state.add_transition(symbol, terminal)

    for symbol in automata.symbols():
        terminal.add_transition(symbol, terminal)

    return Automata(automata.initial, automata.finals)


def minimize(automata):
    automata=add_terminal_node(automata)
    current_partition={}
    for state in automata.states():
        if state not in automata.finals:
            current_partition[state.name]=1
        if state in automata.finals:
            current_partition[state.name]=2

    previous_partition=None
    while current_partition != previous_partition:
        previous_partition=current_partition
        current_partition={}
        labels=defaultdict(dict)

        # previous partitons es equiv_(n-1)
        # labels refiere a el identificador de la particion
        for symbol in automata.symbols():
            for state in automata.states():
                labels[state.name][symbol]=previous_partition[state.transition(symbol).name]

        new_labels=defaultdict(dict)
        for state in automata.states():
            # -1 es para identificar a la columna de la equiv_k
            new_labels[state.name][-1]=previous_partition[state.name]
            for symbol in automata.symbols():
                new_labels[state.name][symbol]=labels[state.name][symbol]

        # esto para armar los nuevos identificadores
        # para las nuevas particiones.
        new_labels_unique=[]
        # calculo los nuevos nombres de particion
        for label in new_labels.values():
            if label not in new_labels_unique:
                new_labels_unique.append(label)

        for state in automata.states():
            current_partition[state.name]=new_labels_unique.index(new_labels[state.name])

    # armo el grafo
    min_states_by_name={}
    for new_label in new_labels_unique:
        min_states_by_name[new_labels_unique.index(new_label)]=Node(name='q{0}'.format(new_labels_unique.index(new_label)))

    initial = None
    finals=set()

    for state in automata.states():
        for symbol in automata.symbols():
            new_label=current_partition[state.name]
            try:
                to_state=min_states_by_name[labels[state.name][symbol]]
            except KeyError:
                # no hay eje en el nuevo grafo
                continue
            current_new_state=min_states_by_name[new_label]
            current_new_state.add_transition(symbol, to_state)
            if state in automata.finals:
                finals.add(current_new_state)
            if state == automata.initial:
                initial = current_new_state

    assert initial is not None

    return Automata(initial, finals)


def nfa_to_dfa(automata):
    initial = Node(nfa_states=lambda_closure(set([automata.initial]), automata))
    states_queue = Queue()
    states_queue.put(initial)
    used_states = set([initial])
    # aca construimos el nuevo delta
    while not states_queue.empty():
        dfa_state = states_queue.get()
        for symbol in automata.symbols():
            state_closure=lambda_closure(automata.move_set(dfa_state.nfa_states, symbol), automata)

            new_dfa_state=Node(nfa_states=state_closure)
            new = True
            for used_state in used_states:
                if state_closure == used_state.nfa_states:
                    new_dfa_state = used_state
                    new = False
                    break

            if new:
                states_queue.put(new_dfa_state)
            dfa_state.add_transition(symbol, new_dfa_state)
            used_states.add(new_dfa_state)

    res = Automata(initial, [])
    for state in res.states():
        for nfa_state in state.nfa_states:
            if nfa_state in automata.finals:
                res.finals.add(state)

    return res


def afd_minimo(archivo_regex, archivo_automata):
    automata=regex_to_automata(archivo_regex)
    if not automata.is_deterministic():
        automata=nfa_to_dfa(automata)
    automata=minimize(automata)
    save_automata(automata, archivo_automata)
