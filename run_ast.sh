#!/bin/bash

python3 compiler.py /dump-ast hello_world.py
echo
python3 compiler.py /dump-ast minmax.py
echo
python3 compiler.py /dump-ast nod.py
echo
python3 compiler.py /dump-ast strinstr.py
echo
python3 compiler.py /dump-ast strinstr.py