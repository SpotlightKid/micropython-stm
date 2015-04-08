#!/bin/bash

NOTEBOOK="micropython-stm"

ipython nbconvert --to markdown "$NOTEBOOK.ipynb"
mv -f "$NOTEBOOK.md" README.md
ipython nbconvert --to slides --post serve "$NOTEBOOK.ipynb"

