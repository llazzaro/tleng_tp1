
def save_dot(automata, dot_file):
    dot_file.write('digraph automata {')
    dot_file.write('rankdir=LR;')
    for state in automata.states():
        if state == automata.initial:
            dot_file.write('node [shape = none, label = "", width = 0, height = 0]; {0}'.format(state.name))
        elif state in automata.finals:
            dot_file.write('"{0}" [shape = doublecircle]'.format(state.name))
        else:
            dot_file.write('"{0}" [shape=none]'.format(state.name))
    dot_file.write('"" -> "{0}"'.format(automata.initial.name))
    for state in automata.states():
        for symbol, nodes in state.transitions.iteritems():
            for node in nodes:
                dot_file.write('"{0}" -> "{1}" [label="{2}"]'.format(state.name, symbol, node.name))
    dot_file.write('}')


def save_automata(automata, automata_file):
    states = ''
    for index, state in enumerate(automata.states()):
        states +='{0}'.format(state.name)
        if index > 0:
            states +='\t'
    automata_file.write(states + '\n')

    symbols = ''
    for symbol in automata.symbols():
        symbols += '{0}'.format(symbol)

    automata_file.write(symbols + '\n')

    automata_file.write(automata.initial.name + '\n')

    finals_out = ''
    for index, final_state in enumerate(automata.finals):
        finals_out += '{0}'.format(final_state.name)
        if index > 0:
            finals_out += '\t'

    transitions_out = ''
    for state in automata.states():
        for symbol, nodes in state.transitions:
            for node in nodes:
                transitions_out += '{0}\t{1}\t{2}\n'.format(state.name, symbol, node.name)

    automata_file.write(transitions_out)
