#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import types
import re
from copy import copy
from pprint import pformat

from utils import ListOverlay, RestrictedDict, RestrictedList, Field, ParamField
from AlexaInterface import AlexaInterface, AlexaInterfaceFactory

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())

KWARGS_PAT = re.compile('\.{([a-z]+)}\.')


class AlexaSkill(AlexaInterface):
    """
    """
    _subdict = {
        'category': [
            'ALARMS_AND_CLOCKS', 'ASTROLOGY', 'BUSINESS_AND_FINANCE', 'CALCULATORS', 'CALENDARS_AND_REMINDERS',
            'CHILDRENS_EDUCATION_AND_REFERENCE', 'CHILDRENS_GAMES', 'CHILDRENS_MUSIC_AND_AUDIO',
            'CHILDRENS_NOVELTY_AND_HUMOR', 'COMMUNICATION', 'CONNECTED_CAR', 'COOKING_AND_RECIPE',
            'CURRENCY_GUIDES_AND_CONVERTERS', 'DATING', 'DELIVERY_AND_TAKEOUT', 'DEVICE_TRACKING',
            'EDUCATION_AND_REFERENCE', 'EVENT_FINDERS', 'EXERCISE_AND_WORKOUT', 'FASHION_AND_STYLE', 'FLIGHT_FINDERS',
            'FRIENDS_AND_FAMILY', 'GAME_INFO_AND_ACCESSORY', 'GAMES', 'HEALTH_AND_FITNESS', 'HOTEL_FINDERS',
            'KNOWLEDGE_AND_TRIVIA', 'MOVIE_AND_TV_KNOWLEDGE_AND_TRIVIA', 'MOVIE_INFO_AND_REVIEWS', 'MOVIE_SHOWTIMES',
            'MUSIC_AND_AUDIO_ACCESSORIES', 'MUSIC_AND_AUDIO_KNOWLEDGE_AND_TRIVIA',
            'MUSIC_INFO_REVIEWS_AND_RECOGNITION_SERVICE', 'NAVIGATION_AND_TRIP_PLANNER', 'NEWS', 'NOVELTY',
            'ORGANIZERS_AND_ASSISTANTS', 'PETS_AND_ANIMAL', 'PODCAST', 'PUBLIC_TRANSPORTATION',
            'RELIGION_AND_SPIRITUALITY', 'RESTAURANT_BOOKING_INFO_AND_REVIEW', 'SCHOOLS', 'SCORE_KEEPING',
            'SELF_IMPROVEMENT', 'SHOPPING', 'SMART_HOME', 'SOCIAL_NETWORKING', 'SPORTS_GAMES', 'SPORTS_NEWS',
            'STREAMING_SERVICE', 'TAXI_AND_RIDESHARING', 'TO_DO_LISTS_AND_NOTES', 'TRANSLATORS', 'TV_GUIDES',
            'UNIT_CONVERTERS', 'WEATHER', 'WINE_AND_BEVERAGE', 'ZIP_CODE_LOOKUP',
        ],
        'interfaces': [
            'AUDIO_PLAYER', 'VIDEO_APP', 'RENDER_TEMPLATE',
        ],
        'eventSubscriptions': {
            'eventName': [
                "SKILL_ENABLED", "SKILL_DISABLED",
                "SKILL_PERMISSION_ACCEPTED", "SKILL_PERMISSION_CHANGED",
                "SKILL_ACCOUNT_LINKED",
                "ITEMS_CREATED", "ITEMS_UPDATED","ITEMS_DELETED",
            ],
        },
        'permissions': {
            'name': [
                "alexa::devices:all:address:full:read",
                "alexa:devices:all:address:country_and_postal_code:read",
                "alexa::household:lists:read",
                "alexa::household:lists:write",
            ],
        },
    }

    _structure = {
        # publishing information
        'locales': (False, 'publishingInformation.locales', 'keys'),
        'summary': (True, 'publishingInformation.locales.{locale}.summary', types.StringType),
        'examplePhrases': (True, 'publishingInformation.locales.{locale}.examplePhrases', types.ListType),
        'keywords': (True, 'publishingInformation.locales.{locale}.keywords', types.ListType),
        'name': (True, 'publishingInformation.locales.{locale}.name', types.StringType),
        'smallIconUri': (True, 'publishingInformation.locales.{locale}.smallIconUri', types.StringType),
        'largeIconUri': (True, 'publishingInformation.locales.{locale}.largeIconUri', types.StringType),
        'description': (True, 'publishingInformation.locales.{locale}.description', types.StringType),

        'isAvailableWorldwide': (True, 'publishingInformation.isAvailableWorldwide', types.BooleanType),
        'testingInstructions': (True, 'publishingInformation.testingInstructions', types.StringType),
        'category': (True, 'publishingInformation.category', types.StringType),
        'distributionCountries': (True, 'publishingInformation.distributionCountries', types.ListType),

        # apis
        'endpointUri': (True, 'apis.custom.endpoint.uri', types.StringType),
        # 'endpointCertType': (True, 'apis.custom.endpoint.sslCertificateType', types.StringType),
        'interfaces': (True, 'apis.custom.interfaces', types.ListType),
        'endpointRegions': (False, 'apis.custom.regions', 'keys'),
        'endpointRegionUri': (True, 'apis.custom.regions.{region}.endpoint.uri', types.StringType),
        'endpointRegionCertType': (True, 'apis.custom.regions.{region}.endpoint.sslCertificateType', types.StringType),

        # base
        'manifestVersion': (False, 'manifestVersion', types.StringType),
        "permissions": (True, 'permissions', types.ListType), # dict with naem .. lets see

        # privacy
        'allowsPurchases': (True, 'privacyAndCompliance.allowsPurchases', types.BooleanType),
        'usesPersonalInfo': (True, 'privacyAndCompliance.usesPersonalInfo', types.BooleanType),
        'isChildDirected': (True, 'privacyAndCompliance.isChildDirected', types.BooleanType),
        'isExportCompliant': (True, 'privacyAndCompliance.isExportCompliant', types.BooleanType),
        'containsAds': (True, 'privacyAndCompliance.containsAds', types.BooleanType),
        'privacyPolicyUrl': (True, 'privacyAndCompliance.locales.{locale}.privacyPolicyUrl', types.StringType),
        'termsOfUseUrl': (True, 'privacyAndCompliance.locales.{locale}.termsOfUseUrl', types.StringType),

        # events
        'eventUri': (True, 'events.endpoint.uri', types.StringType),
        'eventSubscriptions': (True, 'events.subscriptions', types.ListType),
        'eventRegions': (False, 'events.regions', 'keys'),
        'eventRegionUri': (True, 'events.regions.{region}.endpoint.uri', types.StringType),
    }
    _subclass = {
        'locale': ['locales'],
        'region': ['endpointRegions', 'eventRegions'],
    }

    def __init__(self, id, data=None, api=None, defaultLocale=None):
        if not api or not data:
            raise Exception("You need to provide on of 'api' or 'data'.")

        self._model = {}
        self._api = api
        self._defaultLocale = defaultLocale
        if data:
            self._data = data
        else:
            self._loadData(data)
        super(AlexaSkill, self).__init__(id, self._data)


    def _loadData(self):
        if not self._api:
            log.error('Cannot read data - no api provided')
            return False

        manifest = self._api.skillGet(self._id)
        self._data = manifest
        for locale in self.get('locales'):
            model = AlexaInteractionModelFactory(self._api, self._id, locale)
            if model:
                self._model[locale] = model
            else:
                log.warning("Could not load modell for language %s" % (locale))


    def __repr__(self):
        return '<%s.%s object at %s id=%s models=%s>' % (
            self.__class__.__module__, self.__class__.__name__,
            hex(id(self)), pformat(self._id), self._model.keys())


