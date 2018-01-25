#! /usr/bin/env python
"""Small script to retrieve Authentication Data via Oauth2 from Amazon.blank

Usage:
$> authweb.py

Open printen url in Browser and follow the steps.

You get the autentication data printed in the website.

"""

import cherrypy
from settings import Settings
import requests
import urllib


class Start(object):

    def __init__(self, setting):
        self.setting = setting

    def index(self):

        url = "https://www.amazon.com/ap/oa"
        callback = cherrypy.url() + "authresponse"
        payload = {
            "client_id": self.setting.clientID,
            "scope": "alexa::ask:skills:readwrite alexa::ask:skills:test alexa::ask:models:readwrite",
            "response_type": "code",
            "redirect_uri": callback,
        }
        req = requests.Request('GET', url, params=payload)
        p = req.prepare()
        raise cherrypy.HTTPRedirect(p.url)

    def authresponse(self, var=None, **params):
        code = urllib.quote(cherrypy.request.params['code'])
        callback = cherrypy.url()
        payload = {
            "client_id": self.setting.clientID,
            "client_secret": self.setting.clientSecret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": callback
        }
        url = "https://api.amazon.com/auth/o2/token"
        r = requests.post(url, data=payload)
        resp = r.json()
        self.setting.updateWithResponse(resp)
        return "Success! Here is your refresh token:<br>{}".format(
            resp)

    index.exposed = True
    authresponse.exposed = True


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE" % (sys.argv[0], )
        sys.exit(0)

    asetting = Settings(sys.argv[1])

    cherrypy.config.update({'server.socket_host': 'localhost'})
    cherrypy.config.update({'server.socket_port': asetting.webPort})
    print('Open http://localhost:%d to login in amazon alexa service' % asetting.webPort)
    cherrypy.quickstart(Start(asetting))
