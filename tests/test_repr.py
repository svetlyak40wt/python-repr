# coding: utf-8

from __future__ import division, absolute_import
from __future__ import print_function

from nose.tools import eq_
from magic_repr import (
    make_repr,
    _get_indent,
    _inc_indent)


def test_automatic_builder_sorts_alphabetically():
    class TestMe(object):
        def __init__(self):
            self.foo = 1
            self.bar = 2

        __repr__ = make_repr()

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe bar=2 foo=1>")


def test_automatic_builder_ignores_underscored_attributes():
    class TestMe(object):
        def __init__(self):
            self.foo = 1
            self._bar = 2

        __repr__ = make_repr()

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo=1>")


def test_automatic_builder_ignores_methods():
    class TestMe(object):
        def __init__(self):
            self.foo = 1

        def bar(self):
            return 2

        __repr__ = make_repr()

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo=1>")


def test_with_unicode_value():
    class TestMe(object):
        def __init__(self):
            self.foo = u'бар'

        __repr__ = make_repr('foo')

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo=u'бар'>")


def test_utf8_value():
    class TestMe(object):
        def __init__(self):
            # this reformatting needed to convence Python3
            # that we want to put bytes into this attribute
            self.foo = u'бар'.encode('utf-8')

        __repr__ = make_repr('foo')

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo='бар'>")


def test_two_value_are_shown_in_row():
    class TestMe(object):
        def __init__(self):
            self.foo = u'фу'
            self.bar = u'бар'

        __repr__ = make_repr('foo', 'bar')

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo=u'фу' bar=u'бар'>")


def test_three_and_more_value_are_multiline():
    class TestMe(object):
        def __init__(self):
            self.foo = u'фу'
            self.bar = u'бар'
            self.bazz = u'базз'

        __repr__ = make_repr('foo', 'bar', 'bazz')

    instance = TestMe()

    expected = """
<TestMe foo=u'фу'
        bar=u'бар'
        bazz=u'базз'>
"""
    eq_(repr(instance),
        expected.strip())


def test_nested_values():
    class TestMe(object):
        def __init__(self, name, parent=None):
            self.name = name
            self.parent = parent

        __repr__ = make_repr('name', 'parent')

    parent = TestMe(u'родитель')
    instance = TestMe(u'дитя', parent)

    eq_(repr(instance),
        "<TestMe name=u'дитя' parent=<TestMe name=u'родитель' parent=None>>")


def test_when_value_is_in_the_list():
    class TestMe(object):
        def __init__(self):
            self.foo = u'фуу'

        __repr__ = make_repr('foo')

    instance = TestMe()
    lst = [instance]

    eq_(repr(lst),
        "[<TestMe foo=u'фуу'>]")


def test_when_instance_contains_list_of_values():
    class TestMe(object):
        def __init__(self):
            self.foo = list(range(3))

        __repr__ = make_repr('foo')

    instance = TestMe()
    eq_(repr(instance),
        "<TestMe foo=[0, 1, 2]>")


def test_long_list_shown_vertically():
    class TestMe(object):
        def __init__(self):
            self.foo = list(range(25))

        __repr__ = make_repr('foo')

    instance = TestMe()
    expected = """
<TestMe foo=[0,
             1,
             2,
             3,
             4,
             5,
             6,
             7,
             8,
             9,
             10,
             11,
             12,
             13,
             14,
             15,
             16,
             17,
             18,
             19,
             20,
             21,
             22,
             23,
             24]
"""
    eq_(repr(instance),
        expected.strip())


def test_zero_indent():
    # By default, indent is zero
    eq_(_get_indent(), 0)


def test_inc_indent():
    # check if nested _inc_indent calls increment indentation level

    with _inc_indent(2):
        # first increment
        eq_(_get_indent(), 2)

        # second
        with _inc_indent(5):
            eq_(_get_indent(), 7)

        # now second value should be substracted
        eq_(_get_indent(), 2)

    # and finally, first value substracted
    eq_(_get_indent(), 0)
