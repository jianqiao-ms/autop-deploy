#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape

# system packages

# self packages
from handlers.base import BaseHandler
from handlers.base import authenticated
from handlers.base import async_authenticated

class AdminHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('admin/admin.html')

class DbInitHandler(BaseHandler):
    @async_authenticated
    async def get(self):
        gitlab_projects = await self.get_gitlab_api('/projects')

        gitlab_projects = escape.json_decode(escape.to_unicode(gitlab_projects))

        for p in gitlab_projects:
            print('正在添加{}'.format(p['name']))
            self.db_sesion.add(self.table['Project'](
                gitlab_id   = p['id'],
                name        = p['name'],
                deploy_name = '',
                description = p['description'],
                repo_ssh    = p['ssh_url_to_repo'],
                repo_htts   = p['http_url_to_repo'],
                lang        = '',
                tags        = ''
            ))
            self.db_sesion.commit()

            # print(p)
        # self.finish()