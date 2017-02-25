#!/bin/bash

num_frames=499
gifsicle -U ani.gif `seq -f "#%g" 0 10 $num_frames` -O2 -o out.gif

printf "\n----------------------\n"
echo "Size of original gif: "$(du -sh ani.gif)
echo "Side of optimized gif: "$(du -sh out.gif)
