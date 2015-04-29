#!/bin/sh

FILES_DIR=files
FILE_IN1=$FILES_DIR/wikipedia.aut
FILE_IN2=$FILES_DIR/wikipedia_min.aut

python AFD.py -equival -aut1 $FILE_IN1 -aut2 $FILE_IN2
