#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape
from tornado.websocket import WebSocketHandler
from tornado.process import Subprocess

# system packages
import os
import shlex

# self packages
from handlers.base import BaseHandler


class ProjectListHandler(BaseHandler):
    async def get(self):
        _gitlab_id = self.get_query_argument('gitlab_id', False)
        if not _gitlab_id:
            _projects = self.db_sesion.query(self.schema.project).all()
            self.render('project/project.html', projects = _projects)
        else:
            _project = self.db_sesion.query(self.schema.project).filter(
                self.schema.project.gitlab_id == _gitlab_id).one()
            _commits = await self.get_gitlab_api(
                '/projects/{project_id}/repository/commits'.format(project_id=_gitlab_id))

            _history = self.db_sesion.query(self.schema.deploy_history).filter(
                self.schema.deploy_history.gitlab_id == _gitlab_id).order_by(self.schema.deploy_history.op_time)[-20:]

            self.render('project/projectdetails.html', project=_project, commits=escape.json_decode(_commits),
                        history=_history)