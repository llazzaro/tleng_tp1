from collections import defaultdict
from Queue import Queue

LAMBDA = '@'


class Node(object):

    NODE_INDEX = 0

    def __init__(self, name=None, nfa_states=None):
        self.name = name
        if not name:
            self.name = 'q{0}'.format(Node.NODE_INDEX)
        self.nfa_states = nfa_states
        Node.NODE_INDEX += 1
        self.transitions = defaultdict(set)

    def add_transition(self, symbol, state):
        self.transitions[symbol].add(state)

    def transition(self, symbol):
        for state in self.transitions[symbol]:
            return state

    def __eq__(self, other):
        return self.name == other.name or (self.nfa_states and self.nfa_states == other.nfa_states)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Automata:

    def __init__(self, initial, finals, symbols=None, states=None):
        self.initial = initial
        self.current_state = initial
        self.finals = finals
        if type(self.finals) == list:
            self.finals = set(self.finals)
        self.symbols = symbols
        self.states = states
        if not symbols or not states:
            self.states = set()
            self.symbols = set()
            visited = set()
            queue = Queue()
            queue.put(initial)
            self.states.add(self.initial)
            while not queue.empty():
                state = queue.get()
                if state in visited:
                    continue
                visited.add(state)
                for symbol, nodes in state.transitions.iteritems():
                    self.symbols.add(symbol)
                    for node in nodes:
                        self.states.add(node)
                        queue.put(node)

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

    def move_sequence(self, input_sequence):
        try:
            for sequence_symbol in input_sequence:
                self.current_state = list(self.current_state.transitions[sequence_symbol])[0]

            return self.current_state in self.finals
        except KeyError:
            return False
        except IndexError:
            return False

    def states(self):
        return self.states

    def symbols(self):
        return self.symbols

    def state_by_name(self, state_name):
        for state in self.states:
            if state.name == state_name:
                return state
        raise ValueError('State not found')

    def is_deterministic(self):
        for state in self.states:
            for key, to_states in state.transitions.iteritems():
                if len(to_states) > 1:
                    return False
        return True

