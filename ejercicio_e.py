# -*- coding: utf-8 -*-
#!/usr/bin/python

from parsers import load_automata
from writers import save_automata
from models import *

def complemento(archivo_automata1, archivo_automata):
    automata = load_automata(archivo_automata1)

    save_automata(afd_complemento(automata), archivo_automata)

def afd_complemento(automata):
    aut_con_trampa = add_terminal_node(automata)

    res = Automata(aut_con_trampa.states, aut_con_trampa.symbols, aut_con_trampa.initial, list(set(aut_con_trampa.states) - set(aut_con_trampa.finals)))
    res.prune_unreachable_states()
    return res
