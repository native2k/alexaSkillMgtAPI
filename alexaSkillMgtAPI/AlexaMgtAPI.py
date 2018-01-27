#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Summary
"""
import logging
import requests
from pprint import pformat
import time

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())

class AlexaMgtAPI(object):
    """Class to communicate with the Alexa Skill Management API

    Attributes:
        accessToken (TYPE): Description
    """
    _BASE_URL = 'https://api.amazonalexa.com/v0'
    _operations = {
        # SKill Operations
        'skillGet': {
            'url': _BASE_URL + '/skills/{skillId}',
            'method': 'GET',
        },
        'skillStatus': {
            'url': _BASE_URL + '/skills/{skillId}/status',
            'method': 'GET',
        },
        'skillCreate': {
            'url': _BASE_URL + '/skills',
            'method': 'POST',
        },
        'skillUpdate': {
            'url': _BASE_URL + '/skills/{skillId}',
            'method': 'PUT',
        },
        'skillListNext': {
            'url': _BASE_URL + '/skills?vendorId={vendorId}&maxResults={maxResults}&nextToken={token}',
            'method': 'GET',
        },
        'skillList': {
            'url': _BASE_URL + '/skills?vendorId={vendorId}&maxResults={maxResults}',
            'method': 'GET',
        },

        'skillDelete': {
            'url': _BASE_URL + '/skills/{skillId}/',
            'method': 'DELETE',
        },
        #  -----------------------------------------------------
        #  Vendor
        #  -----------------------------------------------------
        'vendorList': {
            'url': _BASE_URL + '/vendors',
            'method': 'GET',
        },
        #  -----------------------------------------------------
        # Interactions Model
        #  -----------------------------------------------------
        'modelGet': {
            'url': _BASE_URL + '/skills/{skillId}/interactionModel/locales/{locale}',
            'method': 'GET',
        },
        'modelGetTag': {
            'url': _BASE_URL + '/skills/{skillId}/interactionModel/locales/{locale}',
            'method': 'HEAD',
        },
        'modelUpdate': {
            'url': _BASE_URL + '/skills/{skillId}/interactionModel/locales/{locale}',
            'method': 'POST',
        },
        'modelStatus': {
            'url': _BASE_URL + '/skills/{skillId}/interactionModel/locales/{locale}/status',
            'method': 'GET',
        },
        #  -----------------------------------------------------
        # Account Linking
        #  -----------------------------------------------------
        'linkUpdate': {
            'url': _BASE_URL + '/skills/{skill_id}/accountLinkingClient',
            'method': 'PUT',
        },
        'linkInfo': {
            'url': _BASE_URL + '/skills/{skill_id}/accountLinkingClient',
            'method': 'GET',
        },
        #  -----------------------------------------------------
        #  Skill Invocations / Simulations
        #  -----------------------------------------------------
        'invocation': {
            'url': _BASE_URL + '/skills/{skillId}/invocations',
            'method': 'POST',
        },
        'simulation': {
            'url': _BASE_URL + '/skills/{skillId}/simulations',
            'method': 'POST',
        },
        'simulationResult': {
            'url': _BASE_URL + '/skills/{skillId}/simulations/{id}',
            'method': 'GET',
        },
    }
    _errorCodes = {
        400: 'Server cannot process the request due to a client error.',
        401: 'Unauthorized.',
        404: 'Not Found.',
        500: 'Internal Server Error.',
        202: 'Accepted',
        200: 'OK',
        204: 'NoContent',
        None: 'Unkown Error.',
    }
    _valid_locales = ['en-US', 'en-GB', 'en-IN', 'en-CA', 'de-DE']

    def __init__(self, accessToken):
        """Summary

        Attributes:
            accessToken (String): Amazon API access token

        Args:
            accessToken (String): Amazon API access token
        """

        self.accessToken = accessToken

    def _replace(self, aString, data):
        """Replaces placeholder in string.

        Args:
            aString (String): String with placeholder
            data (Dictionary): Data for replacement

        Returns:
            TYPE: String
        """
        for key, value in data.items():
            aString = aString.replace('{%s}' % (key, ), value)
        return aString

    def _getHeaders(self):
        """Returns Headers

        Returns:
            TYPE: Dictionary
        """
        return {
            'Authorization': self.accessToken
        }

    def _doRequest(self, operation, data=None, **kwargs):
        """Sends request to Amazon API

        Args:
            operation (String): Operation to send
            data (Dictionary, optional): request payload data
            **kwargs: request parameter like skill_id

        Returns:
            TYPE: Result Dictionary

        Raises:
            Exception: Description
        """
        op = self._operations.get(operation)
        if not op:
            raise Exception(
                'Unkown operation %s - must be one of %s' % (
                    operation, self._operations.keys()))

        url = self._replace(op['url'], kwargs)
        # log.debug("request: %s -> %s (%s)" % (url, data, self._getHeaders()))
        res = requests.request(
            method=op['method'],
            url=url,
            headers=self._getHeaders(),
            json=data
        )

        statusDesc = '%s: %s' % (
            res.status_code,
            self._errorCodes.get(res.status_code, self._errorCodes[None])
        )
        if res.status_code not in [200, 202, 204]:
            log.debug("%s - %s" % (statusDesc, res.text))
            try:
                msg = res.json().get('message') or res.text
            except Exception:
                msg = res.text
            if msg:
                statusDesc = '%s - %s' % (statusDesc, msg)

        result = {
            'status': res.status_code,
            'statusDesc': statusDesc,
            'headers': res.headers,
            'content': res.text,
            'json': res.text and res.json() or {},
        }
        return result

    def skillStatus(self, skillId):
        res = self._doRequest('skillStatus', skillId=skillId)
        if res['status'] == 200:
            return res['json']['manifest']
        else:
            raise Exception(res['statusDesc'])

    def skillGet(self, skillId):
        res = self._doRequest('skillGet', skillId=skillId)
        if res['status'] == 200:
            return res['json']['skillManifest']
        else:
            raise Exception(res['statusDesc'])

    def skillCreate(self, vendorId, manifest):
        res = self._doRequest('skillCreate', {
            'vendorId': vendorId,
            'skillManifest': manifest
        })
        if res['status'] == 202:
            return res['json']['skillId']
        else:
            raise Exception(res['statusDesc'])

    def skillUpdate(self, skillId, manifest):
        res = self._doRequest(
            'skillUpdate', {'skillManifest': manifest},
            skillId=skillId)
        if res['status'] == 202:
            return True
        else:
            raise Exception(res['statusDesc'])

    def skillDelete(self, skillId):
        res = self._doRequest('skillDelete', skillId=skillId)
        if res['status'] == 204:
            return True
        else:
            raise Exception(res['statusDesc'])

    def skillList(self, vendorId):
        res = self._doRequest('skillList', maxResults='50', vendorId=vendorId)

        if res['status'] == 200:
            results = {}
            for askill in res['json']['skills']:
                skillKey = "_".join([askill['skillId'], askill['stage']])
                if skillKey in results:
                    log.warning("Double skillid for: \n%s\n%s" % (results[skillKey], askill))
                results[skillKey] = askill
            # need to request more?
            # res = self._doRequest('skillListNext', maxResults='50', vendorId=vendorId, token=?)

            return results
        else:
            raise Exception(res['statusDesc'])

    def vendorList(self):
        res = self._doRequest('vendorList')
        if res['status'] == 200:
            return dict([
                (v['id'], v)
                for v in res['json']['vendors']
            ])
        else:
            raise Exception(res['statusDesc'])

    def modelGet(self, skillId, locale):
        res = self._doRequest('modelGet', skillId=skillId, locale=locale)
        # What is this etag for?
        # tag = self._doRequest('modelGetTag', skillId=skillId, locale=locale)
        # log.debug(pformat(tag))
        if res['status'] == 200:
            return res['json']['interactionModel']['languageModel']
        else:
            raise Exception(res['statusDesc'])

    def modelUpdate(self, skillId, locale, model):
        res = self._doRequest(
            'modelUpdate',
            {'interactionModel': {'languageModel': model}},
            # {'interactionModel': model},
            skillId=skillId, locale=locale)
        if res['status'] == 202:
            return True
        else:
            raise Exception(res['statusDesc'])

    def modelStatus(self, skillId, locale):
        res = self._doRequest('modelStatus', skillId=skillId, locale=locale)
        if res['status'] == 200:
            return res['json']['status']
        else:
            raise Exception(res['statusDesc'])

    def linkInfo(self, skillId):
        res = self._doRequest('linkInfo', skillId=skillId)
        if res['status'] == 200:
            return res['json']
        else:
            raise Exception(res['statusDesc'])

    # def invocation(self, skillId):
    #     res = self._doRequest('invocation', skillId=skillId)
    #     if res['status'] == 200:
    #         return res['json']
    #     else:
    #         raise Exception(res['statusDesc'])

    def _sleep(self, seconds):
        time.sleep(seconds)

    def simulation(self, skillId, locale, text):
        SIM_MAX = 20
        SIM_WAIT = 2

        res = self._doRequest(
            'simulation', {
                "input": {"content": text},
                "device": {"locale": locale},
            }, skillId=skillId)
        if res['status'] == 200:
            if res['json']['status'] == 'IN_PROGRESS':
                n = 0
                reqId = res['json']['id']
                while res['json']['status'] == 'IN_PROGRESS' and n < SIM_MAX:
                    n += 1
                    self._sleep(SIM_WAIT)
                    res = self._doRequest(
                        'simulationResult',
                        skillId=skillId, id=reqId)
            return res['json']
        else:
            raise Exception(res['statusDesc'])

    def __repr__(self):
        return '<%s.%s object at %s accessToken=%s>' % (
            self.__class__.__module__, self.__class__.__name__,
            hex(id(self)), self.accessToken)


if __name__ == '__main__':
    import sys
    from copy import copy
    from settings import Settings

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE [SKILLID]" % (sys.argv[0], )
        sys.exit(0)

    settings = Settings(sys.argv[1])
    api = AlexaMgtAPI(settings.accessToken)

    vendors = api.vendorList()
    print "Result vendorList: %s" % vendors
    vendorID = vendors.keys()[0]
    skills = api.skillList(vendorID)
    print "Result skillList: %s" % pformat(skills)
    # amzn1.ask.skill.57378e2b-c4a4-4949-b11d-38dd7f53f519
    if len(sys.argv) > 2:
        skillID = sys.argv[2]
    else:
        skillID = skills.values()[0]['skillId']
    # skillID = 'amzn1.ask.skill.57378e2b-c4a4-4949-b11d-38dd7f53f519'
    skill = api.skillGet(skillID)
    print "Result getSkill: %s" % pformat(skill)
    print "Result skillStatus: %s" % pformat(api.skillStatus(skillID))

    locale = 'de-DE'
    model = api.modelGet(skillID, locale)
    print "result modelGet: %s" % pformat(model)
    print "result modelStatus: %s" % pformat(api.modelStatus(skillID, locale))
    # print "result modelUpdate: %s" % pformat(api.modelUpdate(skillID, locale, model))
    # print "result modelStatus: %s" % pformat(api.modelStatus(skillID, locale))
    print "result simulation: %s" % pformat(api.simulation(skillID, locale, 'starten'))

    # # create emtpy skill as copy from retreived
    # newSkill = copy(skill)
    # pubInf = newSkill['publishingInformation']['locales']['de-DE']
    # pubInf['name'] = 'Testskill'
    # pubInf['description'] = 'Testskill for api develop'
    # del(pubInf['largeIconUri'])
    # del(pubInf['smallIconUri'])

    # newSkillID = api.skillCreate(vendorID, newSkill)
    # print "result skillCreate: %s" % newSkillID
    # print "result new skillStatus: %s" % pformat(api.skillStatus(newSkillID))
    # newSkill = api.skillGet(newSkillID)
    # print "result new skillGet: %s" % pformat(newSkill)
    # newSkill['publishingInformation']['locales']['de-DE']['name'] = "Testupdate"
    # print "Result updateSkill: %s" % pformat(api.skillUpdate(newSkillID, newSkill))
    # print "result new skillDelete: %s" % pformat(api.skillDelete(newSkillID))


