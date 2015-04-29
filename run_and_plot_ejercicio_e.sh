#!/bin/sh

FILES_DIR=files
FILE_IN1=$FILES_DIR/termina_010.aut
#FILE_IN1=$FILES_DIR/empieza_010.aut
FILE_OUT=$FILES_DIR/eje.aut
DOT_OUT=$FILES_DIR/eje.dot
PNG_OUT=$FILES_DIR/eje.png

python AFD.py -complemento -aut1 $FILE_IN1 -aut $FILE_OUT
python AFD.py -aut $FILE_OUT -dot $DOT_OUT
dot -Tpng $DOT_OUT -o $PNG_OUT
eog $PNG_OUT

