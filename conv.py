#!/usr/bin/env python2.7

import argparse

(StartMask, AMask, BMask, XMask,
    YMask, ZMask, UpMask, DownMask) = (1 << x for x in range(8))

# no input
BLANK = "".join(chr(x) for x in (0, 0, 0, 0, 0x80, 0x80, 0x80, 0x80))

# C-stick up zooms out
ZOOM_OUT = "".join(chr(x) for x in (0, 1 << 0, 0, 0, 0x80, 0x80, 0x80, 0))
ZOOM_FRAMES = 10


def __main__():
    parser = argparse.ArgumentParser(
        description="Inject input into a Melee .dtm movie that simplifies extraction of animation frames.")
    parser.add_argument(
        'infile', metavar='infile', type=str, help='the .dtm file to be modified')
    parser.add_argument('outfile', metavar='outfile', type=str,
                        help='the destination of the modified .dtm file')
    parser.add_argument('frames_to_wait', metavar='frames_to_wait', type=int,
                        help='the number of frames to wait before injecting input')
    parser.add_argument(
        'mode', choices=['white', 'black', 'labeled'], help='the type of movie to output')

    args = parser.parse_args()

    with open(args.outfile, "w") as f:
        data = open(args.infile, "r").read()

        print(data)

        # copy DTM header
        f.write(data[0:0x100])
        # copy inputs until injection time
        f.write(data[0x100: 0x100 + (400 + args.frames_to_wait) * 0x8])

        # generate the sequence of inputs to be injected:
        #   - Start pauses the game;
        #   - Up, Up locks camera on P1;
        #   - X + Down cycles through: no HUD, white, black, normal;
        #   - Y + Down toggles labels.
        if args.mode == "white":
            initseq = [StartMask,
                       UpMask, UpMask,
                       XMask | DownMask, XMask | DownMask]
        elif args.mode == "black":
            initseq = [StartMask,
                       UpMask, UpMask,
                       XMask | DownMask, XMask | DownMask, XMask | DownMask]
        elif args.mode == "labeled":
            initseq = [StartMask,
                       UpMask, UpMask,
                       XMask | DownMask, XMask | DownMask, XMask | DownMask,
                       YMask | DownMask]
        else:
            raise ValueError('invalid mode: choose from {"white", "black", "labeled"}')

        # 1 frame of input translates to 4 lines of DTM, so we write every input 4 times
        for input in [item for sublist in [[i] * 4 + [0] * 4 for i in initseq] for item in sublist]:
            f.write(chr(input))
            f.write(BLANK[1:])

        # zoom out slightly to better capture sprites
        for _ in range(ZOOM_FRAMES):
            for _ in range(4):
                f.write(ZOOM_OUT)

        # unpause
        for _ in range(4):
            f.write(chr(StartMask))
            f.write(BLANK[1:])

        # copy the rest of the inputs
        f.write(data[0x100 + (args.frames_to_wait * 0x8):])

if __name__ == "__main__":
    __main__()
