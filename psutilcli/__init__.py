import sys
import functools


COLORS_DISABLED = False


# ===================================================================
# --- python
# ===================================================================


def memoize(fun):
    """A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>
    """
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            return cache[key]
        except KeyError:
            ret = cache[key] = fun(*args, **kwargs)
            return ret

    def cache_clear():
        """Clear cache."""
        cache.clear()

    cache = {}
    wrapper.cache_clear = cache_clear
    return wrapper


# ===================================================================
# --- terminal / gui
# ===================================================================


@memoize
def term_supports_colors(file=sys.stdout):
    """Whether this terminal supports colors."""
    try:
        import curses
        assert file.isatty()
        curses.setupterm()
        assert curses.tigetnum("colors") > 0
    except Exception:
        return False
    else:
        return True


def colorstr(s, color=None, bold=False):
    """Return a coloured version of 'string'."""
    # http://misc.flogisoft.com/bash/tip_colors_and_formatting
    if COLORS_DISABLED or not term_supports_colors():
        return s

    attr = []

    if color is None:  # no color
        pass
    elif color == "red":
        attr.append('31')
    elif color == "green":
        attr.append('32')
    elif color == "yellow":
        attr.append('33')
    elif color == "blue":
        attr.append('34')
    elif color == "grey":
        attr.append('90')
    else:
        raise ValueError("invalid color %r" % color)

    if bold:
        attr.append('1')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)


def disable_colors():
    """Disable colorstr() function colorized output."""
    global COLORS_DISABLED
    COLORS_DISABLED = True


def get_percent_grid(perc, length=40):
    dashes = "|" * int((float(perc) / 10 * (length / 10)))
    tot_dashes = len(dashes)
    empty_dashes = " " * (length - tot_dashes)
    dashes = colorstr(
        dashes, "green" if perc <= 50 else "yellow" if perc < 90 else "red")
    perc = colorstr(
        str(perc) + "%",
        "green" if perc <= 50 else "yellow" if perc < 90 else "red")
    return "%s%s%s%-9s %14s" % (
        colorstr("[", bold=True),
        dashes,
        empty_dashes,
        colorstr("]", bold=True),
        perc
    )


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
