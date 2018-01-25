#!/usr/bin/env python
# -*- coding: utf-8 -*-



def AlexaSkill(object):
    """
{u'skillManifest': {u'apis': {u'custom': {u'endpoint': {u'sslCertificateType': u'Wildcard',
                                                        u'uri': u'https://rl7pobxxp1.execute-api.eu-west-1.amazonaws.com/fefe_v1'},
                                          u'interfaces': [{u'type': u'RENDER_TEMPLATE'}]}},
                    u'manifestVersion': u'1.0',
                    u'permissions': [],
                    u'privacyAndCompliance': {u'allowsPurchases': False,
                                              u'containsAds': False,
                                              u'isChildDirected': False,
                                              u'isExportCompliant': True,
                                              u'usesPersonalInfo': False},
                    u'publishingInformation': {u'category': u'NEWS',
                                               u'distributionCountries': [],
                                               u'isAvailableWorldwide': True,
                                               u'locales': {u'de-DE': {u'description': u'Mit diesem Skill k\xf6nnt ihr euch in aller Ruhe zur\xfccklehnen und euch die aktuellen Verschw\xf6rungstheorien von Felix von Leitner bequem von Alexa vorlesen lassen.\n\nWenn ihr einen Beitrag \xfcberspringen  wollt sagt einfach "weiter" oder "stop" um das Vortragen zu beenden.\n\n\n\nUpdate:\n - Nun auch mit Unterst\xfctzung fuer Echo Show',
                                                                       u'examplePhrases': [u'Alexa, starte Fefes Blog'],
                                                                       u'keywords': [u'fefe',
                                                                                     u'blog',
                                                                                     u'Verschw\xf6rungstheorien',
                                                                                     u'nerd'],
                                                                       u'largeIconUri': u'https://api.amazonalexa.com/v0/skills/amzn1.ask.skill.dc08640f-eeab-45d5-84b7-4c5bb7e10101/images/eyJkIjoiQlRlNktNRHREOCtFOTljUXdOV3diZUE3S1pqZ2RFd3BlSk5KRmpIVFB3R0o0aUl3a1hSU2NFWmJ0S0Y2M3Y2dG9VSEZTMU82TXJ1MTMydHJPci9zUFFVNXFNc0tlR0xzRjhrVWN1REVGU3ZnVEhoN25KWTY5cVh6QzJPT2NaN21WRGo3Q1FXVWNaWjdKSnJSZE4rWmZRPT0iLCJpdiI6Ill3Sm1RNU5jMFJIYU5tOEQ0WlF5ZGc9PSIsInYiOjF9',
                                                                       u'name': u'Fefes Blog (inoffiziell)',
                                                                       u'smallIconUri': u'https://api.amazonalexa.com/v0/skills/amzn1.ask.skill.dc08640f-eeab-45d5-84b7-4c5bb7e10101/images/eyJkIjoicmNDVmZsOWpiWVVmb2FvcGl0MVVYQU4wb2hXTWtldWFqY29MZmc2TExIQ0wwZ3VTZDMzRGhFM0dBVHBkaWR6dzBYS2oraStsOVMwWVMyUC9wRmtlZFVaWEFuOFJ4bE02bEtUUW4wbDJ6UVlqeEpCWFhUTjNXUGNNNjlHbk9LQTIiLCJpdiI6IjYzVDlUZitmWUVFOEQycHdndXJkVlE9PSIsInYiOjF9',
                                                                       u'summary': u'Liest die aktuellen Beitr\xe4ge von blog.fefe.de vor.'}},
                                               u'testingInstructions': u'just start the skill and enjoy.'}}}
    """
    _valid_locales = ['de-DE', 'en-US']
    _valid_interfaces = ['RENDER_TEMPLATE']

    def __init__(self, AlexaSkillMmgtAPI, skillId):
        self._api = AlexaSkillMmgtAPI
        self._id = skillId
        self._manifest = self._api.skill(self._id)

    def __repr__(self):
        return '<%s.%s object at %s id=%s>' % (
            self.__class__.__module__, self.__class__.__name__,
            hex(id(self)), self._id)

    def manifestVersion(self):
