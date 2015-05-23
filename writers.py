from collections import defaultdict


def save_dot(automata, dot_file):
    dot_file.write('strict digraph {\n')
    dot_file.write('rankdir=LR;\n')
    dot_file.write('node [shape = none, label = "", width = 0, height = 0]; qd;\n')
    dot_file.write('node [label="\N", width = 0.5, height = 0.5];\n')
    for state in automata.states:
        if state in automata.finals:
            dot_file.write('node [shape = doublecircle]; "{0}";\n'.format(state.name))
    dot_file.write('node [shape = circle];\n')
    dot_file.write('qd -> "{0}"\n'.format(automata.initial.name))
    arc_dict = defaultdict(list)
    for state in automata.states:
        for symbol, nodes in state.transitions.iteritems():
            for node in nodes:
                arc_dict[(state.name, node.name)].append(symbol)

    for nodes_tuple, symbols in arc_dict.iteritems():
        symbols_comma = ', '.join(symbols)
        dot_file.write('"{0}" -> "{1}" [label="{2}"]\n'.format(nodes_tuple[0], nodes_tuple[1], symbols_comma))
    dot_file.write('}')


def save_automata(automata, automata_file):
    states = '\t'.join(map(lambda s: s.name, automata.states))
    automata_file.write(states + '\n')

    symbols = '\t'.join(automata.symbols)
    automata_file.write(symbols + '\n')

    automata_file.write(automata.initial.name + '\n')

    finals = '\t'.join(map(lambda s: s.name, automata.finals))
    automata_file.write(finals + '\n')

    transitions = ''
    for source in automata.states:
        for symbol in source.transitions:
            for target in source.transitions[symbol]:
                transitions += '{0}\t{1}\t{2}\n'.format(source.name, symbol, target.name)

    automata_file.write(transitions)
