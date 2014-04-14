# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division	

"""
Created on Mon Apr 14 12:20:24 2014

@author: sympy team
"""

"""
Reimplementations of constructs introduced in later versions of Python than
we support. Also some functions that are needed SymPy-wide and are located
here for easy import.
"""

import operator
from collections import defaultdict


"""
Python 2 and Python 3 compatible imports

String and Unicode compatible changes:
    * `unicode()` removed in Python 3, import `unicode` for Python 2/3
      compatible function
    * `unichr()` removed in Python 3, import `unichr` for Python 2/3 compatible
      function
    * Use `u()` for escaped unicode sequences (e.g. u'\u2020' -> u('\u2020'))
    * Use `u_decode()` to decode utf-8 formatted unicode strings
    * `string_types` gives str in Python 3, unicode and str in Python 2,
      equivalent to basestring

Integer related changes:
    * `long()` removed in Python 3, import `long` for Python 2/3 compatible
      function
    * `integer_types` gives int in Python 3, int and long in Python 2

Types related changes:
    * `class_types` gives type in Python 3, type and ClassType in Python 2

Renamed function attributes:
    * Python 2 `.func_code`, Python 3 `.__func__`, access with
      `get_function_code()`
    * Python 2 `.func_globals`, Python 3 `.__globals__`, access with
      `get_function_globals()`
    * Python 2 `.func_name`, Python 3 `.__name__`, access with
      `get_function_name()`

Moved modules:
    * `reduce()`
    * `StringIO()`
    * `cStringIO()` (same as `StingIO()` in Python 3)
    * Python 2 `__builtins__`, access with Python 3 name, `builtins`

Iterator/list changes:
    * `xrange` removed in Python 3, import `xrange` for Python 2/3 compatible
      iterator version of range

exec:
    * Use `exec_()`, with parameters `exec_(code, globs=None, locs=None)`

Metaclasses:
    * Use `with_metaclass()`, examples below
        * Define class `Foo` with metaclass `Meta`, and no parent:
            class Foo(with_metaclass(Meta)):
                pass
        * Define class `Foo` with metaclass `Meta` and parent class `Bar`:
            class Foo(with_metaclass(Meta, Bar)):
                pass
"""

import sys
PY3 = sys.version_info[0] > 2

if PY3:
    class_types = type,
    integer_types = (int,)
    string_types = (str,)
    long = int

    # String / unicode compatibility
    unicode = str
    unichr = chr
    def u(x):
        return x
    def u_decode(x):
        return x

    Iterator = object

    # Moved definitions
    get_function_code = operator.attrgetter("__code__")
    get_function_globals = operator.attrgetter("__globals__")
    get_function_name = operator.attrgetter("__name__")

    import builtins
    from functools import reduce
    from io import StringIO
    cStringIO = StringIO

    exec_ = getattr(builtins, "exec")

    xrange = range
else:
    import codecs
    import types

    class_types = (type, types.ClassType)
    integer_types = (int, long)
    string_types = (str, unicode)
    long = long

    # String / unicode compatibility
    unicode = unicode
    unichr = unichr
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
    def u_decode(x):
        return x.decode('utf-8')

    class Iterator(object):
        def next(self):
            return type(self).__next__(self)

    # Moved definitions
    get_function_code = operator.attrgetter("func_code")
    get_function_globals = operator.attrgetter("func_globals")
    get_function_name = operator.attrgetter("func_name")

    import __builtin__ as builtins
    reduce = reduce
    from StringIO import StringIO
    from cStringIO import StringIO as cStringIO

    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("exec _code_ in _globs_, _locs_")

    xrange = xrange

# These are in here because telling if something is an iterable just by calling
# hasattr(obj, "__iter__") behaves differently in Python 2 and Python 3.  In
# particular, hasattr(str, "__iter__") is False in Python 2 and True in Python 3.
# I think putting them here also makes it easier to use them in the core.

class NotIterable:
    """
    Use this as mixin when creating a class which is not supposed to return
    true when iterable() is called on its instances. I.e. avoid infinite loop
    when calling e.g. list() on the instance
    """
    pass

def iterable(i, exclude=(string_types, dict, NotIterable)):
    """
    Return a boolean indicating whether ``i`` is an iterable.
    True also indicates that the iterator is finite, i.e. you e.g.
    call list(...) on the instance.

    When it is working with iterables, it is almost always assuming
    that the iterable is not a string or a mapping, so those are excluded
    by default. If you want a pure Python definition, make exclude=None. To
    exclude multiple items, pass them as a tuple.

    See also: is_sequence

    Examples
    ========

    >>> from sympy.utilities.iterables import iterable
    >>> from sympy import Tuple
    >>> things = [[1], (1,), set([1]), Tuple(1), (j for j in [1, 2]), {1:2}, '1', 1]
    >>> for i in things:
    ...     print('%s %s' % (iterable(i), type(i)))
    True <... 'list'>
    True <... 'tuple'>
    True <... 'set'>
    True <class 'sympy.core.containers.Tuple'>
    True <... 'generator'>
    False <... 'dict'>
    False <... 'str'>
    False <... 'int'>

    >>> iterable({}, exclude=None)
    True
    >>> iterable({}, exclude=str)
    True
    >>> iterable("no", exclude=str)
    False

    """
    try:
        iter(i)
    except TypeError:
        return False
    if exclude:
        return not isinstance(i, exclude)
    return True

try:
    from functools import cmp_to_key
except ImportError: # <= Python 2.6
    def cmp_to_key(mycmp):
        """
        Convert a cmp= function into a key= function
        """
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

try:
    from itertools import zip_longest
except ImportError: # <= Python 2.7
    from itertools import izip_longest as zip_longest

try:
    from itertools import combinations_with_replacement
except ImportError:  # <= Python 2.6
    def combinations_with_replacement(iterable, r):
        """Return r length subsequences of elements from the input iterable
        allowing individual elements to be repeated more than once.

        Combinations are emitted in lexicographic sort order. So, if the
        input iterable is sorted, the combination tuples will be produced
        in sorted order.

        Elements are treated as unique based on their position, not on their
        value. So if the input elements are unique, the generated combinations
        will also be unique.

        See also: combinations

        Examples
        ========

        >>> from sympy.core.compatibility import combinations_with_replacement
        >>> list(combinations_with_replacement('AB', 2))
        [('A', 'A'), ('A', 'B'), ('B', 'B')]
        """
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [0] * r
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)