class AlexaSmartHomeSkill(AlexaSkill):

    _structure = copy(AlexaSkill._structure)
    _structure['endpointUri'] = (True, 'apis.smartHome.endpoint.uri', types.StringType)
    _structure['endpointCertType'] = (True, 'apis.smartHome.endpoint.sslCertificateType', types.StringType)

    _structure['endpointRegionUri'] = (True, 'apis.smartHome.regions.{region}.endpoint.uri', types.StringType)
    _structure['endpointRegionCertType'] = (True, 'apis.smartHome.regions.{region}.endpoint.sslCertificateType', types.StringType)


class AlexaListSkill(AlexaSkill):

    _structure = copy(AlexaSkill._structure)
    _structure['householdList'] = (True, 'apis.householdList', types.DictType)

class AlexaFlashBriefingSkill(AlexaSkill):

    _structure = copy(AlexaSkill._structure)
    _structure['feed'] = (True, 'apis.flashBriefing.locales.{locale}.feeds', types.ListType)
    _structure['errorMessage'] = (True, 'apis.flashBriefing.locales.{locale}.customErrorMessage', types.StringType)

    _subdict = copy(AlexaSkill._subdict)
    _subdict['feed'] = {
        'updateFrequency': ['DAILY', 'HOURLY', 'WEEKLY'],
        'genre': [
            'HEADLINE_NEWS', 'BUSINESS', 'POLITICS', 'ENTERTAINMENT', 'TECHNOLOGY', 'HUMOR', 'LIFESTYLE', 'SPORTS',
            'SCIENCE', 'HEALTH_AND_FITNESS', 'ARTS_AND_CULTURE', 'PRODUCTIVITY_AND_UTILITIES', 'OTHER',
        ],
        'contentType': ['TEXT', 'AUDIO'],
        'name': types.StringType,
        'isDefault': types.BooleanType,
        'vuiPreample': types.StringType,
        'imageUri': types.StringType,
        'url': types.StringType,
    }

