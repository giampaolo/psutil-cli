#!/usr/bin/env python

"""Shows system memory usage.

Usage: ps-sysmem [-p] [-b]

-h --help          print help
-p --parsable      output in a parsable format
-b --bytes         express numbers in bytes
"""

from __future__ import print_function

from docopt import docopt
import psutil

from psutilcli import bytes2human
from psutilcli import colorstr


BYTES = False


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value) if not BYTES else value
        else:
            value = "%s%%" % value
        print('%-10s:\t%7s' % (name, value))


def pprint_ntuple_parsable(nt, prefix):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value) if not BYTES else value
        else:
            value = "%s%%" % value
        print('%s.%s: %s' % (prefix, name, value))


def get_percent_grid(perc, length=40):
    dashes = "|" * int((float(perc) / 10 * (length / 10)))
    tot_dashes = len(dashes)
    empty_dashes = " " * (length - tot_dashes)
    dashes = colorstr(
        dashes, "green" if perc <= 50 else "yellow" if perc <= 75 else "red")
    perc = colorstr(
        str(perc) + "%",
        "green" if perc <= 50 else "yellow" if perc <= 75 else "red")
    return "%s%s%s %14s%s" % (
        colorstr("[", bold=True),
        dashes,
        empty_dashes,
        perc,
        colorstr("]", bold=True))


def main():
    global BYTES
    args = docopt(__doc__)
    BYTES = args['--bytes']
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if args['--parsable']:
        pprint_ntuple_parsable(virtual, "virtual")
        pprint_ntuple_parsable(virtual, "swap")
    else:
        print('%s   %s' % (
            colorstr("Virtual", bold=1),
            get_percent_grid(virtual.percent)))
        print(colorstr('-' * 57, bold=1))
        pprint_ntuple(virtual)

        print()
        print('%s      %s' % (
            colorstr("Swap", bold=1),
            get_percent_grid(swap.percent)))
        print(colorstr('-' * 58, bold=1))
        pprint_ntuple(swap)


if __name__ == '__main__':
    main()
