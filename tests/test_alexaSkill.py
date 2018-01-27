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
from alexaSkillMgtAPI.AlexaSkill import AlexaSkillFactory


@pytest.fixture
def testdata():
    return [{
          "skillManifest": {
            "publishingInformation": {
              "locales": {
                "en-US": {
                  "summary": "This is a sample Alexa custom skill.",
                  "examplePhrases": [
                    "Alexa, open sample custom skill.",
                    "Alexa, play sample custom skill."
                  ],
                  "keywords": [
                    "Descriptive_Phrase_1",
                    "Descriptive_Phrase_2",
                    "Descriptive_Phrase_3"
                  ],
                  "smallIconUri": "https://smallUri.com",
                  "largeIconUri": "https://largeUri.com",
                  "name": "Sample custom skill name.",
                  "description": "This skill does interesting things."
                }
              },
              "isAvailableWorldwide": False,
              "testingInstructions": "1) Say 'Alexa, hello world'",
              "category": "HEALTH_AND_FITNESS",
              "distributionCountries": [
                "US",
                "GB",
                "DE"
              ]
            },
            "apis": {
              "custom": {
                "endpoint": {
                  "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
                },
                "regions": {
                  "NA": {
                    "endpoint": {
                      "sslCertificateType": "Trusted",
                      "uri": "https://customapi.sampleskill.com"
                    }
                  }
                }
              }
            },
            "manifestVersion": "1.0",
            "permissions": [
              {
                "name": "alexa::devices:all:address:full:read"
              },
              {
                "name": "alexa:devices:all:address:country_and_postal_code:read"
              },
              {
                "name": "alexa::household:lists:read"
              },
              {
                "name": "alexa::household:lists:write"
              }
            ],
            "privacyAndCompliance": {
              "allowsPurchases": False,
              "usesPersonalInfo": False,
              "isChildDirected": False,
              "isExportCompliant": True,
              "containsAds": False,
              "locales": {
                "en-US": {
                  "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com",
                  "termsOfUseUrl": "http://www.termsofuse.sampleskill.com"
                }
              }
            },
            "events": {
              "endpoint": {
                "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
              },
              "subscriptions": [
                {
                  "eventName": "SKILL_ENABLED"
                },
                {
                  "eventName": "SKILL_DISABLED"
                },
                {
                  "eventName": "SKILL_PERMISSION_ACCEPTED"
                },
                {
                  "eventName": "SKILL_PERMISSION_CHANGED"
                },
                {
                  "eventName": "SKILL_ACCOUNT_LINKED"
                }
              ],
              "regions": {
                "NA": {
                  "endpoint": {
                    "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
                  }
                }
              }
            }
          }
        },


        # # smarthome
        # {
        #   "skillManifest": {
        #     "manifestVersion": "1.0",
        #     "publishingInformation": {
        #       "locales": {
        #         "en-US": {
        #           "name": "Sample skill name.",
        #           "summary": "This is a sample Alexa skill.",
        #           "description": "This skill has basic and advanced smart devices control features.",
        #           "smallIconUri": "https://smallUri.com",
        #           "largeIconUri": "https://largeUri.com",
        #           "examplePhrases": [
        #             "Alexa, open sample skill.",
        #             "Alexa, blink kitchen lights."
        #           ],
        #           "keywords": [
        #             "Smart Home",
        #             "Lights",
        #             "Smart Devices"
        #           ]
        #         }
        #       },
        #       "distributionCountries": [
        #         "US",
        #         "GB",
        #         "DE"
        #       ],
        #       "isAvailableWorldwide": False,
        #       "testingInstructions": "1) Say 'Alexa, turn on sample lights'",
        #       "category": "SMART_HOME"
        #     },
        #     "privacyAndCompliance": {
        #       "allowsPurchases": False,
        #       "usesPersonalInfo": False,
        #       "isChildDirected": False,
        #       "isExportCompliant": True,
        #       "containsAds": False,
        #       "locales": {
        #         "en-US": {
        #           "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com",
        #           "termsOfUseUrl": "http://www.termsofuse.sampleskill.com"
        #         }
        #       }
        #     },
        #     "apis": {
        #       "smartHome": {
        #         "endpoint": {
        #           "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #         },
        #         "regions": {
        #           "NA": {
        #             "endpoint": {
        #               "uri": "arn:aws:lambda:us-west-2:010623927470:function:sampleSkillWest"
        #             }
        #           }
        #         }
        #       }
        #     }
        #   }
        # },

        # #List Skill Manifest With Custom Component
        # {
        #   "skillManifest": {
        #     "publishingInformation": {
        #       "locales": {
        #         "en-US": {
        #           "summary": "This is a sample Alexa skill.",
        #           "examplePhrases": [
        #             "Alexa, open sample skill.",
        #             "Alexa, play sample skill."
        #           ],
        #           "keywords": [
        #             "Descriptive_Phrase_1",
        #             "Descriptive_Phrase_2",
        #             "Descriptive_Phrase_3"
        #           ],
        #           "smallIconUri": "https://smallUri.com",
        #           "largeIconUri": "https://largeUri.com",
        #           "name": "Sample skill name.",
        #           "description": "This skill does interesting things."
        #         }
        #       },
        #       "isAvailableWorldwide": False,
        #       "testingInstructions": "1) Say 'Alexa, hello world'",
        #       "category": "HEALTH_AND_FITNESS",
        #       "distributionCountries": [
        #         "US",
        #         "GB",
        #         "DE"
        #       ]
        #     },
        #     "apis": {
        #       "custom": {
        #         "endpoint": {
        #           "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #         },
        #         "regions": {
        #           "NA": {
        #             "endpoint": {
        #               "sslCertificateType": "Trusted",
        #               "uri": "https://customapi.sampleskill.com"
        #             }
        #           }
        #         }
        #       },
        #       "householdList": {}
        #     },
        #     "manifestVersion": "1.0",
        #     "permissions": [
        #       {
        #         "name": "alexa::devices:all:address:full:read"
        #       },
        #       {
        #         "name": "alexa:devices:all:address:country_and_postal_code:read"
        #       },
        #       {
        #         "name": "alexa::household:lists:read"
        #       },
        #       {
        #         "name": "alexa::household:lists:write"
        #       }
        #     ],
        #     "privacyAndCompliance": {
        #       "allowsPurchases": False,
        #       "locales": {
        #         "en-US": {
        #           "termsOfUseUrl": "http://www.termsofuse.sampleskill.com",
        #           "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com"
        #         }
        #       },
        #       "isExportCompliant": True,
        #       "containsAds": False,
        #       "isChildDirected": False,
        #       "usesPersonalInfo": False
        #     },
        #     "events": {
        #       "endpoint": {
        #         "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #       },
        #       "subscriptions": [
        #         {
        #           "eventName": "SKILL_ENABLED"
        #         },
        #         {
        #           "eventName": "SKILL_DISABLED"
        #         },
        #         {
        #           "eventName": "SKILL_PERMISSION_ACCEPTED"
        #         },
        #         {
        #           "eventName": "SKILL_PERMISSION_CHANGED"
        #         },
        #         {
        #           "eventName": "SKILL_ACCOUNT_LINKED"
        #         },
        #         {
        #           "eventName": "ITEMS_CREATED"
        #         },
        #         {
        #           "eventName": "ITEMS_UPDATED"
        #         },
        #         {
        #           "eventName": "ITEMS_DELETED"
        #         }
        #       ],
        #       "regions": {
        #         "NA": {
        #           "endpoint": {
        #             "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #           }
        #         }
        #       }
        #     }
        #   }
        # },

        # # List Skill Manifest With No Custom Component
        # {
        #   "skillManifest": {
        #     "publishingInformation": {
        #       "locales": {
        #         "en-US": {
        #           "summary": "This is a sample Alexa skill.",
        #           "examplePhrases": [
        #             "Alexa, open sample skill.",
        #             "Alexa, play sample skill."
        #           ],
        #           "keywords": [
        #             "Descriptive_Phrase_1",
        #             "Descriptive_Phrase_2",
        #             "Descriptive_Phrase_3"
        #           ],
        #           "smallIconUri": "https://smallUri.com",
        #           "largeIconUri": "https://largeUri.com",
        #           "name": "Sample skill name.",
        #           "description": "This skill does interesting things."
        #         }
        #       },
        #       "isAvailableWorldwide": False,
        #       "testingInstructions": "1) Say 'Alexa, hello world'",
        #       "category": "HEALTH_AND_FITNESS",
        #       "distributionCountries": [
        #         "US",
        #         "GB",
        #         "DE"
        #       ]
        #     },
        #     "apis": {
        #       "householdList": {}
        #     },
        #     "manifestVersion": "1.0",
        #     "permissions": [
        #       {
        #         "name": "alexa::devices:all:address:full:read"
        #       },
        #       {
        #         "name": "alexa:devices:all:address:country_and_postal_code:read"
        #       },
        #       {
        #         "name": "alexa::household:lists:read"
        #       },
        #       {
        #         "name": "alexa::household:lists:write"
        #       }
        #     ],
        #     "privacyAndCompliance": {
        #       "allowsPurchases": False,
        #       "locales": {
        #         "en-US": {
        #           "termsOfUseUrl": "http://www.termsofuse.sampleskill.com",
        #           "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com"
        #         }
        #       },
        #       "isExportCompliant": True,
        #       "containsAds": False,
        #       "isChildDirected": False,
        #       "usesPersonalInfo": False
        #     },
        #     "events": {
        #       "endpoint": {
        #         "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #       },
        #       "subscriptions": [
        #         {
        #           "eventName": "SKILL_ENABLED"
        #         },
        #         {
        #           "eventName": "SKILL_DISABLED"
        #         },
        #         {
        #           "eventName": "SKILL_PERMISSION_ACCEPTED"
        #         },
        #         {
        #           "eventName": "SKILL_PERMISSION_CHANGED"
        #         },
        #         {
        #           "eventName": "SKILL_ACCOUNT_LINKED"
        #         },
        #         {
        #           "eventName": "ITEMS_CREATED"
        #         },
        #         {
        #           "eventName": "ITEMS_UPDATED"
        #         },
        #         {
        #           "eventName": "ITEMS_DELETED"
        #         }
        #       ],
        #       "regions": {
        #         "NA": {
        #           "endpoint": {
        #             "uri": "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"
        #           }
        #         }
        #       }
        #     }
        #   }
        # },


        # # Flash Briefing Skill Manifest
        # {
        #   "skillManifest": {
        #     "manifestVersion": "1.0",
        #     "publishingInformation": {
        #       "locales": {
        #         "en-US": {
        #           "name": "Sample skill name.",
        #           "summary": "This is a sample Alexa skill.",
        #           "description": "This skill has basic and advanced features.",
        #           "smallIconUri": "https://smallUri.com",
        #           "largeIconUri": "https://largeUri.com",
        #           "examplePhrases": [],
        #           "keywords": [
        #             "Flash Briefing",
        #             "News",
        #             "Happenings"
        #           ]
        #         }
        #       },
        #       "distributionCountries": [
        #         "US",
        #         "GB",
        #         "DE"
        #       ],
        #       "isAvailableWorldwide": False,
        #       "testingInstructions": "1) Say 'Alexa, hello world'",
        #       "category": "HEALTH_AND_FITNESS"
        #     },
        #     "privacyAndCompliance": {
        #       "allowsPurchases": False,
        #       "usesPersonalInfo": False,
        #       "isChildDirected": False,
        #       "isExportCompliant": True,
        #       "containsAds": False,
        #       "locales": {
        #         "en-US": {
        #           "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com",
        #           "termsOfUseUrl": "http://www.termsofuse.sampleskill.com"
        #         }
        #       }
        #     },
        #     "apis": {
        #       "flashBriefing": {
        #         "locales": {
        #           "en-US": {
        #             "customErrorMessage": "Error message",
        #             "feeds": [
        #               {
        #                 "name": "feed name",
        #                 "isDefault": True,
        #                 "vuiPreamble": "In this skill",
        #                 "updateFrequency": "HOURLY",
        #                 "genre": "POLITICS",
        #                 "imageUri": "https://fburi.com",
        #                 "contentType": "TEXT",
        #                 "url": "https://feeds.sampleskill.com/feedX"
        #               }
        #             ]
        #           }
        #         }
        #       }
        #     }
        #   }
        # },

        # # Video Skill Manifest
        # {
        #   "skillManifest": {
        #     "publishingInformation": {
        #       "locales": {
        #         "en-US": {
        #           "summary": "This is a sample Alexa skill.",
        #           "examplePhrases": [
        #             "Alexa, tune to channel 206",
        #             "Alexa, search for comedy movies",
        #             "Alexa, pause."
        #           ],
        #           "keywords": [
        #             "Video",
        #             "TV"
        #           ],
        #           "name": "VideoSampleSkill",
        #           "smallIconUri": "https://smallUri.com",
        #           "largeIconUri": "https://smallUri.com",
        #           "description": "This skill has video control features."
        #         }
        #       },
        #       "isAvailableWorldwide": False,
        #       "testingInstructions": "",
        #       "category": "SMART_HOME",
        #       "distributionCountries": [
        #         "US",
        #         "GB",
        #         "DE"
        #       ]
        #     },
        #     "apis": {
        #       "video": {
        #         "locales": {
        #           "en-US": {
        #             "videoProviderTargetingNames": [
        #               "TV provider"
        #             ],
        #             "catalogInformation": [
        #               {
        #                 "sourceId": "1234",
        #                 "type": "FIRE_TV"
        #               }
        #             ]
        #           }
        #         },
        #         "endpoint": {
        #           "uri": "arn:aws:lambda:us-east-1:452493640596:function:sampleSkill"
        #         },
        #         "regions": {
        #           "NA": {
        #             "endpoint": {
        #               "uri": "arn:aws:lambda:us-east-1:452493640596:function:sampleSkill"
        #             },
        #             "upchannel": [
        #               {
        #                 "uri": "arn:aws:sns:us-east-1:291420629295:sampleSkill",
        #                 "type": "SNS"
        #               }
        #             ]
        #           }
        #         }
        #       }
        #     },
        #     "manifestVersion": "1.0",
        #     "privacyAndCompliance": {
        #       "allowsPurchases": False,
        #       "locales": {
        #         "en-US": {
        #           "termsOfUseUrl": "http://www.termsofuse.sampleskill.com",
        #           "privacyPolicyUrl": "http://www.myprivacypolicy.sampleskill.com"
        #         }
        #       },
        #       "isExportCompliant": True,
        #       "isChildDirected": False,
        #       "usesPersonalInfo": False,
        #       "containsAds": False
        #     }
        #   }
        # },

    ]






