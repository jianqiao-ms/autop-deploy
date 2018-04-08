#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado.web import HTTPError
from tornado.util import PY3
from tornado.process import Subprocess
import tornado.escape

# system packages
import sys
import os
import shlex
import functools
if PY3:
    import urllib.parse as urlparse
    from urllib.parse import urlencode
else:
    import urlparse
    from urllib import urlencode

# self packages
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from db import db_session
from db import Project

async def run_command(command):
    """run command"""
    process = Subprocess(
        shlex.split(command),
        stdout=Subprocess.STREAM,
        stderr=Subprocess.STREAM
    )
    out, err = await process.stdout.read_until_close(), process.stderr.read_until_close()
    return (out,err)

def adminAuthenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user == 'root':
            raise HTTPError(403)
    return wrapper

def authenticated(method):

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        self.current_user = await self.get_current_user()
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

def async_authenticated(method):

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        self.current_user = await self.get_current_user()
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return await method(self, *args, **kwargs)
    return wrapper

class GitlabOAuth2LoginHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = 'http://192.168.3.252/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'http://192.168.3.252/oauth/token'
    _OAUTH_REDIRECT_URI = 'http://192.168.2.200:60000/login'
    _OAUTH_APP_ID = 'e49e6db2f2b83295d43ab21490137687c2c068283ddc9eccdcf752221e5f7e9a'
    _OAUTH_APP_SECRET = '0ca6835640412d1d7d6d149fc47dcb5ad41602a87c129cd3c30bf58329cbd358'


    async def get(self):
        returned_code = self.get_query_argument('code', False)
        redirect_next = self.get_query_argument('next', False)

        if returned_code:
            access_token = await self.get_authenticated_user(returned_code)
            self.set_cookie('token',access_token['access_token'])
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
        parameters = urlencode(
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

        return tornado.escape.json_decode(response.body)

class BaseHandler(RequestHandler, OAuth2Mixin):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.db_sesion = db_session
        self.table = {
            'Project':Project
        }

    async def get_current_user(self):
        token = self.get_cookie('token')
        if not token:
            return None
        user = await self.oauth2_request('http://192.168.3.252/api/v4/user', access_token=token)
        return user

    async def get_gitlab_api(self, url):
        gitlab_api_prefix = 'http://192.168.3.252/api/v4'
        _httpclient = self.get_auth_http_client()
        _header = {
            'Private-Token': 'hsssfmR1LxNAfCG5NB7g'
        }

        resonse =  await _httpclient.fetch(gitlab_api_prefix + url, headers = _header)
        return resonse.body

if __name__ == '__main__':
    print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))