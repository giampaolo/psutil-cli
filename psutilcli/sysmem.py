#!/usr/bin/env python

"""Shows system memory usage.

Usage: ps-sysmem [-p] [-b] [-N]

-h --help          print help
-p --parsable      output in a parsable format
-b --bytes         express numbers in bytes
-N --nocolors      turn off colors
"""

from __future__ import print_function

from docopt import docopt
import psutil

from psutilcli import bytes2human
from psutilcli import colorstr
from psutilcli import disable_colors
from psutilcli import get_percent_grid


BYTES = False


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value) if not BYTES else value
            print('%-10s:\t%12s' % (name, value))


def pprint_ntuple_parsable(nt, prefix):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value) if not BYTES else value
        else:
            value = "%s" % value
        print('%s.%s: %s' % (prefix, name, value))


def main():
    global BYTES, NOCOLORS
    args = docopt(__doc__)
    BYTES = args['--bytes']
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()
    if args['--nocolors']:
        disable_colors()

    if args['--parsable']:
        pprint_ntuple_parsable(virtual, "virtual")
        pprint_ntuple_parsable(swap, "swap")
    else:
        print('%s   %s' % (
            colorstr("Virtual", bold=1),
            get_percent_grid(virtual.percent)))
        print(colorstr('-' * 58, bold=1))
        pprint_ntuple(virtual)

        print()
        print('%s      %s' % (
            colorstr("Swap", bold=1),
            get_percent_grid(swap.percent)))
        print(colorstr('-' * 58, bold=1))
        pprint_ntuple(swap)


if __name__ == '__main__':
    main()
