#!/usr/bin/env python

"""
"""

from __future__ import print_function

import psutil

from psutilcli import bytes2human


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
