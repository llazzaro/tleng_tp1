# -*- coding: utf-8 -*-
#!/usr/bin/python

from parsers import load_automata
from writers import save_dot


def grafo(archivo_automata, archivo_dot):
    automata = load_automata(archivo_automata)

    save_dot(automata, archivo_dot)
