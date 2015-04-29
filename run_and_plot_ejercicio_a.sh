#!/bin/sh

FILES_DIR=files
FILE_IN1=$FILES_DIR/4_3_arbol_ejemplo_1
FILE_OUT=$FILES_DIR/eja.aut
DOT_OUT=$FILES_DIR/eja.dot
PNG_OUT=$FILES_DIR/eja.png

python AFD.py -leng $FILE_IN1 -aut $FILE_OUT
python AFD.py -aut $FILE_OUT -dot $DOT_OUT
dot -Tpng $DOT_OUT -o $PNG_OUT
