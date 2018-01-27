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
from alexaSkillMgtAPI.utils import ListOverlay, RestrictedDict, RestrictedList, kwargsPermutations


@pytest.mark.parametrize('data,exp', [
    ({}, []),
    ({'a': [1]}, [{'a': 1}]),
    ({'a': [1, 2]}, [{'a': 1}, {'a': 2}]),
    ({'a': [1], 'b': [2]}, [{'a': 1, 'b': 2}]),
    ({'a': [1, 2], 'b': [3]}, [{'a': 1, 'b': 3}, {'a': 2, 'b': 3}]),
    ({'a': [1, 2], 'b': [3, 4]},  [
        {'a': 1, 'b': 3}, {'a': 2, 'b': 3},
        {'a': 1, 'b': 4}, {'a': 2, 'b': 4},
    ]),
    ({'a': [1, 2, 3], 'b': [4, 5, 6]}, [
        {'a': 1, 'b': 4}, {'a': 2, 'b': 4}, {'a': 3, 'b': 4},
        {'a': 1, 'b': 5}, {'a': 2, 'b': 5}, {'a': 3, 'b': 5},
        {'a': 1, 'b': 6}, {'a': 2, 'b': 6}, {'a': 3, 'b': 6},
    ]),
    ({'a': [1, 4], 'b': [2, 5], 'c': [3, 6]}, [
        {'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 2, 'c': 3},
        {'a': 1, 'b': 5, 'c': 3}, {'a': 4, 'b': 5, 'c': 3},
        {'a': 1, 'b': 2, 'c': 6}, {'a': 4, 'b': 2, 'c': 6},
        {'a': 1, 'b': 5, 'c': 6}, {'a': 4, 'b': 5, 'c': 6},
    ]),
])
def test_kwargsPermutations(data, exp):
    print "Input Data: %s " % pformat(data)
    print "Expected:   %s " % pformat(exp)
    res = kwargsPermutations(data)
    print "Result:     %s"  % pformat(res)
    assert sorted(res) == sorted(exp)


class TestListOverlay(object):
    def test_operations(self):
        akey = 'foo'
        alist = [{akey: 0}, {akey: 1}, {akey: 2}, {akey: 3}]
        aoverlay = ListOverlay(akey, alist)
        assert aoverlay[0] == 0
        assert aoverlay == [0,1,2,3]
        assert str(aoverlay) == "[0, 1, 2, 3]"

        aoverlay.append(4)
        assert alist[4] == {akey: 4}
        assert aoverlay[4] == 4

        aoverlay[4] = 'ab'
        assert alist[4] == {akey: 'ab'}
        assert 'ab' in aoverlay

        assert aoverlay.pop(0) == 0
        assert alist[0] == {akey: 1}
        assert aoverlay.pop() == 'ab'
        assert alist[-1] == {akey: 3}

        assert aoverlay == [1, 2, 3]

        iterres = [n for n in iter(aoverlay)]
        assert iterres == [1, 2, 3]

        iterres = [n for n in reversed(aoverlay)]
        assert iterres == [3, 2, 1]

        alist[1] = {akey: 1}
        assert aoverlay == [1, 1, 3]

        del(aoverlay[1])
        assert aoverlay == [1, 3]
        assert alist == [{akey: 1}, {akey: 3}]

        aoverlay[1:2] = [5,4]
        assert aoverlay == [1, 5, 4]
        assert alist == [{akey: 1}, {akey: 5}, {akey: 4}]


class TestRestrictedList(object):
    @pytest.mark.parametrize("args,opsuccess,opfail,expected", [
        ([types.BooleanType], [True, False], ['1', 3, 1.2], [True, False])
    ])
    def test_operations(self, args, opsuccess, opfail, expected):
        print "Args: %s" % args
        tlist = RestrictedList(*args)

        print "OpSuccess: %s" % (opsuccess, )
        for v in opsuccess:
            tlist.append(v)

        print "opFail: %s" % (opfail, )
        for v in opfail:
            with pytest.raises(Exception) as excinfo:
                tlsit.append = v

        print "Expected: %s Current: %s" % (expected, tlist)
        assert expected == tlist


    def test_methodsBool(self):
        tlist = RestrictedList(types.BooleanType, [True, False])
        assert tlist == [True, False]
        tlist.append(True)
        tlist[1] = True
        assert tlist.pop(0)
        print tlist
        assert tlist == [True, True]
        tlist[2:4] = [True, False, False, True]
        print tlist
        assert tlist == [True, True, True, False, False, True]
        tlist.insert(1, True)
        tlist.extend([True, False])

    def test_methodsBoolFail(self):
        tlist = RestrictedList(types.BooleanType, [True, False])
        assert tlist == [True, False]
        with pytest.raises(Exception) as excinfo:
            tlist.append('foo')
        with pytest.raises(Exception) as excinfo:
            tlist[1] = 'foo'
        with pytest.raises(Exception) as excinfo:
            tlist[2:4] = ['True', 'False', 'False', 'True']
        with pytest.raises(Exception) as excinfo:
            tlist.insert(1, 'True')
        with pytest.raises(Exception) as excinfo:
            tlist.extend(['True', 'False'])
        assert tlist == [True, False]


class TestRestrictedDict(object):
    def test_operations(self):
        tdict = RestrictedDict({
            'astring': types.StringType,
            'aint': types.IntType,
            'abool': types.BooleanType,
            'aenum': ['vala', 'valb'],
            })

        # check normal
        tdict['astring'] = 'sfsf'
        tdict['aint'] = 12
        tdict['abool'] = True
        tdict['aenum'] = 'valb'

        print tdict
        assert tdict == {
            'aint': 12, 'abool': True,
            'aenum': 'valb', 'astring': 'sfsf'
        }

        # check fail
        for key, values in {
            'astring': (1.23, True, False),
            'aint': ('blub', 1.34),
            'abool': ('ab', 4, 1.2),
            'aenum': (9, 1.2, True, 'blub'),
        }.items():
            for value in values:
                print "key: %s  << %s" % (key, pformat(value) )
                with pytest.raises(Exception) as excinfo:
                    tdict[key] = value

        # check convert
        for key, values in {
            'aint': [(True, 1), (False, 0)],
            'abool': [(1, True), (0, False)],
        }.items():
            for value, expected in values:
                print "key: %s << %s >> %s" % (key, pformat(value), pformat(expected) )
                tdict[key] = value
                assert tdict[key] == expected

        # check setdefault
        with pytest.raises(Exception) as excinfo:
            tdict.setdefault('abool', 'astring')
        tdict.setdefault('abool', True)

        # check adding invalid key
        with pytest.raises(Exception) as excinfo:
            tdict.setdefault('foo', 'astring')
        with pytest.raises(Exception) as excinfo:
            tdict['foo'] = 'astring'



