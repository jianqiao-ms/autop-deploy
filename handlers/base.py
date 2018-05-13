#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado.util import PY3
import tornado.escape

# system packages
import sys
import os

if PY3:
    pass
else:
    pass
if PY3:
    long = int
else:
    pass
# self packages
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from handlers import database

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
GITLAB_PRIVATE_TOKEN            = '9PnZDPXdzpxskMu3vmRy'

GITLAB_OAUTH_REDIRECT_URI       = 'http://localhost:60000/login'
GITLAB_OAUTH_APP_ID             = 'e49e6db2f2b83295d43ab21490137687c2c068283ddc9eccdcf752221e5f7e9a'
GITLAB_OAUTH_APP_SECRET         = '0ca6835640412d1d7d6d149fc47dcb5ad41602a87c129cd3c30bf58329cbd358'

GITLAB_API_PREFIX               = '{}/api/v4'.format(GITLAB)
GITLAB_OAUTH_AUTHORIZE_URL      = '{}/oauth/authorize'.format(GITLAB)
GITLAB_OAUTH_ACCESS_TOKEN_URL   = '{}/oauth/token'.format(GITLAB)

# class SqlSchema(object):
#     environment = database.Environment
#     container = database.Container
#     app_type = database.AppType
#     app = database.App
#     deploy_rule = database.DeployRule
#     deploy_history = database.DeployHistory

class BaseHandler(RequestHandler, OAuth2Mixin):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.database = database
        # self.schema = SqlSchema

    async def get_gitlab_api(self, url):
        _httpclient         = self.get_auth_http_client()
        _header             = {'Private-Token': GITLAB_PRIVATE_TOKEN}

        _response = await _httpclient.fetch(GITLAB_API_PREFIX + url, headers = _header, method='HEAD')
        _response = await _httpclient.fetch(GITLAB_API_PREFIX + url + '?per_page={}'.format(_response.headers['X-Total']), headers = _header)
        return tornado.escape.json_decode(_response.body)

if __name__ == '__main__':
    from tornado.httpclient import HTTPClient as SyncHTTPClient
    from tornado.httputil import HTTPHeaders
    from tornado.httpclient import HTTPRequest


    request = HTTPRequest(GITLAB_API_PREFIX + '/projects', headers=HTTPHeaders({'Private-Token': 'TH_rmdTezUXEEQa74tQg'}), method= "HEAD")
    response = SyncHTTPClient().fetch(request)
    print(response.headers)
    # print(len(tornado.escape.json_decode(response.body)))