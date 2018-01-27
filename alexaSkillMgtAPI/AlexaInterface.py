#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import types
import re
from copy import copy
from pprint import pformat
from utils import ListOverlay, RestrictedDict, RestrictedList, Field, ParamField

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())

KWARGS_PAT = re.compile('\.{([a-z]+)}\.')



class AlexaInterface(object):

    _subdict = {
    }

    _structure = {
    }

    _subclass = {
    }

    def __init__(self, id, data=None):
        self._obj = self
        self._kwargs = {}
        self._id = id
        self._data = data or {}
        self._populateClass()

    def _populateClass(self):
        # build subclasses also
        for subclass, scmethods in self._subclass.items():
            targets = []
            for scmethod in scmethods:
                try:
                    targets.extend(self.get(scmethod))
                except:
                    pass
            for target in targets:
                self._createSubclass(subclass, target)

    def _nameSubclass(self, subclass, target):
        return '%s_%s' % (subclass, target.replace('-', '_'))

    def _createSubclass(self, subclass, target):
        setattr(
            self,
            self._nameSubclass(subclass, target),
            getattr(self, subclass)(self, **{subclass:target})
        )

    @classmethod
    def _replacePath(cls, path, data):
        needReplace = KWARGS_PAT.findall(path)
        if needReplace == data.keys():
            for key, value in data.items():
                path = path.replace('{%s}' % key, value)
            return path
        else:
            raise Exception('Need to provide %s but got %s instead.' % (needReplace, data.keys()))

    @classmethod
    def _iterPath(cls, data, path, forWrite=False):
        if forWrite and len(path) == 1:
            # in case of write we need to exit earlier
            return (data, path[0])
        elif path:
            currentKey = path.pop(0)
            if isinstance(data, types.DictType) and currentKey in data:
                return cls._iterPath(data[currentKey], path)
            elif isinstance(data, types.DictType) and forWrite in data:
                data[currentKey] = {}
                return cls._iterPath(data[currentKey], path)
            else:
                raise ValueError('Unable to find value for "%s".' % currentKey)
        else:
            return data

    def _doIterPath(self, paramDef, forWrite, **kwargs):
        if not paramDef:
            raise Exception('Unable to find definition for "%s" must be one of %s' % (
                param, self._structure.keys()
                ))
        path = self._replacePath(paramDef[1], kwargs).split('.')
        value = self._iterPath(self._data, path)
        return value

    def get(self, param, **kwargs):
        log.debug("get(%s, %s)" % (param, kwargs))
        paramDef = self._structure.get(param)
        value = self._doIterPath(paramDef, False, **kwargs)

        if param in self._subdict:
            subdictDef = self._subdict[param]
            if isinstance(subdictDef, types.DictType):
                if len(subdictDef) == 1:
                    subkey, restriction = subdictDef.items()[0]
                    return ListOverlay(subkey, value, restriction)

                elif isinstance(subdictDef, types.ListType):
                    res = []
                    for val in value:
                        res.append(RestrictedDict(subdictDef, value))
                    return res
            elif isinstance(subdictDef, types.ListType):
                # is an enum .. we can do not much
                pass
            else:
                raise Exception('Invalid definition type "%s" for %s' % (type(subdictDef, param)))
        elif isinstance(paramDef[2], types.StringType):
            return getattr(value, paramDef[2])()
        return value

    def set(self, param, value, **kwargs):
        log.debug("get(%s, %s, %s)" % (param, value, kwargs))
        paramDef = self._structure.get(param)

        # do some checks first
        if paramDef[0] is False:
            raise Exception('Param "%s" is not writeable.' % (param, ))
        if not isinstance(value, paramDef):
            raise Exception('Invalid type "%s" for param %s - expected %s' % (
                type(value), param, paramDef[2]
                ))
        subdictDef = self._subdict.get(param)
        if subdictDef and isinstance(subdictDef, types.ListType) and value not in subdictDef:
            raise Exception('Param "%s" invalid value "%s" expect one of: %s' % (
                parm, value, subdictDef
                ))

        # build the subclass if necessary
        if kwargs:
            scname = self._nameSubclass(*kwargs.items()[0])
            if not hasattr(self, scname):
                self._createSubclass(*kwargs.items()[0  ])

        # resolve value
        data, key = value = self._doIterPath(param, True, **kwargs)
        if paramDef[0] in [types.BooleanType, types.StringType, types.IntType]:
            data[key] = value
        elif paramDef[0] in [types.ListType]:
            if isinstance(subdictDef, types.DictType) and len(subdictDef) == 1:
                if isinstance(value, ListOverlay):
                    data[key] = value._orig
                else:
                    akey = self._subdict[param]
                    data[key] = [{akey: v} for v in values]
            else:
                data[key] = value

    def __repr__(self):
        return '<%s.%s object at %s id=%s>' % (
            self.__class__.__module__, self.__class__.__name__,
            hex(id(self)), pformat(self._id))


def AlexaInterfaceFactory(baseClass, id, data, **kwargs):
    # add attributes
    for key, attribDef in baseClass._structure.items():
        sub = KWARGS_PAT.findall(attribDef[1])
        if len(sub) == 1:
            # arguments with placeholders
            subclass = sub[0]
            if not hasattr(baseClass, subclass):
                setattr(baseClass, subclass, ParamField)
            setattr(getattr(baseClass, subclass), key, Field(key))
        elif len(sub) > 1:
            # if necessary need to implement this
            raise Exception('Unable to handle "%s" more han one subkey: %s' % (sub, ))
        else:
            # the normal attribs without parameter
            setattr(baseClass, key, Field(key))

    return baseClass(id=id, data=data, **kwargs)