class TestAlexaSkill(object):


    """
        Test methods
    """
    @pytest.mark.parametrize('skillId, param, kwargs, exp', [
        ('0', 'manifestVersion', {}, '1.0'),
        ('0', 'locales', {}, ['en-US']),
        ('0', 'summary', {'locale': 'en-US'}, "This is a sample Alexa custom skill."),
        ('0', 'examplePhrases', {'locale': 'en-US'}, [
            "Alexa, open sample custom skill.",
            "Alexa, play sample custom skill."]),
        ('0', 'keywords', {'locale': 'en-US'}, [
            "Descriptive_Phrase_1",
            "Descriptive_Phrase_2",
            "Descriptive_Phrase_3"]),
        ('0', 'name', {'locale': 'en-US'}, "Sample custom skill name."),
        ('0', 'smallIconUri', {'locale': 'en-US'}, "https://smallUri.com"),
        ('0', 'largeIconUri', {'locale': 'en-US'}, "https://largeUri.com"),
        ('0', 'description', {'locale': 'en-US'}, "This skill does interesting things."),
        ('0', 'privacyPolicyUrl', {'locale': 'en-US'}, "http://www.myprivacypolicy.sampleskill.com"),
        ('0', 'termsOfUseUrl', {'locale': 'en-US'}, "http://www.termsofuse.sampleskill.com"),
        ('0', 'endpointRegionUri', {'region': 'NA'}, "https://customapi.sampleskill.com"),
        ('0', 'endpointRegionCertType', {'region': 'NA'}, 'Trusted'),
        ('0', 'eventRegionUri', {'region': 'NA'}, "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"),
        ('0', 'isAvailableWorldwide', {}, False),
        ('0', 'testingInstructions', {}, "1) Say 'Alexa, hello world'"),
        ('0', 'category', {}, "HEALTH_AND_FITNESS"),
        ('0', 'distributionCountries', {}, ["US", "GB", "DE"]),
        ('0', 'endpointUri', {}, "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"),
        # ('0', 'interfaces', {}, ),
        ('0', 'allowsPurchases', {}, False),
        ('0', 'usesPersonalInfo', {}, False),
        ('0', 'isChildDirected', {}, False),
        ('0', 'isExportCompliant', {}, True),
        ('0', 'containsAds', {}, False),
        ('0', 'eventUri', {}, "arn:aws:lambda:us-east-1:040623927470:function:sampleSkill"),
        ('0', 'keywords', {'locale': 'en-US'}, [
            "Descriptive_Phrase_1",
            "Descriptive_Phrase_2",
            "Descriptive_Phrase_3"]),
        ('0', 'permissions', {}, [
            "alexa::devices:all:address:full:read",
            "alexa:devices:all:address:country_and_postal_code:read",
            "alexa::household:lists:read",
            "alexa::household:lists:write"]),
        ('0', 'eventSubscriptions',{}, [
          "SKILL_ENABLED",
          "SKILL_DISABLED",
          "SKILL_PERMISSION_ACCEPTED",
          "SKILL_PERMISSION_CHANGED",
          "SKILL_ACCOUNT_LINKED"]),

    ])
    def test_getParam(self, skillId, param, kwargs, exp, api):
        print "SkillID: %s, param: %s, KWargs: %s -> expected: %s" % (
            skillId, param, kwargs, exp)
        skill = AlexaSkillFactory(api, skillId)
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






