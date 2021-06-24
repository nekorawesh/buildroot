#!/bin/sh
UI_DIR="/usr/local/cpx/ui"

if [ -d "$UI_DIR" ]; then         
    cd $UI_DIR
    python gui.py &
else
    echo "ui direcotry not found!"       
fi