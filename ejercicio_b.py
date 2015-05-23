# -*- coding: utf-8 -*-
#!/usr/bin/python

from parsers import load_automata


def pertenece_al_lenguaje(archivo_automata, cadena):
    automata = load_automata(archivo_automata)

    result = automata.accepts(cadena)

    if result:
        print 'TRUE'
        return True
    else:
        print 'FALSE'
        return False
