#!/usr/bin/env python

"""
"""

from __future__ import print_function

import psutil


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        else:
            value = "%s%%" % value
        print('%-10s:\t%7s' % (name, value))


def main():
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print('VIRTUAL')
    print('-------')
    pprint_ntuple(virtual)

    print()
    print('SWAP')
    print('----')
    pprint_ntuple(swap)


if __name__ == '__main__':
    main()
