#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_alexaSkill
----------------------------------

Tests for `alexaSkill` module.
"""
import pytest
import types
from pprint import pformat
from alexaSkillMgtAPI.AlexaInterface import AlexaInterface


class TestAlexaInterface(object):

    """
         Test class mehthods

    """
    @pytest.mark.parametrize('path,rdict,exp', [
        ('ab.{bc}.de', {'bc': 'ef'}, 'ab.ef.de'),
        ('ab.de', {}, 'ab.de'),
        ('ab.{bc}.de.{bc}.nf', {'bc': 'ef'}, 'ab.ef.de.ef.nf'),
        ('ab.{bc}.de.{ac}.nf', {'bc': 'ef', 'ac': 'nb'}, 'ab.ef.de.nb.nf'),
    ])
    def test_replacePath(self, path, rdict, exp):
        print "Path: %s, ReqDict: %s, Expected: %s" % (path, rdict, exp)
        res = AlexaInterface._replacePath('ab.{bc}.de', {'bc': 'ef'})
        assert res == 'ab.ef.de'

    @pytest.mark.parametrize('path,rdict,exp', [
        ('ab.de', {'bc': 'ef'}, "Need to provide [] but got ['bc'] instead."),
        ('ab.{cd}.de', {}, "Need to provide ['cd'] but got [] instead."),
        ('ab.{cd}.de', {'cd': 'ef', 'ab': 'ne'}, "Need to provide ['cd'] but got ['ab', 'cd'] instead."),
    ])
    def test_replacePathExc(self, path, rdict, exp):
        print "Path: %s, ReqDict: %s, Expected: %s" % (path, rdict, exp)
        with pytest.raises(Exception) as excinfo:
            res = AlexaInterface._replacePath(path, rdict)
        assert exp in excinfo.value

    @pytest.mark.parametrize('path,data,exp', [
        ('ab', {'ab': 1}, 1),
        ('ab.cd.ef', {'ab': {'cd': {'ef': 2}}}, 2),
        ('ab.cd', {'ab': {'cd': {'ef': 3}}}, {'ef': 3}),
    ])
    def test_iterPath(self, path, data, exp):
        print "Path: %s, data: %s, Expected: %s" % (path, data, exp)
        res = AlexaInterface._iterPath(data, path.split('.'))
        assert res == exp

    @pytest.mark.parametrize('path,data,exp', [
        ('ab.de', {'ab': 1}, 'Unable to find value for "de".'),
        ('ab.gf.ef', {'ab': {'cd': {'ef': 2}}}, 'Unable to find value for "gf".'),
    ])
    def test_iterPathExc(self, path, data, exp):
        print "Path: %s, data: %s, Expected: %s" % (path, data, exp)
        with pytest.raises(Exception) as excinfo:
            res = AlexaInterface._iterPath(data, path.split('.'))
        print excinfo.value
        assert exp in excinfo.value
