#!/bin/bash

frames() {
    n=$(ffprobe -v error -count_frames -select_streams v:0 \
        -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 $1)
    ffmpeg -i $1 -vf fps=60,scale=1080:-1:flags=lanczos $2%0${#n}d.png
}

dtm=${1%.dtm}
frames=$2

dump=~/.dolphin-emu/Dump/Frames/framedump0.avi

python2 conv.py $dtm.dtm "$dtm"_white.dtm   $2 white
dolphin -m "$dtm"_white.dtm
mv $dump "$dtm"_white.avi

python2 conv.py $dtm.dtm "$dtm"_black.dtm   $2 black
dolphin -m "$dtm"_black.dtm
mv $dump "$dtm"_black.avi

python2 conv.py $dtm.dtm "$dtm"_labeled.dtm $2 annotated
dolphin -m "$dtm"_labeled.dtm
mv $dump "$dtm"_labeled.avi

frames "$dtm"_black.avi "$dtm"_black
frames "$dtm"_white.avi "$dtm"_white
frames "$dtm"_labeled.avi "$dtm"_labeled

# frames=$(ffprobe -v error -count_frames -select_streams v:0 \
#       -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 $file)

#for n in {1236..1825}; do
#    echo $n
#    convert white$((n + 16)).png black$n.png \
#        -alpha off \
#        \( -clone 0,1 -compose difference -composite -negate \) \
#        \( -clone 0,2 +swap -compose divide -composite \) \
#        -delete 0,1 +swap -compose Copy_Opacity -composite \
#        alpha$n.png
#done
