#! /usr/bin/env python
#-* coding: utf-8 -*

from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
import urllib.parse
import json

class GitlabOAuth2LoginHandler(RequestHandler, OAuth2Mixin):
    _GITLAB_URI = 'http://192.168.3.252'

    _OAUTH_AUTHORIZE_URL = '{GITLAB}/oauth/authorize'.format(GITLAB = _GITLAB_URI)
    _OAUTH_ACCESS_TOKEN_URL = '{GITLAB}/oauth/token'.format(GITLAB = _GITLAB_URI)

    _OAUTH_REDIRECT_URI = 'http://192.168.2.200:60000/login'
    _OAUTH_APP_ID = 'e49e6db2f2b83295d43ab21490137687c2c068283ddc9eccdcf752221e5f7e9a'
    _OAUTH_APP_SECRET = '0ca6835640412d1d7d6d149fc47dcb5ad41602a87c129cd3c30bf58329cbd358'

    _USERNAME_ACCESS_URL = '{GITLAB}/api/v4/user'.format(GITLAB = _GITLAB_URI)



    async def get(self):
        returned_code = self.get_query_argument('code', False)
        redirect_next = self.get_query_argument('next', False)

        if returned_code:
            access_token = await self.get_authenticated_user(returned_code)
            user = await self.oauth2_request(self._USERNAME_ACCESS_URL,access_token = access_token['access_token'])

            self.set_cookie('token',json.dumps(access_token))
            self.set_cookie('user',user['username'])

            self.redirect(redirect_next if redirect_next else '/')
        else:
            await self.authorize_redirect(
                redirect_uri=self._OAUTH_REDIRECT_URI,
                client_id=self._OAUTH_APP_ID,
                response_type='code',
                extra_params = {
                    'state':self._OAUTH_APP_SECRET,
                    'next': redirect_next if redirect_next else '/'
                }
            )

    async def get_authenticated_user(self, code):
        parameters = urllib.parse.urlencode(
            {
                'client_id': self._OAUTH_APP_ID,
                'client_secret': self._OAUTH_APP_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self._OAUTH_REDIRECT_URI
            }
        )


        http_client = self.get_auth_http_client()
        response =  await http_client.fetch(self._OAUTH_ACCESS_TOKEN_URL, body=parameters, method='POST')

        return json.loads(response.body)