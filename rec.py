from sys import argv
from PIL import Image
from pytesseract import image_to_string
from Levenshtein import seqratio
from re import match
from collections import defaultdict

import glob
import os

states = open("states.txt").read().split("\n")[:-1]

counts = defaultdict(int)

for infile in sorted(glob.iglob(argv[1])):
    im = Image.open(infile)

    state_rect = (370, 40, 660, 100)
    digit_rect = (660, 40, 800, 100)

    state_box = im.crop(state_rect).point(lambda p: p > 111)
    state_box.convert("1")

    state_text = image_to_string(
        state_box, config="-psm 7 -l hud bazaar").split("\n")[0]
    if match("\d+", state_text) or not state_text:
        continue
    else:
        state = state_text if state_text in states else max(
            states, key=lambda s: seqratio(state_text, s))

    digit_box = im.crop(digit_rect).point(lambda p: p > 100)
    digit_box.convert("1")

    digit = image_to_string(
        digit_box, config="-psm 7 -l hud -c tessedit_char_whitelist='0123456789' bazaar").split("\n")[0].replace(" ", "")

    digit = digit[:-2] + "_" + digit[-2:]

    title = "{0}_{1}".format(state.rjust(3, "0"), digit)
    counts[title] += 1

    os.system("mv -v {0} fox2_alpha/fox_{1}_{2}_{3}.png".format(
        infile.replace("label", "alpha"), state.lower(), counts[title], digit))
