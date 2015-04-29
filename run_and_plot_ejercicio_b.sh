#!/bin/sh

FILES_DIR=files
FILE_IN=test/automata_pruebas.aut
DOT_OUT=$FILES_DIR/ejc.dot
PNG_OUT=$FILES_DIR/ejc.png

python AFD.py -aut $FILE_IN -dot $DOT_OUT
dot -Tpng $DOT_OUT -o $PNG_OUT
