#!/usr/bin/env python2.7

import argparse

(StartMask, AMask, BMask, XMask,
    YMask, ZMask, UpMask, DownMask) = ((1 << x) for x in range(8))

(LeftMask, RightMask, LMask, RMask) = ((0, 1 << x) for x in range(4))

# no input
BLANK = "".join(chr(x) for x in (0, 0, 0, 0, 0x80, 0x80, 0x80, 0x80))


CHARAS = ['CAPTAIN', 'DONKEY', 'FOX',     'GAMEWATCH', 'KIRBY',
          'KOOPA',   'LINK',   'LUIGI',   'MARIO',     'MARS',
          'MEWTWO',  'NESS',   'PEACH',   'PIKACHU',   'POPONANA',
          'PURIN',   'SAMUS',  'YOSHI',   'ZE->SE',    'SE->ZE',
          'FALCO',   'CLINK',  'DRMARIO', 'EMBLEM',    'PICHU',
          'GANON',   None,     None,      None,        None,
          None,      None,     'POPO',    None]


def __main__():
    parser = argparse.ArgumentParser(
        description="Inject input into a Melee .dtm movie that simplifies extraction of animation frames.")
    parser.add_argument('chara', choices=CHARAS, help='the character to be used')
    parser.add_argument('palette', choices=range(6), type=int, help='the character to be used')
    parser.add_argument('outfile', metavar='outfile', type=str,
                        help='the destination of the modified .dtm file')
    parser.add_argument(
        'mode', choices=['white', 'black', 'labeled'], help='the type of movie to output')

    args = parser.parse_args()

    with open(args.outfile, "w") as f:
        # TODO copy DTM header
        f.write(data[0:0x100])

        # Generate sequence of TAS inputs.
        inputs = [StartMask,        # Access Debug Menu.
                  BMask]

        inputs += 4 * [DownMask]    # Set DB_LEVEL=DEVELOP.
        inputs += 4 * [RightMask]
        inputs += 4 * [UpMask]

        inputs += 3 * [AMask]       # root > VERSUS MODE > DAIRANTOU > CHAR SELECT

        # select P1 chara
        if CHARAS.find(args.chara) >= CHARAS.find('LINK'):
            inputs += (CHARAS.find(args.chara) - CHARAS.find('LINK')) * [RightMask]
        else:
            inputs += (CHARAS.find('LINK') - CHARAS.find(args.chara)) * [LeftMask]

        inputs += [BMask]

        inputs += 2 * [DownMask]    # Set PKIND_2=NONE.
        inputs += [AMask]
        inputs += [DownMask]
        inputs += 2 * [RightMask]
        inputs += [BMask]

        inputs += [DownMask]    # Set COLOR_1.
        inputs += args.palette * [RightMask]
        inputs += [BMask]

        inputs += 8 * [DownMask]    # Set STAGE=TEST.
        inputs += 31 * [LeftMask]

        inputs += 2 * [DownMask]
        inputs += [AMask]

        def ljust(ls, length, padchar):
            return (ls + [padchar] * length)[:length]

        # write the input 4 times, then nothing 4 times
        for input in inputs:
            for _ in range(4):
                f.write(''.join(chr(x) for x in ljust(ljust(input, 4, 0), 8, 1 << 7)))
            for _ in range(4):
                f.write(''.join(chr(x) for x in ljust(ljust([], 4, 0), 8, 1 << 7)))


if __name__ == "__main__":
    __main__()
