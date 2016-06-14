# coding: utf-8

import six
import sys

from threading import local
from contextlib import contextmanager
from itertools import starmap
from pprint import PrettyPrinter


__version__ = "0.1.0"


ON_PYTHON2 = sys.version_info.major == 2

# this is a thread local storage, to make
# nested function calls to know about current
# indentation
_indent = local()


def force_unicode(value):
    """If input string is binary, then decode from utf-8."""
    if isinstance(value, six.binary_type):
        return value.decode('utf-8')
    return value


def format_value(value):
    """This function should return unicode representation of the value

    indent is used when value is displayed in column mode
    """
    if isinstance(value, six.binary_type):
        # suppose, all byte strings are in unicode
        # don't know if everybody in the world uses anything else?
        return u"'{0}'".format(value.decode('utf-8'))

    elif isinstance(value, six.text_type):
        return u"u'{0}'".format(value)

    elif isinstance(value, (list, tuple)):
        # long lists are shown vertically
        if len(value) > 3:
            pp = PrettyPrinter(indent=_get_indent() + 1)
            result = pp.pformat(value)
            return force_unicode(result)

    return force_unicode(repr(value))


def make_repr(*args):
    """Returns __repr__ method which returns ASCII
    representaion of the object with given fields.
    """

    def method(self):
        cls_name = self.__class__.__name__

        if args:
            field_names = args
        else:
            undercored = lambda name: name.startswith('_')
            is_method = lambda name: callable(getattr(self, name))

            good_name = lambda name: not undercored(name) \
                                 and not is_method(name)

            field_names = filter(good_name, dir(self))
            field_names = sorted(field_names)

        if len(field_names) > 2:
            # we need this, to print object with many fields nicely formatted,
            # outputing each field under the previous

            # increment indent for fields in column mode
            indent_increment = len(cls_name) + 2
            delimiter = u'\n'
        else:
            indent_increment = 0
            delimiter = u' '

        with _inc_indent(indent_increment):
            delimiter += u' ' * _get_indent()

            fields = ((name, format_value(getattr(self, name)))
                      for name in field_names)

            fields = starmap(u'{0}={1}'.format, fields)
            fields = delimiter.join(fields)

            result = u'<{cls_name} {fields}>'.format(
                cls_name=cls_name,
                fields=fields
            )

        if ON_PYTHON2:
            # on python 2.x repr returns bytes, but on python3 - unicode strings
            result = result.encode('utf-8')

        return result

    return method


@contextmanager
def _inc_indent(value):
    """Increments indentation value for the block of text.
    """

    if not hasattr(_indent, 'level'):
        _indent.level = value
    else:
        _indent.level += value

    yield

    _indent.level -= value


def _get_indent():
    """Returns current indent for output functions.
    """
    return getattr(_indent, 'level', 0)
