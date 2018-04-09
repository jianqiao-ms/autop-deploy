#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape
from tornado.websocket import WebSocketClientConnection
from tornado.process import Subprocess

# system packages
import os
import shlex

# self packages
from handlers.base import BaseHandler
from handlers.base import authenticated
from handlers.base import async_authenticated

class DeployHandler(BaseHandler):
    @async_authenticated
    async def get(self):
        _gitlab_id = self.get_query_argument('gitlab_id', False)
        if not _gitlab_id:
            _projects = self.db_sesion.query(self.schema.project).all()
            self.render('deploy/deploy.html', projects = _projects)
        else:
            _project = self.db_sesion.query(self.schema.project).filter(self.schema.project.gitlab_id == _gitlab_id).one()
            _commits = await self.get_gitlab_api('/projects/{project_id}/repository/commits'.format(project_id = _gitlab_id))
            _history = self.db_sesion.query(self.schema.deploy_history).filter(self.schema.deploy_history.gitlab_id == _gitlab_id).order_by(self.schema.deploy_history.op_time)[-20:]

            self.render('deploy/details.html', project = _project, commits = escape.json_decode(_commits), history = _history)

class DeployActionHandler(BaseHandler):
    async def get(self):
        # _gitlab_id = self.get_query_argument('gitlab_id', False)
        _gitlab_id = 39
        _commit = self.get_query_argument('commit', False)
        _project = self.db_sesion.query(self.schema.project).filter(self.schema.project.gitlab_id == _gitlab_id).one()

        os.chdir('/home/jianqiao/Workspace/autop/tmp')
        process = Subprocess(
                        # shlex.split('git clone {}'.format(_project.repo_ssh)),
                        shlex.split('ping -c 10 baidu.com'),
                        stdout=Subprocess.STREAM,
                        stderr=Subprocess.STREAM
                    )

        out, err = await process.stdout.read_bytes(32), process.stderr.read_bytes(32)

        while process.returncode != None:
            print(out)

        # for data in out:
        #     self.write(data)
        # self.finish()