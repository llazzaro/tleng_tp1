from collections import defaultdict
from Queue import Queue

LAMBDA = '@'


class Node:

    def __init__(self):
        self.transitions = defaultdict(list)


class Automata:

    def __init__(self, initial, finals):
        self.initial = initial
        self.finals = finals

    def is_deterministic(self):
        queue = Queue()
        queue.put(self.initial)
        while not queue.empty():
            node = queue.get()
            for key, nodes in node.transitions.iteritems():
                if len(nodes) > 1:
                    return False
                queue.put(nodes[0])
        return True
