#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import types
from copy import copy
from pprint import pformat

from utils import ListOverlay, RestrictedDict, RestrictedList
from AlexaInterface import AlexaInterface, AlexaInterfaceFactory

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())


class AlexaInteractionModel(AlexaInterface):

    _subdict = {
        'intents': {
            'name': types.StringType,
            'sample': types.ListType,
        },
    }
    _structure = {
        'invocationName': (True, 'invocationName', types.StringType),
        'intents': (True, 'intents', types.ListType),
    }
    # _subclass = {}

    def __init__(self, id, data=None, api=None):
        if not api or not data:
            raise Exception("You need to provide on of 'api' or 'data'.")

        self._api = api
        if data:
            self._data = data
        else:
            self._loadData()
        super(AlexaInteractionModel, self).__init__(id, self._data)

    def _loadData(self):
        if not self._api:
            log.error('Cannot read data - no api provided')
            return False

        manifest = self._api.modelGet(*self._id)
        self._data = manifest

def AlexaModelFactory(api, skillID, locale):
    id = (skillID, locale)
    baseClass = AlexaInteractionModel
    # try:
    model = api.modelGet(skillID, locale)
    return AlexaInterfaceFactory(baseClass, id, model, api=api)
    # except Exception, e :
    #     log.error("Could not load modell for language %s of skill %s" % (
    #         locale, skillID))


if __name__ == '__main__':
    import sys
    from settings import Settings
    from AlexaMgtAPI import AlexaMgtAPI
    from AlexaSkill import AlexaSkillFactory

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE [SKILLID] [LOCALE]" % (sys.argv[0], )
        sys.exit(0)

    settings = Settings(sys.argv[1])
    api = AlexaMgtAPI(settings.accessToken)

    if len(sys.argv) > 2:
        skillID = sys.argv[2]
    else:
        vendors = api.vendorList()
        vendorID = vendors.keys()[0]
        skills = api.skillList(vendorID)
        skillID = skills.values()[0]['skillId']

    skill = AlexaSkillFactory(api, skillID)

    if len(sys.argv) > 3:
        locale = sys.argv[3]
    else:
        locale = skill.locales[0]

    model = AlexaModelFactory(api, skillID, locale)
    print "Model: %s" % model
    print "Model: %s" % dir(model)




