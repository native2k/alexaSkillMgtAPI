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

@pytest.fixture
def testdata():
    return [
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
    @pytest.mark.parametrize('modelid, param, exp', [
        (0, 'invocationName', 'law blog'),
    ])
    def test_getParam(self, modelid, param, exp, api):
        print "ModelID: %s, param: %s,  -> expected: %s" % (
            modelid, param, exp)
        model = AlexaModelFactory(api, modelid, 'de-DE')
        res = model.get(param)
        print "res: %s" % (res, )
        assert res == exp
        assert getattr(model, param) == exp




