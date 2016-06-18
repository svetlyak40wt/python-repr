# coding: utf-8

from __future__ import division, absolute_import
from __future__ import print_function

from itertools import repeat
from nose.tools import eq_
from magic_repr import (
    ON_PYTHON2,
    serialize_list,
    serialize_text,
    is_multiline,
    format_value,
    make_repr,
    padding_adder)


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

    expected = """
<TestMe name=u'дитя'
        parent=<TestMe name=u'родитель'
                       parent=None>>
"""
    eq_(repr(instance), expected.strip())


def test_nested_values_with_padded_fields():
    # Check if fields of the nested attribute
    # will be padded with right padding

    class TestMe(object):
        def __init__(self, name, parent=None):
            self.name = name
            self.parent = parent
            self.foo = False

        __repr__ = make_repr('parent', 'foo', 'name')

    parent = TestMe(u'родитель')
    instance = TestMe(u'дитя', parent)

    expected = """
<TestMe parent=<TestMe parent=None
                       foo=False
                       name=u'родитель'>
        foo=False
        name=u'дитя'>
"""
    eq_(repr(instance), expected.strip())


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
             24]>
"""

    eq_(repr(instance),
        expected.strip())


def test_list_attribute_can_contain_another_repred_objects_with_indentaion():
    class Bar(object):
        def __init__(self):
            self.first = 1
            self.second = 2
            self.third = 3

        __repr__ = make_repr()

    class Foo(object):
        def __init__(self):
            self.bars = [Bar() for i in range(3)]

        __repr__ = make_repr()

    instance = Foo()

    expected = """
<Foo bars=[<Bar first=1
                second=2
                third=3>,
           <Bar first=1
                second=2
                third=3>,
           <Bar first=1
                second=2
                third=3>]>
"""

    eq_(repr(instance), expected.strip())



def test_format_for_long_list():
    value = list(range(25))
    expected = u"""
[0,
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
    eq_(format_value(value), expected.strip())


def test_is_multiline():
    eq_(is_multiline('blah'), False)
    eq_(is_multiline('blah\nminor'), True)


def test_serialize_list_of_texts_when_there_are_few_oneline_short_texts():
    lst = ['a=foo', 'b=bar']
    output = '<SomeClass '
    expected = '<SomeClass a=foo b=bar'

    result = serialize_list(output, lst)
    eq_(result, expected)


def test_serialize_list_can_use_delimiters():
    lst = ['blah=minor', 'foo=bar']
    output = ''
    expected = 'blah=minor, foo=bar'

    result = serialize_list(output, lst, delimiter=u',')
    eq_(result, expected)


def test_serialize_list_of_texts_when_there_is_one_multiline_text():
    # In this case, all texts in the list should be serialized
    # in one column
    lst = ['blah=minor', 'foo=foo\n    bar']
    output = '<SomeClass '
    expected = """
<SomeClass blah=minor
           foo=foo
               bar
"""

    result = serialize_list(output, lst)
    eq_(result, expected.strip())


def test_serialize_list_of_texts_when_multiline_text_goes_first():
    # In this case, all texts in the list should be serialized
    # in one column and first texts's lines should be formatted each
    # under another
    lst = ['foo=foo\n    bar', 'blah=minor']
    output = '<SomeClass '
    expected = """
<SomeClass foo=foo
               bar
           blah=minor
"""

    result = serialize_list(output, lst)
    eq_(result, expected.strip())


def test_serialize_list_should_use_column_mode_when_there_are_long_items():
    # In this case, all texts in the list should be serialized
    # in one column and first texts's lines should be formatted each
    # under another.
    # Column mode is selected because summary item's length is more than 20

    lst = ['this-is-a-foo-bar-string', 'and-blah-minor']
    output = '<SomeClass '
    expected = """
<SomeClass this-is-a-foo-bar-string
           and-blah-minor

"""

    result = serialize_list(output, lst)
    eq_(result, expected.strip())


def test_padding_adder():
    adder = padding_adder(4)

    # testing that padding adder works for oneline texts
    eq_(adder('blah'), '    blah')

    # testing that padding adder works with multiline
    eq_(adder('foo\nbar'), '    foo\n    bar')

    # checking if adder don't touch leading spaces
    eq_(adder('foo\n  bar'), '    foo\n      bar')


def test_serialize_text():
    eq_(serialize_text(u'фуу ', u'бар'),
        u'фуу бар')

    eq_(serialize_text(u'foo ', u'bar\nbazz'),
        u'foo bar\n    bazz')

    eq_(serialize_text(u'фуу ', u'бар\nбаз'),
        u'фуу бар\n    баз')


def test_on_instance_which_has_dict_attribute():
    # In this case, we expect, the dict will be pretty-printed
    class TestMe(object):
        def __init__(self):
            self.foo = {u'foo': u'bar',
                        u'блах': u'минор'}

        __repr__ = make_repr()

    instance = TestMe()

    if ON_PYTHON2:
        expected = """
<TestMe foo={u'foo': u'bar',
             u'блах': u'минор'}>
"""
    else:
        # Python3 has slightly different PrettyPrinter.
        # It does not output "u" for strings and wraps
        # text more smartly
        expected = "<TestMe foo={'foo': 'bar', 'блах': 'минор'}>"

    result = repr(instance)
    eq_(result, expected.strip())


def test_if_attribute_can_be_generated_by_callable():
    # In this case, we check if make_repr can
    # accept keyword arguments, where value is
    # a callable which returns attribute's value

    class TestMe(object):
        def some_method(self):
            return u'Минор'

    TestMe.__repr__ = make_repr(blah=TestMe.some_method)

    instance = TestMe()

    expected = "<TestMe blah=u'Минор'>"
    result = repr(instance)
    eq_(result, expected.strip())
