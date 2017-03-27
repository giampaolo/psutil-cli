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
        print('VIRTUAL')
        print('-------')
        pprint_ntuple(virtual)

        print()
        print('SWAP')
        print('----')
        pprint_ntuple(swap)


if __name__ == '__main__':
    main()
