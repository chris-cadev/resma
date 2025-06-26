#!/bin/bash -e
topic="${2:-"$(pdm run toml get --toml-path pyproject.toml project.version)"}"
filepath="$1/resma.$topic"
asciinema rec "$filepath.cast"
agg --font-family "CaskaydiaMono NF" --font-size 32 --speed 1 "$filepath.cast" $(dirname $filepath)/$(basename $filepath).gif
rm "$filepath.cast"
