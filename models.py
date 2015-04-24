from collections import defaultdict
from Queue import Queue

LAMBDA = '@'


class Node(object):

    NODE_INDEX = 0

    def __init__(self, name=None):
        self.name = name
        if not name:
            self.name = 'q{0}'.format(Node.NODE_INDEX)
        Node.NODE_INDEX += 1
        self.transitions = defaultdict(set)

    def add_transition(self, symbol, state):
        self.transitions[symbol].add(state)

    def transition(self, symbol):
        for state in self.transitions[symbol]:
            return state

    def __eq__(self, other):
        return self.name == other.name

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
        self._symbols = symbols
        self._states = states
        if not symbols or not states:
            self._states = set()
            self._symbols = set()
            visited = set()
            queue = Queue()
            queue.put(initial)
            self._states.add(self.initial)
            while not queue.empty():
                state = queue.get()
                if state in visited:
                    continue
                visited.add(state)
                for symbol, nodes in state.transitions.iteritems():
                    self._symbols.add(symbol)
                    for node in nodes:
                        self._states.add(node)
                        queue.put(node)

    def move_set(self, state, symbol):
        res = set()
        for edge, nodes in state.transitions:
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

    def move(self, symbol):
        raise NotImplementedError

    def reset(self):
        self.current_state = self.initial

    def states(self):
        return self._states

    def symbols(self):
        return self._symbols

    def delta(self):
        raise NotImplementedError

    def add_symbol(self, symbol):
        self._symbols.add(symbol)

    def add_state(self, state):
        self.state.add(state)

    def state_by_name(self, state_name):
        for state in self._states:
            if state.name == state_name:
                return state
        raise ValueError('State not found')

    def is_deterministic(self):
        for state in self._states:
            for key, to_states in state.transitions.iteritems():
                if len(to_states) > 1:
                    return False
        return True

    def set_final_state(self, state_name):
        for state in self.state:
            if state.name == state_name:
                self.finals.add(state)
                return


class FromNFANode(Node):

    def __init__(self, nodes, name=None):
        super(FromNFANode, self).__init__(name)
        self.nodes = nodes

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.nodes == other.nodes and self.name == other.name
