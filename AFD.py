# -*- coding: utf-8 -*- 
#!/usr/bin/python

import sys
import os

from ejercicio_a import afd_minimo
from ejercicio_b import pertenece_al_lenguaje
from ejercicio_c import grafo
from ejercicio_d import interseccion
from ejercicio_e import complemento
from ejercicio_f import equivalentes


def parametros_coinciden(parametros, *patron):
    if len(parametros) != len(patron):
        return False

    for esperado, recibido in zip(patron, parametros):
        if esperado is not None and esperado != recibido:
            return False

    return True


def archivo_para_leer(ruta):
    if not os.path.exists(ruta):
        sys.exit("El archivo '%s' no existe." % ruta)
    elif not os.path.isfile(ruta):
        sys.exit("El archivo '%s' es invalido." % ruta)

    return open(ruta, "r")


def archivo_para_escribir(ruta):
    ruta_completa = os.path.realpath(ruta)
    directorio = os.path.dirname(ruta_completa)
    if not os.access(directorio, os.W_OK):
        sys.exit("El archivo '%s' no puede escribirse." % ruta)

    return open(ruta, "w")


if __name__ == "__main__":
    parametros = sys.argv[1:]

    try:
        if parametros_coinciden(parametros, "-leng", None, "-aut", None):
            archivo_regex = archivo_para_leer(parametros[1])
            archivo_automata = archivo_para_escribir(parametros[3])
            afd_minimo(archivo_regex, archivo_automata)
            sys.exit(0)
        elif parametros_coinciden(parametros, "-aut", None, None):
            archivo_automata = archivo_para_leer(parametros[1])
            cadena = parametros[2]
            pertenece_al_lenguaje(archivo_automata, cadena)
            sys.exit(0)
        elif parametros_coinciden(parametros, "-aut", None, "-dot", None):
            archivo_automata = archivo_para_leer(parametros[1])
            archivo_dot = archivo_para_escribir(parametros[3])
            grafo(archivo_automata, archivo_dot)
            sys.exit(0)
        elif parametros_coinciden(parametros, "-intersec", "-aut1", None, "-aut2", None, "-aut", None):
            archivo_automata1 = archivo_para_leer(parametros[2])
            archivo_automata2 = archivo_para_leer(parametros[4])
            archivo_automata = archivo_para_escribir(parametros[6])
            interseccion(archivo_automata1, archivo_automata2, archivo_automata)
            sys.exit(0)
        elif parametros_coinciden(parametros, "-complemento", "-aut1", None, "-aut", None):
            archivo_automata1 = archivo_para_leer(parametros[2])
            archivo_automata = archivo_para_escribir(parametros[4])
            complemento(archivo_automata1, archivo_automata)
            sys.exit(0)
        elif parametros_coinciden(parametros, "-equival", "-aut1", None, "-aut2", None):
            archivo_automata1 = archivo_para_leer(parametros[2])
            archivo_automata2 = archivo_para_leer(parametros[4])
            equivalentes(archivo_automata1, archivo_automata2)
            sys.exit(0)
    except NotImplementedError:
        sys.exit("Funcionalidad no implementada.")

    print "Parametros invalidos."
    print "Uso:"
    print 
    print "afd -leng <archivo_regex> -aut <archivo_automata>"
    print "afd -aut <archivo_automata> <cadena>"
    print "afd -aut <archivo_automata> -dot <archivo_dot>"
    print "afd -intersec -aut1 <archivo_automata> -aut2 <archivo_automata> -aut <archivo_automata>"
    print "afd -complemento -aut1 <archivo_automata> -aut <archivo_automata>"
    print "afd -equival -aut1 <archivo_automata> -aut2 <archivo_automata>"

    sys.exit(1)
