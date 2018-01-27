#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_alexaModel
----------------------------------

Tests for `alexaModel` module.
"""
import pytest
import types
from pprint import pformat
from alexaSkillMgtAPI.AlexaModel import AlexaModelFactory

TESTDATA = [
    {u'intents': [{u'name': u'start', u'samples': [u'start']},
                  {u'name': u'AMAZON.StopIntent'},
                  {u'name': u'AMAZON.CancelIntent'},
                  {u'name': u'AMAZON.HelpIntent'},
                  {u'name': u'AMAZON.NoIntent'},
                  {u'name': u'AMAZON.YesIntent',
                   u'samples': [u'Ja', u'Jawohl', u'Richtig']},
                  {u'name': u'AMAZON.PreviousIntent',
                   u'samples': [u'Vorher', u'Vorheriges', u'Zur\xfcck']},
                  {u'name': u'AMAZON.NextIntent',
                   u'samples': [u'N\xe4chster',
                                u'N\xe4chstes',
                                u'Vor',
                                u'Weiter',
                                u'\xdcberspringen']},
                  {u'name': u'AMAZON.ScrollUpIntent'},
                  {u'name': u'AMAZON.ScrollLeftIntent'},
                  {u'name': u'AMAZON.ScrollDownIntent'},
                  {u'name': u'AMAZON.ScrollRightIntent'},
                  {u'name': u'AMAZON.PageUpIntent'},
                  {u'name': u'AMAZON.PageDownIntent'},
                  {u'name': u'AMAZON.MoreIntent'},
                  {u'name': u'AMAZON.NavigateSettingsIntent'}],
     u'invocationName': u'law blog'},
]




class TestAlexaSkill(object):


    """
        Test methods
    """
    @pytest.mark.parametrize('modelid, param, kwargs, exp', [

    })
    def test_getParam(self, skillId, param, kwargs, exp, api):
        print "SkillID: %s, param: %s, KWargs: %s -> expected: %s" % (
            skillId, param, kwargs, exp)
        skill = AlexaSKillFactory(api, skillId)
        res = skill.get(param, **kwargs)
        print "res: %s" % (res, )
        assert res == exp
        # assert skill.manifestVersion == "1.0"
        if kwargs:
            subobj = getattr(skill, ('%s_%s' % kwargs.items()[0]).replace('-', '_'))
            assert subobj
            assert getattr(subobj, param) == exp
        else:
            assert getattr(skill, param) == exp




