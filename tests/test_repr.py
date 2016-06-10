# coding: utf-8

from nose.tools import eq_
from magic_repr import make_repr


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
            self.foo = 'бар'

        __repr__ = make_repr('foo')

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo='бар'>")


def test_two_value_are_shown_in_row():
    class TestMe(object):
        def __init__(self):
            self.foo = 'фу'
            self.bar = 'бар'

        __repr__ = make_repr('foo', 'bar')

    instance = TestMe()

    eq_(repr(instance),
        "<TestMe foo='фу' bar='бар'>")


def test_three_and_more_value_are_multiline():
    class TestMe(object):
        def __init__(self):
            self.foo = 'фу'
            self.bar = 'бар'
            self.bazz = 'базз'

        __repr__ = make_repr('foo', 'bar', 'bazz')

    instance = TestMe()

    expected = """
<TestMe foo='фу'
        bar='бар'
        bazz='базз'>
"""
    eq_(repr(instance),
        expected.strip())


def test_nested_values():
    class TestMe(object):
        def __init__(self, name, parent=None):
            self.name = name
            self.parent = parent

        __repr__ = make_repr('name', 'parent')

    parent = TestMe('родитель')
    instance = TestMe('дитя', parent)

    eq_(repr(instance),
        "<TestMe name='дитя' parent=<TestMe name='родитель' parent=None>>")


def test_when_value_is_in_the_list():
    class TestMe(object):
        def __init__(self):
            self.foo = 'фуу'

        __repr__ = make_repr('foo')

    instance = TestMe()
    lst = [instance]

    eq_(repr(lst),
        "[<TestMe foo='фуу'>]")


def test_when_instance_contains_list_of_values():
    class TestMe(object):
        def __init__(self):
            self.foo = list(range(3))

        __repr__ = make_repr('foo')

    instance = TestMe()
    eq_(repr(instance),
        "<TestMe foo=[0, 1, 2]>")
