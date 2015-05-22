#!/bin/sh

FILES_DIR=files
#FILE_IN1=$FILES_DIR/empieza_010.aut
#FILE_IN2=$FILES_DIR/termina_010.aut
FILE_IN1=$FILES_DIR/simple.aut
FILE_IN2=$FILES_DIR/simple.aut
FILE_OUT=$FILES_DIR/ejd.aut
DOT_OUT=$FILES_DIR/ejd.dot
PNG_OUT=$FILES_DIR/ejd.png

python AFD.py -intersec -aut1 $FILE_IN1 -aut2 $FILE_IN2 -aut $FILE_OUT
#python AFD.py -aut $FILE_OUT -dot $DOT_OUT
#dot -Tpng $DOT_OUT -o $PNG_OUT
#eog $PNG_OUT

