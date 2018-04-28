#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado.web import HTTPError
from tornado.util import PY3
from tornado.process import Subprocess
import tornado.escape
from tornado.httpclient import AsyncHTTPClient as HTTPClient

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
if PY3:
    import urllib.parse as urlparse
    import urllib.parse as urllib_parse
    long = int
else:
    import urlparse
    import urllib as urllib_parse
# self packages
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import db as Database

# def run_command(command):
# """run command"""
# async def run_command(command):
#     process = Subprocess(
#         shlex.split(command),
#         stdout=Subprocess.STREAM,
#         stderr=Subprocess.STREAM
#     )
    # out, err = await process.stdout.read_until_close(), process.stderr.read_until_close()
    # return (out,err)
    # return process

###############################
# GITLAB Configuration
###############################
# GITLAB                          = 'http://192.168.3.252'
GITLAB                          = 'http://gitlab.shangweiec.com'
GITLAB_API_PREFIX               = '{}/api/v4'.format(GITLAB)
GITLAB_OAUTH_AUTHORIZE_URL      = '{}/oauth/authorize'.format(GITLAB)
GITLAB_OAUTH_ACCESS_TOKEN_URL   = '{}/oauth/token'.format(GITLAB)

GITLAB_OAUTH_REDIRECT_URI       = 'http://localhost:60000/login'
GITLAB_OAUTH_APP_ID             = 'e49e6db2f2b83295d43ab21490137687c2c068283ddc9eccdcf752221e5f7e9a'
GITLAB_OAUTH_APP_SECRET         = '0ca6835640412d1d7d6d149fc47dcb5ad41602a87c129cd3c30bf58329cbd358'


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
    _OAUTH_AUTHORIZE_URL = '{}/oauth/authorize'.format(GITLAB)
    _OAUTH_ACCESS_TOKEN_URL = '{}/oauth/token'.format(GITLAB)

    _OAUTH_REDIRECT_URI = 'http://localhost:60000/login'

    async def get(self):
        returned_code = self.get_query_argument('code', False)
        redirect_next = self.get_query_argument('next', False)

        if returned_code:
            access_token = await self.get_authenticated_user(returned_code)
            self.set_cookie('token',access_token['access_token'])
            self.redirect(redirect_next if redirect_next else '/')
        else:
            await self.authorize_redirect(
                redirect_uri=GITLAB_OAUTH_REDIRECT_URI,
                client_id=GITLAB_OAUTH_APP_ID,
                response_type='code',
                extra_params = {
                    'state':GITLAB_OAUTH_APP_SECRET,
                    'next': redirect_next if redirect_next else '/'
                }
            )

    async def get_authenticated_user(self, code):
        parameters = urlencode(
            {
                'client_id': GITLAB_OAUTH_APP_ID,
                'client_secret': GITLAB_OAUTH_APP_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': GITLAB_OAUTH_REDIRECT_URI
            }
        )
        http_client = self.get_auth_http_client()
        response =  await http_client.fetch(GITLAB_OAUTH_ACCESS_TOKEN_URL, body=parameters, method='POST')

        return tornado.escape.json_decode(response.body)

class SqlSchema(object):
    environment = Database.Environment
    container = Database.Container
    app_type = Database.AppType
    app = Database.App
    deploy_rule = Database.DeployRule
    deploy_history = Database.DeployHistory

class BaseHandler(RequestHandler, OAuth2Mixin):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.db_sesion = Database.session
        self.schema = SqlSchema

    async def get_current_user(self):
        token = self.get_cookie('token')
        if not token:
            return None
        user = await self.oauth2_request('{}/api/v4/user'.format(GITLAB), access_token=token)
        return user

    async def get_gitlab_api(self, url):
        GITLAB_API_PREFIX   = '{}/api/v4'.format(GITLAB)
        _httpclient         = self.get_auth_http_client()
        _header             = {'Private-Token': '9PnZDPXdzpxskMu3vmRy'}

        _response = await _httpclient.fetch(GITLAB_API_PREFIX + url, headers = _header, method='HEAD')
        _response = await _httpclient.fetch(GITLAB_API_PREFIX + url + '?per_page={}'.format(_response.headers['X-Total']), headers = _header)
        return _response.body

if __name__ == '__main__':
    from tornado.httpclient import HTTPClient as SyncHTTPClient
    from tornado.httputil import HTTPHeaders
    from tornado.httpclient import HTTPRequest


    request = HTTPRequest(GITLAB_API_PREFIX + '/projects', headers=HTTPHeaders({'Private-Token': 'TH_rmdTezUXEEQa74tQg'}), method= "HEAD")
    response = SyncHTTPClient().fetch(request)
    print(response.headers)
    # print(len(tornado.escape.json_decode(response.body)))