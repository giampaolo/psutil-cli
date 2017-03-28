#!/usr/bin/env python

"""Usage: psutil-procsmem [-h] [-s SORT]

Options:
  -h --help                # print this help
  -s [SORT] --sort [SORT]  # sort by column, either uss, pss, swap or pss

Description:
  Show "real" (USS) memory usage about all (querable) processes.
  "USS" (Unique Set Size) memory is probably the most representative metric
  for determining how much memory is actually being used by a process as it
  represents the amount of memory that would be freed if the process was
  terminated right now.
  This is similar to "smem" cmdline utility on Linux:
  https://www.selenic.com/smem/
"""

from __future__ import print_function
import sys

from docopt import docopt
import psutil

from psutilcli import bytes2human
from psutilcli import exit
from psutilcli import warn


def main():
    args = docopt(__doc__)
    if not args['--sort']:
        sort = 'uss'
    else:
        sort = args['--sort']
        valid_params = ('uss', 'pss', 'swap', 'rss')
        if sort not in valid_params:
            exit("invalid sort parameter %r; choose between %s" % (
                sort, ', '.join(valid_params)))

    if not (psutil.LINUX or psutil.OSX or psutil.WINDOWS):
        sys.exit("platform not supported")

    ad_pids = []
    procs = []
    for p in psutil.process_iter():
        with p.oneshot():
            try:
                info = p.as_dict(attrs=["pid", "cmdline", "username"])
                info['mem'] = p.memory_full_info()._asdict()
            except psutil.AccessDenied:
                ad_pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass
            else:
                procs.append(info)

    procs.sort(key=lambda p: p['mem'][sort])
    templ = "%-7s %-7s %-30s %7s %7s %7s %7s"
    print(templ % ("PID", "User", "Cmdline", "USS", "PSS", "Swap", "RSS"))
    print("=" * 78)
    for p in procs:
        uss = p["mem"]["uss"]
        if not uss:
            continue
        pss = p["mem"].get("pss", None)
        swap = p["mem"].get("swap", None)
        rss = p["mem"].get("rss", None)
        line = templ % (
            p["pid"],
            p["username"][:7],
            " ".join(p["cmdline"])[:30],
            bytes2human(uss),
            bytes2human(pss) if pss is not None else "",
            bytes2human(swap) if swap is not None else "",
            bytes2human(rss) if rss is not None else "",
        )
        print(line)
    if ad_pids:
        warn("access denied for %s pids which were skipped; "
             "try re-running as root" % (len(ad_pids)))


if __name__ == '__main__':
    main()
