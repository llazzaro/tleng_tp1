# -*- coding: utf-8 -*-
#!/usr/bin/python

from parsers import load_automata
from writers import save_automata
from models import Automata, Node
from ejercicio_a import copy_with_terminal_node

def complemento(archivo_automata1, archivo_automata):
    automata = load_automata(archivo_automata1)

    save_automata(afd_complemento(automata), archivo_automata)

def afd_complemento(automata):
    aut_con_trampa = copy_with_terminal_node(automata)

    res = Automata(aut_con_trampa.initial, set(aut_con_trampa.states()).difference(set(aut_con_trampa.finals)), aut_con_trampa.symbols(), aut_con_trampa.states())
    res.prune_unreachable_states()
    return res
