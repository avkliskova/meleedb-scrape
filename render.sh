#!/bin/bash

dtm=${1%.dtm}

# mkdir "$dtm"_alpha "$dtm"_label

min=1899
max=2221
for n in $(seq $min $max); do
    echo -ne "Processing frame $((n - min)) / $((max - min))"\\r
    convert "$dtm"_white/"$dtm"_white$((n - 2)).png "$dtm"_black/"$dtm"_black$n.png \
        -quiet \
        -alpha off \
        \( -clone 0,1 -compose difference -composite -negate \) \
        \( -clone 0,2 +swap -compose divide -composite \) \
        -delete 0,1 +swap -compose Copy_Opacity -composite \
        "$dtm"_alpha/"$dtm"_alpha$n.png
    convert "$dtm"_labeled/"$dtm"_labeled$((n + 2)).png "$dtm"_black/"$dtm"_black$n.png \
        -quiet \
        -compose Minus_Src -composite \
        "$dtm"_label/"$dtm"_label$n.png
done
