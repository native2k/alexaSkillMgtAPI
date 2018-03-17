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


def kwargsPermutations(data):
    """ build all permutations from data

    >>> kwargsPermutations({'a': [1, 2], 'b': [3]})
    [{'a': 1, 'b': 3}, {'a': 2, 'b': 3}]

    """
    results = []
    for key, items in data.items():
        if not results:
            for item in items:
                results.append({key: item})
        else:
            temp = []
            for result in results:
                print "results: %s - %s" % (results, result)
                result[key] = items[0]
                temp.append(result)
            for item in items[1:]:
                for res in temp:
                    cres = copy(res)
                    res[key] = item
                    results.append(cres)
    return results


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
    if isinstance(adef, types.ListType):
        if value not in adef:
            raise ValueError('Value "%s" must be one of %s' % (
                value, adef))
    elif isinstance(adef, types.StringType):
        if not isinstance(value, types.ListType):
            raise ValueError('Value "%s" must be a List' % (
                value, ))
    elif isinstance(adef, types.DictType):
        if not isinstance(value, types.DictType):
            raise ValueError('Value "%s" must be a Dictionary' % (
                value, ))
    elif not isinstance(value, adef):
        if adef == types.StringType and isinstance(value, types.IntType) and not isinstance(value, types.BooleanType):
            return str(value)   # exception for numeric value
        elif adef == types.BooleanType and value in [1, 0]:
            return bool(value)

        raise ValueError('Value "%s" is type %s but must be %s' % (
            value, type(value), adef))
    return value

class DictOverlay(dict):
    # class DictOverlayKeyIterator(Iterator):
    #     def __init__(self, n, reverse=False):
    #         self.i = 0
    #         self.reverse = reverse
    #         self.n = n._orig.keys()
    #         if self.reverse:
    #             self.i = len(self.n) - 1

    #     def __iter__(self):
    #         return self

    #     def next(self):
    #         if self.i < len(self.n) and self.i >= 0:
    #             i = self.n[self.i]
    #             if self.reverse:
    #                 self.i -= 1
    #             else:
    #                 self.i += 1
    #             return i
    #         else:
    #             raise StopIteration()


    class DictOverlayItemIterator():
        """docstring for DictOverlayItemIterator"""

        def __init__(self, n):
           self.n = n
           self.keyiter = n._orig.iterkeys()

        def __iter__(self):
            return self

        def next(self):
            key = self.keyiter.next()
            return (key, self.n[key])


    class DictOverlayValueIterator():
        """docstring for DictOverlayItemIterator"""

        def __init__(self, n):
           self.n
           self.keyiter = n._orig.iterkeys()


        def __iter__(self):
            return self

        def next(self):
            key = self.keyiter.next()
            return self.n[key]



    def __init__(self, definition, orig):
        self._definition = definition
        self._orig = orig

    def __eq__(self, y):
        if isinstance(y, DictOverlay):
            return y._orig == self._orig
        elif isinstance(y, types.DictType):
            nd = DictOverlay(self._definition, {})
            for k, v in y.items():
                nd[k] = v
            return nd._orig == self._orig
        else:
            return False

    def __iter__(self):
        return self.iterkeys()

    def __to_orig(self, v):
        result = point = {}
        deflist = self._definition.split('.')
        for k in deflist[:-1]:
            point[k] = {}
            point = point[k]
        point[deflist[-1]] = self.__doValidate(v)
        return result
        # return {self._definition: self.__doValidate(v)}

    def __from_orig(self, i):
        deflist = self._definition.split('.')
        point = i
        for k in deflist:
            point = point[k]
        return point

    def __doValidate(self, value):
        if self._allowedTypes is None:
            return value
        else:
            return validConvert(value, self._allowedTypes)

    def __getitem__(self, key):
        if key not in self._definition:
            return ValueError('Invalid key %s' % (key, ))
        # self.__from_orig(self._orig.__getitem__())
        # print "__getitem__: [%s] %s => %s" % (key, self._definition.get(key), self._orig.get(key))
        if isinstance(self._definition.get(key), types.StringType):
            return ListOverlay(self._definition[key], self._orig.__getitem__(key))
        elif isinstance(self._definition.get(key), types.DictType):
            return DictOverlay(self._definition[key], self._orig.__getitem__(key))
        else:
            return self._orig.__getitem__(key)

    def __setitem__(self, key, value):
        if key not in self._definition:
            return ValueError('Invalid element %s' % (key, ))

        if isinstance(self._definition.get(key), types.StringType):
            if not self._orig.get(key):
                self._orig[key] = []
            if isinstance(value, ListOverlay):
                self._orig[key] = value._orig
            elif isinstance(value, types.ListType):
                self._orig[key] = self._orig[key][:0]
                # print type(self[key])
                for val in value:
                    self[key].append(val)
                # print 'self[key]', self[key]
                # print '_orig[key]', self._orig[key]
            else:
                raise ValueError('Invalid type %s for element %s' % (type(value), key))
            # return ListOverlay(self._definition[key], self._orig.__getitem__(key))
        elif isinstance(self._definition.get(key), types.DictType):
            # return ListOverlay(self._definition[key], self._orig.__getitem__(key))
            if not self._orig.get(key):
                self._orig[key] = {}
            if isinstance(value, DictOverlay):
                self._orig[key] = value._orig
            elif isinstance(value, types.DictType):
                self._orig[key] = {}
                for k, v in value.items():
                    self[k] = v
            else:
                raise ValueError('Invalid type %s for element %s' % (type(value), key))
        else:
            self._orig[key] = validConvert(value, self._definition.get(key))

    def setdefault(self, key, value=None):
        return self._orig.setdefault(key, validConvert(value, self._definition.get(key)))

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return self.DictOverlayItemIterator(self)

    def iterkeys(self):
        return slef._orig.iterkeys()

    def keys(self):
        return self._orig.keys()

    def itervalues(self):
        return self.DictOverlayValueIterator(self)

    def values(self):
        return list[self.itervalues()]

    def values(self):
        return [self[k] for k in self._orig.keys()]

    def has_key(self, key):
        return key in self._orig

    def clear(self):
        return self._orig.clear()

    def copy(self):
        orig = self._orig.copy()
        definition = self._definition.copy()
        return DictOverlay(definition, orig)

    def get(self, key, default=None):
        if key in self._orig:
            return self[key]
        else:
            return default

    def pop(self, key):
        val = self[key]
        del(self[key])
        return  val

    def popitem(self, key):
        val = self.pop(key)
        return (key, val)

    def update(self, data):
        for k, v in data.items():
            if isinstance(v, types.DictType) and k in v:
                self[k].update(v)
            else:
                self[k] = v

    def __repr__(self):
        return '{%s}' % (', '.join(['%s: %s' % (k.__repr__(), v.__repr__()) for k, v in self.items()]))


