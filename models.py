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
            if len(node.transitions):
                pass
            for transition in node.transitions:
                pass
