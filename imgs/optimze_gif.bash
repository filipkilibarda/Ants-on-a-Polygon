#!/bin/bash

gifsicle -O3 --colors 4 --use-colormap gray < ani.gif > out.gif

printf "\n----------------------\n"
echo "Size of original gif: "$(du -sh ani.gif)
echo "Side of optimized gif: "$(du -sh out.gif)