class ListOverlay(list):

    class ListOverlayIterator():
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


    def __to_orig(self, v):
        result = point = {}
        deflist = self._definition.split('.')
        for k in deflist[:-1]:
            point[k] = {}
            point = point[k]
        point[deflist[-1]] = self.__doValidate(v)
        return result
        # return {self._definition: self.__doValidate(v)}

    def __from_orig(self, i):
        deflist = self._definition.split('.')
        point = i
        for k in deflist:
            point = point[k]
        return point

    def __init__(self, definition, orig, allowedTypes=None):
        self._definition = definition
        self._orig = orig
        self._allowedTypes = allowedTypes

    def __doValidate(self, value):
        if self._allowedTypes is None:
            return value
        else:
            return validConvert(value, self._allowedTypes)

    def __add__(self, y):
        res = self._orig.__add__([self.__to_orig(v) for v in y])
        return ListOverlay(self._definition, res, self._allowedTypes)

    def __contains__(self, y):
        return self._orig.__contains__(self.__to_orig(y))

    def __delitem__(self, y):
        self._orig.__delitem__(y)

    def __delslice__(self, i, j):
        self._orig.__delslice__(i, j)

    def __eq__(self, y):
        return self._orig.__eq__([self.__to_orig(v) for v in y])

    # format?
    def __ge__(self, y):
        return self._orig.__ge__([self.__to_orig(v) for v in y])

    def __getitem__(self, y):
        return self.__from_orig(self._orig.__getitem__(y))

    def __getslice__(self, i, y):
        return [self.__from_orig(n) for n in self._orig.__getslice__(i, j)]

    def __gt__(self, y):
        return self._orig.__gt__([self.__to_orig(v) for v in y])

    def __hash__(self):
        return self._orig.__hash__()

    def __iadd__(self, y):
        self._orig.__iadd__([self.__to_orig(v) for v in y])
        return self

    def __imul__(self, y):
        self._orig.__imul__([self.__to_orig(v) for v in y])
        return self

    def __ne__(self, y):
        return self._orig.__ne__([self.__to_orig(v) for v in y])

    def __iter__(self):
        return self.ListOverlayIterator(self)


    def __le__(self, y):
        return self._orig.__le__([self.__to_orig(v) for v in y])

    def __len__(self):
        return self._orig.__len__()

    def __lt__(self, y):
        return self._orig.__lt__([self.__to_orig(v) for v in y])

    def __mul__(self, y):
        res = self._orig.__mul__([self.__to_orig(v) for v in y])
        return ListOverlay(self._definition, res)

    def __ne__(self, y):
        return self._orig.__lt__([self.__to_orig(v) for v in y])

    def __repr__(self):
        return [self.__from_orig(v) for v in self._orig].__repr__()

    def __reversed__(self):
        return self.ListOverlayIterator(self, True)

    def __rmul__(self, n):
        return ListOverlay(self._definition, self._orig.__rmul__(n), self._allowedTypes)

    def __setitem__(self, i, y):
        self._orig.__setitem__(i, self.__to_orig(y))
        # self.__from_orig(self._orig[i]) = self._doValidate(y)

    def __setslice__(self, i, j, y):
        self._orig[i:j] = [self.__to_orig(n) for n in y]

    def __sizeof__(self):
        return self._orig.__sizeof__()

    def extend(self, iterable):
        for i in iterable:
            self.append(self._doValidate(i))

    def append(self, object):
        self._orig.append(self.__to_orig(object))

    def index(self, object):
        return self._orig.index(self.__to_orig(object))

    def insert(self, index, object):
        return self._orig.insert(index, self.__to_orig(object))

    def pop(self, index=-1):
        return self.__from_orig(self._orig.pop(index))

    def remove(self, value):
        return self._origi.remove(self.__to_orig(v))

    def reverse(self):
        self._orig.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        cmpNew = None
        if cmp is not None:
            def cmpNew(x, y):
                return cmp(self.__from_orig(x), self.__from_orig(y))

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

