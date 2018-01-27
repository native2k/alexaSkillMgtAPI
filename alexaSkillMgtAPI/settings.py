#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sesttings object for API

"""
import logging
import yaml
import types
import requests
from voluptuous import Schema, Required, All, Length, Range, Inclusive, Optional
from datetime import datetime, timedelta

log = logging.getLogger('AlexaSkillMgtAPI')
log.addHandler(logging.NullHandler())

BASE_KEY = 'AmazonOAuth'


class Settings(object):
    """ Holds settings for libary

    Attributes:
        configFile (String): Location of config file
    """
    _refresh_format = '%Y-%m-%d_%H:%M'
    _msg = 'accessToken, tokenType, expiresIn and refreshToken must exist together'
    _validate = Schema({
        Required(BASE_KEY): {
            Required('clientID'): All(str, Length(min=61)),
            Required('clientSecret'): All(str, Length(min=61)),
            Optional('webPort', default=8080): All(int, Range(min=1024)),
            Inclusive('accessToken', 'token', msg=_msg): All(str, Length(min=61)),
            Inclusive('tokenType', 'token', msg=_msg): All(str, Length(min=5)),
            Inclusive('refreshToken', 'token', msg=_msg): All(str, Length(min=61)),
            Inclusive('expiresIn', 'token', msg=_msg): All(str, Length(min=5)),
        }
    }, extra=True)

    configFile = None

    def __init__(self, config):
        """Returns an Settings Object

        Args:
            config (String): Location of config file

        """
        self._config = {}
        # if not default and not config and not dataDict:
        #     raise Exception('You must provide one of dataDict or config')

        self.configFile = config
        self.readConfig()

        # check if we need to refresh the token
        if self._config.get('refreshToken') and self._config.get('expiresIn'):
            parsedExpired = datetime.strptime(self.expiresIn, self._refresh_format)
            if parsedExpired < datetime.now():
                log.info("Need to refresh token ...")
                self._refreshToken()

    def _refreshToken(self):
        """ Send token refresh request to amazon
        """
        # POST /auth/o2/token HTTP/l.l
        #  Host: api.amazon.com
        #  Content-Type: application/x-www-form-urlencoded;charset=UTF-8
        #  grant_type=refresh_token
        #  &refresh_token=Atzr|IQEBLzAtAhRPpMJxdwVz2Nn6f2y-tpJX2DeX...
        #  &client_id=foodev
        #  &client_secret=Y76SDl2F
        #
        # HTTP/l.l 200 OK
        #  Content-Type: application/json;charset UTF-8
        #  Cache-Control: no-store
        #  Pragma: no-cache
        #  {
        #     "access_token":"Atza|IQEBLjAsAhRmHjNgHpi0U-Dme37rR6CuUpSR...",
        #     "token_type":"bearer",
        #     "expires_in":3600,
        #     "refresh_token":"Atzr|IQEBLzAtAhRPpMJxdwVz2Nn6f2y-tpJX2DeX..."
        #  }
        res = requests.post(
            url='https://api.amazon.com/auth/o2/token',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refreshToken,
                'client_id': self.clientID,
                'client_secret': self.clientSecret
            },
        )
        if res.status_code == 200:
            self.updateWithResponse(res.json())
        else:
            raise Exception('%s: %s' % (
                res.status_code, res.text,
            ))

    def readConfig(self):
        """ Read data from config file.

        Returns:
            Boolean: Success?
        """
        with open(self.configFile, 'r') as infile:
            data = yaml.load(infile)

        if self._validate(data):
            self._config.update(data[BASE_KEY])
            return True

    def writeConfig(self):
        """ Update data in config file.
        """
        if not self._config:
            raise Exception("Unable to overwrite configfile %s with empty data" % (
                self.configFile))

        with open(self.configFile, 'r') as infile:
            data = yaml.load(infile)

        data[BASE_KEY].update(self._config)
        with open(self.configFile, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return True

    def updateWithResponse(self, response):
        """ Update data and config file with response from amazon.

        Args:
            response (Dictionary): Response dict from amazon.

        Returns:
            Boolean: Success?
        """
        if response.get('access_token') and response.get('refresh_token'):
            return self.setAuthData(
                response['access_token'], response['token_type'],
                response['refresh_token'], response['expires_in'],
            )
        else:
            raise Exception("Invalid data for update: %s" % (response, ))

    def setAuthData(self, accessToken, tokenType, refreshToken, expiresIn):
        """ Set authentication Data

        Args:
            accessToken (String): Access Token
            tokenType (String): Access Token Type
            refreshToken (String): Refresh Token
            expiresIn (String): Datestring when Access Token needs to be refreshed

        Returns:
            Boolean: Success?
        """
        self._config['accessToken'] = str(accessToken)
        self._config['tokenType'] = str(tokenType)
        self._config['refreshToken'] = str(refreshToken)

        if isinstance(expiresIn, datetime):
            pass
        elif isinstance(expiresIn, (types.StringTypes, types.IntType)):
            expiresIn = datetime.now() + timedelta(seconds=int(expiresIn))
        else:
            raise Exception('Invalid value for expiresIn')
        self._config['expiresIn'] = expiresIn.strftime(self._refresh_format)
        return self.writeConfig()

    def __getattr__(self, name):
        """Overwrites class.__getattr__ to provide self._config values as attributes.

        Args:
            name (String): Name of the attribute

        Returns:
            TYPE: Description
        """
        if name in self._config:
            return self._config[name]
        raise AttributeError("'%s' object has no attribute '%s'" % (
            self.__class__.__name__, name))

    def __repr__(self):
        """ Representation of class.

        Returns:
            String: Representation
        """
        return '<%s.%s object at %s data=%s>' % (
            self.__class__.__module__, self.__class__.__name__,
            hex(id(self)), self._config)


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print "usage: %s CONFIGFILE" % (sys.argv[0], )
        sys.exit(0)

    asetting = Settings(sys.argv[1])
    asetting.writeConfig()
    print asetting

