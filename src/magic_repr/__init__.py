# coding: utf-8

from itertools import starmap

__version__ = "0.1.0"


def format_value(value):
    """This function should return unicode representation of the value
    """
    if isinstance(value, str):
        # suppose, all byte strings are in unicode
        # don't know if everybody in the world uses anything else?
        return u"'{0}'".format(value.decode('utf-8'))

    elif isinstance(value, unicode):
        return u"u'{0}'".format(value)

    return repr(value).decode('utf-8')


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
            delimiter = u'\n' + u' ' * (len(cls_name) + 2)
        else:
            delimiter = u' '

        fields = ((name, format_value(getattr(self, name)))
                  for name in field_names)

        fields = starmap(u'{0}={1}'.format, fields)
        fields = delimiter.join(fields)

        result = u'<{cls_name} {fields}>'.format(
            cls_name=cls_name,
            fields=fields
        )
        return result.encode('utf-8')

    return method
