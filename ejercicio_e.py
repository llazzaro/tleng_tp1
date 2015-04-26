# -*- coding: utf-8 -*- 
#!/usr/bin/python

from parsers import load_automata
from writers import save_automata
from models import Automata, Node

def complemento(archivo_automata1, archivo_automata):
    automata = load_automata(archivo_automata1)

    save_automata(afd_complemento(automata), archivo_automata)

def afd_complemento(automata):
    return Automata(automata.initial, automata.states().difference(automata.finals), automata.symbols(), automata.states())