class AlexaVideoSkill(AlexaSkill):

    _subdict = copy(AlexaSkill._subdict)
    _subdict['catalogInformation'] = {
        'sourceId': types.StringType,
        'type': ['FIRE_TV'],
    }
    _structure = copy(AlexaSkill._structure)
    _structure['catalogInformation'] = (True, 'apis.video.locales.{locale}.catalogInformation', types.ListType)
    _structure['videoProviderTargetingNames'] = (True, 'apis.video.locales.{locale}.videoProviderTargetingNames', types.ListType)

    _structure['videoEndpointUri'] = (True, 'apis.video.endpoint.uri', types.ListType)
    _structure['videoEndpointRegionUri'] = (True, 'apis.video.regions.{region}.endpoint.uri', types.StringType)

    _structure['upchannelRegionUri'] = (True, 'apis.video.regions.{region}.upchannel.uri', types.StringType)
    _structure['upchannelRegionType'] = (True, 'apis.video.regions.{region}.upchannel.type', types.StringType)


def AlexaSkillFactory(api, skillID):
    #  detect correct class
    manifest = api.skillGet(skillID)
    if manifest.get('apis', {}).get('smartHome'):
        baseClass = AlexaSmartHomeSkill
    elif manifest.get('apis', {}).get('householdList'):
        baseClass = AlexaListSkill
    elif manifest.get('apis', {}).get('flashBriefing'):
        baseClass = AlexaFlashBriefingSkill
    elif manifest.get('apis', {}).get('video'):
        baseClass = AlexaVideoSkill
    else:
        baseClass = AlexaSkill

    return AlexaInterfaceFactory(baseClass, skillID, manifest, api=api)


if __name__ == '__main__':
    import sys
    from settings import Settings
    from AlexaMgtAPI import AlexaMgtAPI

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE [SKILLID]" % (sys.argv[0], )
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
    print "Skill: %s" % skill
    for value in ['manifestVersion', 'allowsPurchases', 'permissions']:
        print "Skill-%s: %s" % (value, skill.get(value))
    print "Skill: %s" % dir(skill)
    print "Skill.manifestVersion: %s" % skill.manifestVersion
    # print "Skill.manifestVersion: %s" % dir(skill.manifestVersion)
    print "Skill.locale_de_DE: %s" % dir(skill.locale_de_DE)
    print "Skill.locale_de_DE.name: %s" % skill.locale_de_DE.name
    print "Skill._model['de-DE']: %s" % pformat(skill._model.get('de-DE'))

