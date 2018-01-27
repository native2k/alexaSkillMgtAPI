#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import types
import re
import functools
from copy import copy
from pprint import pformat

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())


class Field(object):
    """ A manifest field """

    def __init__(self, key):
        self._key = key

    def __set__(self, obj, val):
        # log.debug( "__set__ %s %s" % (obj, val))
        obj._obj.set(self._key, val, **obj._kwargs)

    def __get__(self, obj, objtype):
        # log.debug("__get__ %s %s" % (obj, objtype))
        # log.debug("Field: _key %s obj._kwargs %s" % (self._key, obj._kwargs))
        return obj._obj.get(self._key, **obj._kwargs)


class ParamField(object):
    """ Container for parametrized manifest field """

    def __init__(self, obj, **kwargs):
        super(ParamField, self).__init__()
        self._kwargs = kwargs
        self._obj = obj


def validConvert(value, adef):
    # print "aDef: %s value: %s Valuetyep: %s" % (adef, value, type(value))
    # if not isinstance(adef, types.ListType):
    #     print "isnstand %s"  % isinstance(value, adef)
    if isinstance(adef, types.ListType):
        if value not in adef:
            raise ValueError('Value "%s" must be one of %s' % (
                value, adef))
    elif not isinstance(value, adef):
        if adef == types.StringType and isinstance(value, types.IntType) and not isinstance(value, types.BooleanType):
            return str(value)   # exception for numeric value
        elif adef == types.BooleanType and value in [1, 0]:
            return bool(value)

        raise ValueError('Value "%s" is type %s but must be %s' % (
            value, type(value), adef))
    return value


class ListOverlay(list):

    class Iterator():
        def __init__(self, n, reverse=False):
            self.i = 0
            self.reverse = reverse
            if self.reverse:
                self.i = len(n) - 1
            self.n = n

        def __iter__(self):
            return self

        def next(self):
            if self.i < len(self.n) and self.i >= 0:
                i = self.n[self.i]
                if self.reverse:
                    self.i -= 1
                else:
                    self.i += 1
                return i
            else:
                raise StopIteration()

    def __init__(self, definition, orig, allowedTypes=None):
        self._definition = definition
        self._orig = orig
        self._allowedTypes = allowedTypes

    def _doValidate(self, value):
        if self._allowedTypes is None:
            return value
        else:
            return validConvert(value, self._allowedTypes)

    def __add__(self, y):
        res = self._orig.__add__([{self._definition: _doValidate(v)} for v in y])
        return ListOverlay(self._definition, res, self._allowedTypes)

    def __contains__(self, y):
        return self._orig.__contains__({self._definition: y})

    def __delitem__(self, y):
        self._orig.__delitem__(y)

    def __delslice__(self, i, j):
        self._orig.__delslice__(i, j)

    def __eq__(self, y):
        return self._orig.__eq__([{self._definition: v} for v in y])

    # format?
    def __ge__(self, y):
        return self._orig.__ge__([{self._definition: v} for v in y])

    def __getitem__(self, y):
        return self._orig.__getitem__(y)[self._definition]

    def __getslice__(self, i, y):
        return [n[self._definition] for n in self._orig.__getslice__(i, j)]

    def __gt__(self, y):
        return self._orig.__gt__([{self._definition: v} for v in y])

    def __hash__(self):
        return self._orig.__hash__()

    def __iadd__(self, y):
        self._orig.__iadd__([{self._definition: v} for v in y])
        return self

    def __imul__(self, y):
        self._orig.__imul__([{self._definition: v} for v in y])
        return self

    def __ne__(self, y):
        return self._orig.__ne__([{self._definition: v} for v in y])

    def __iter__(self):
        return self.Iterator(self)


    def __le__(self, y):
        return self._orig.__le__([{self._definition: v} for v in y])

    def __len__(self):
        return self._orig.__len__()

    def __lt__(self, y):
        return self._orig.__lt__([{self._definition: v} for v in y])

    def __mul__(self, y):
        res = self._orig.__mul__([{self._definition: v} for v in y])
        return ListOverlay(self._definition, res)

    def __ne__(self, y):
        return self._orig.__lt__([{self._definition: v} for v in y])

    def __repr__(self):
        return [v[self._definition] for v in self._orig].__repr__()

    def __reversed__(self):
        return self.Iterator(self, True)

    def __rmul__(self, n):
        return ListOverlay(self._definition, self._orig.__rmul__(n), self._allowedTypes)

    def __setitem__(self, i, y):
        self._orig[i][self._definition] = self._doValidate(y)

    def __setslice__(self, i, j, y):
        self._orig[i:j] = [{self._definition: self._doValidate(n)} for n in y]

    def __sizeof__(self):
        return self._orig.__sizeof__()

    def extend(self, iterable):
        for i in iterable:
            self.append(self._doValidate(i))

    def append(self, object):
        self._orig.append({self._definition: self._doValidate(object)})

    def index(self, object):
        return self._orig.index({self._definition: object})

    def insert(self, index, object):
        return self._orig.insert(index, {self._definition: self._doValidate(object)})

    def pop(self, index=-1):
        return self._orig.pop(index)[self._definition]

    def remove(self, value):
        return self._origi.remove({self._definition: value})

    def reverse(self):
        self._orig.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        cmpNew = None
        if cmp is not None:
            def cmpNew(x, y):
                return cmp(x[self._definition], y[self._definition])

        self._orig.sort(cmpNew, key, reverse)


class RestrictedDict():
    def __init__(self, definition, *args, **kwargs):
        self._definition = definition
        self._data = dict(*args, **kwargs)

    def __setitem__(self, key, value):
        self._data[key] = validConvert(value, self._definition.get(key))

    def setdefault(self, key, value=None):
        return self._data.setdefault(key, validConvert(value, self._definition.get(key)))

    def __getattr__(self, attrib):
        # log.debug("__getattr__ called for %s" % attrib)
        return getattr(self._data, attrib)

    # def __setattr__(self, attrib, value):
    #     if attrib not in ['_definition', 'self._data']
    #     return setattr(self._data, attrib, value)


class RestrictedList():
    def __init__(self, definition, *args, **kwargs):
        self._definition = definition
        self._data = list(*args, **kwargs)

    def __setitem__(self, key, value):
        self._data[key] = validConvert(value, self._definition)

    def __setslice__(self, i, j, y):
        self._data.__setslice__(i, j, [validConvert(v, self._definition) for v in y])

    def append(self, value):
        self._data.append(validConvert(value, self._definition))

    def extend(self, value):
        self._data.extend([validConvert(v, self._definition) for v in value])

    def insert(self, index, object):
        self._data.insert(index, validConvert(object, self._definition))

    def __getattr__(self, attrib):
        # log.debug("__getattr__ called for %s" % attrib)
        return getattr(self._data, attrib)

