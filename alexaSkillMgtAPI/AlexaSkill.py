#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import re
import functools
from copy import copy

KWARGS_PAT = re.compile('\.{([a-z]+)}\.')

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

    # def __new__(self, S):
    #     return self._orig.__new__(S)

    #reduce
    #reduce ex

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
        """
        definition = {
            'keyname': type,
        }
        """
        self._definition = definition
        self._data = dict(*args, **kwargs)

    def __setitem__(self, key, value):
        self._data[key] = validConvert(value, self._definition.get(key))

    def setdefault(self, key, value=None):
        return self._data.setdefault(key, validConvert(value, self._definition.get(key)))

    def __getattr__(self, attrib):
        # print "__getattr__ called for %s" % attrib
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
        print "__getattr__ called for %s" % attrib
        return getattr(self._data, attrib)


class AlexaSkill(object):
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

    # _subdict = {
    #     'permissions': 'name',
    #     'eventSubscriptions': 'eventName',
    # }

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

    def __init__(self, AlexaSkillMmgtAPI, skillId, defaultLocale=None):
        self._api = AlexaSkillMmgtAPI
        self._id = skillId
        self._defaultLocale = defaultLocale
        self._loadData()
        self._populateClass()

    def _populateClass(self):
        class Dummy:
            def __init__(self, id):
                self.id = id

        for attrib, attribDef in self._structure.items():
            sub = KWARGS_PAT.findall(attribDef[1])
            if sub:
                targets = []
                sublcass = []
                for i in self._subclass[sub[0]]:
                    try:
                        sublcass.extend(self.get(i))
                    except:
                        pass

                for asub in set(sublcass):
                    if not hasattr(self, asub):
                        setattr(self, asub, Dummy(asub))
                    targets.append(
                        (getattr(self, asub), {sub[0]:asub})
                    )
            else:
                targets = [(self, {})]

            for target in targets:
                # if self.get(attrib, **target[1]):
                    funcs = [functools.partial(self.get, attrib, **target[1])]
                    if attribDef[0]:
                        funcs.append(functools.partial(self.set, attrib, **target[1]))
                    else:
                        funcs.append(None)
                    funcs.extend([None, 'parameter %s' % attrib])
                    setattr(target[0], attrib, property(*funcs))


    def _loadData(self):
        self._manifest = self._api.skillGet(self._id)

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
        value = self._iterPath(self._manifest, path)
        return value

    def get(self, param, **kwargs):
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
            hex(id(self)), self._id)





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



    # find a way for feed itmes:

    # "apis": {
    #   "flashBriefing": {
    #     "locales": {
    #       "en-US": {
    #         "customErrorMessage": "Error message",
    #         "feeds": [
    #           {
    #             "name": "feed name",
    #             "isDefault": true,
    #             "vuiPreamble": "In this skill",
    #             "updateFrequency": "HOURLY",
    #             "genre": "POLITICS",
    #             "imageUri": "https://fburi.com",
    #             "contentType": "TEXT",
    #             "url": "https://feeds.sampleskill.com/feedX"
    #           }
    #         ]
    #       }
    #     }
    #   }



class AlexaVideoSkill(AlexaSkill):
    _subdict = copy(AlexaSkill._subdict)
    _subdict['catalogInformation'] = ['sourceId', 'type']

    _structure = copy(AlexaSkill._structure)
    _structure['catalogInformation'] = (True, 'apis.video.locales.{locale}.catalogInformation', types.ListType)
    _structure['videoProviderTargetingNames'] = (True, 'apis.video.locales.{locale}.videoProviderTargetingNames', types.ListType)

    _structure['upchannelRegionUri'] = (True, 'apis.smartHome.endpoint.uri', types.StringType)
    _structure['upchannelRegionType'] = (True, 'apis.smartHome.endpoint.type', types.StringType)

if __name__ == '__main__':
    import sys
    from settings import Settings
    from AlexaSkillMgtAPI import AlexaSkillMgtAPI

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE [SKILLID]" % (sys.argv[0], )
        sys.exit(0)

    settings = Settings(sys.argv[1])
    api = AlexaSkillMgtAPI(settings.accessToken)

    if len(sys.argv) > 2:
        skillID = sys.argv[2]
    else:
        vendors = api.vendorList()
        vendorID = vendors.keys()[0]
        skills = api.skillList(vendorID)
        skillID = skills.values()[0]['skillId']

    skill = AlexaSkill(api, skillID)
    print "Skill: %s" % skill
    for value in ['manifestVersion', 'allowsPurchases', 'permissions']:
        print "Skill-%s: %s" % (value, skill.get(value))
    # print "Skill: %s" % dir(skill)
    # print "Skill.manifestVersion: %s" % skill.manifestVersion
    # print "Skill.manifestVersion: %s" % dir(skill.manifestVersion)
    class Test(object):
        val = {}

        class VarProxy(object):
                def __init__(self, data, key):
                    self._data = data
                    self._key = key

                def __set__(self, obj, val):
                    print "__set__ %s %s" % (obj, val)
                    # self._data[self._key] = val
                    obj.setval(self._key, val)

                def __get__(self, obj, objtype):
                    print "__get__ %s %s" % (obj, objtype)
                    # return self._data.get(self._key)
                    return obj.getval(self._key)

        def setval(self, param, value):
            print "setval: %s %s %s" % (self, param, value)
            self.val[param] = value

        def getval(self, param, arg2=None):
            print "getval self: %s param: %s arg2: %s" % (self, param, arg2)
            return self.val.get(param, '-')

        def delval(self, param):
            print "delval self: %s param: %s arg2: %s" % (self, param, arg2)
            del(self.val) #.get(param, '-')

        # def __setattr__(self, param, val):
        #     print "> setattr > %s" % param
        #     if param == 'test1':
        #         return functool.partial(self.setval, 'test1', val)
        #     else:
        #        raise AttributeError('%s.%s has no member %s' % (
        #         self.__class__.__module__, self.__class__.__name__, param))


        def __init__(self):
            pass

        test1 = VarProxy(val, 'test1')


    test = Test()
    print dir(test)
    print 'test.val ', test.val
    print 'test.test1 ', test.test1
    test.test1 = 'blub'
    # test.set_test1('foor')
    print 'test.test1 ', test.test1
    print 'test.val ', test.val
    # print 'test.bar ', test.bar
    # print 'test.bar ', test.bar
    # print 'test.bar ', test.bar




