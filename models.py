# -*- coding: utf-8 -*-
#!/usr/bin/python

from collections import defaultdict
from Queue import Queue

LAMBDA = '@'


class Node(object):

    NODE_INDEX = 0

    #FIXME Revisar esos nfastates
    def __init__(self, name=None, nfastates=None):
        self.name = name
        if not name:
            self.name = 'q{0}'.format(Node.NODE_INDEX)
        self.nfastates = nfastates
        Node.NODE_INDEX += 1
        self.transitions = {}

    def add_transition(self, symbol, state):
        if self.transitions.has_key(symbol):
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

    def is_deterministic(self):
        return self.is_lambda_deterministic() and LAMBDA not in self.transitions.keys()

    def is_lambda_deterministic(self):
       res = True
       for s in self.transitions:
           res = res and len(self.transitions[s]) == 1
        
       return res

    def reachable_nodes(self):
        res = set()
        for a in self.transitions.keys():
            for s in self.transitions[a]:
                res.add(s)

        return res

    #FIXME: Posiblemente inútil.
    def transition(self, symbol):
        for state in self.transitions[symbol]:
            return state

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name or (self.nfastates is not None and self.nfastates == other.nfastates)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class FinalsNotInStatesException(Exception):
    pass

class UnexpectedSymbolOnStateException(Exception):
    pass

class Automata:
    def __init__(self, states, symbols, initial, finals):
        self.initial = initial
        self.current_state = initial
    
        if not (type(states) == type(symbols) == type(finals) == list):
            raise TypeError

        for s in states:
            if set(s.transitions.keys()) - set(symbols) != set():
                raise UnexpectedSymbolOnStateException("El estado {0} tiene símbolos que no corresponden al alfabeto {1}: {2}".format(s, symbols, set(s.transitions.keys()) - set(symbols)))

        if set(finals) - set(states) != set():
            raise FinalsNotInStatesException("Estado(s) final(es) que no pertenece(n) a los estados del autómata: {0}".format(set(finals) - set(states)))

        self.finals = finals

        self.symbols = symbols
        self.states = states

    def move_set(self, states, symbol):
        """
            dado un conjunto de states y un symbol
            devuelve los states que son alcanzables por symbol
        """
        res = set()
        for state in states:
            for edge, nodes in state.transitions.iteritems():
                if symbol == edge:
                    for node in nodes:
                        res.add(node)
        return res

    #def add_symbol(self, symbol):
    #    self.symbols.add(symbol)

    #def add_state(self, state):
    #    self.state.add(state)

    def state_by_name(self, state_name):
        for state in self.states:
            if state.name == state_name:
                return state
        raise ValueError('State not found')

    #def set_final_state(self, state_name):
    #    for state in self.state:
    #        if state.name == state_name:
    #            self.finals.add(state)
    #            return

    def has_lambda(self):
        return LAMBDA in self.symbols

    def is_lambda_deterministic(self):
        res = True
        for state in self.states:
            res = res and state.is_lambda_deterministic()
        return res

    def is_deterministic(self):
        res = True
        for state in self.states:
            res = res and state.is_deterministic()
        return res

    # Métodos para recorrer el autómata con una cadena
    def accepts(self, string):
        if not self.is_deterministic():
            raise TypeError("Sólo sabemos recorrer autómatas determinísticos")

        try:
            current_state = self.initial
            for symbol in string:
                current_state = current_state.transitions[symbol][0]

            return current_state in self.finals
        except KeyError:
            return False
        except IndexError:
            return False

    # Métodos utilizados para implementar la intersección
    def prune_unreachable_states(self):
        """
            Actualiza la lista de estados para que queden sólo los alcanzables desde el inicial
            (En la construcción de la intersección aparecen muchos estados inalcanzables)
        """
        reachable_states = self.all_states_reachable_from(self.initial)
        reachable_states.add(self.initial)
        reachable_finals = set(self.finals) & reachable_states

        self.states = list(reachable_states)
        self.finals = list(reachable_finals)

    def all_states_reachable_from(self, state):
        res = state.reachable_nodes()
        res_prev = set()

        while len(res) > len(res_prev):
            res_menor = res_prev
            res_prev = res
            for s in res_prev:
                if s not in res_menor:  # Módica optimización
                    res = res.union(s.reachable_nodes())

        return res


