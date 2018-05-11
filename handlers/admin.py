#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape
from tornado.web import RequestHandler
# system packages

# self packages
from handlers.base import BaseHandler


class AdminHandler(BaseHandler):
    def get(self):
        self.render('admin/admin.html')

class AdminItemHandler(BaseHandler):
    def get(self):
        _, _, item = self.request.path.rpartition('/')
        if item:
            items = self.db_sesion.query(getattr(self.schema,item)).all()
            self.render('admin/admin-{}.html'.format(item), items=items)

class AdminEnvHandler(AdminItemHandler):
    def post(self):
        pass

class AdminContainerHandler(AdminItemHandler):
    def post(self):
        pass

class AdminAppTypeHandler(AdminItemHandler):
    def post(self):
        pass

class AdminAppHandler(AdminItemHandler):
    def post(self):
        pass

class AdminDeployRuleHandler(AdminItemHandler):
    def post(self):
        pass

class AdminDeployHistoryHandler(AdminItemHandler):
    def post(self):
        pass

class DbInitHandler(BaseHandler):
    async def get(self):
        response_body = await self.get_gitlab_api('/projects')
        gitlab_projects = escape.json_decode(escape.to_unicode(response_body))

        for p in gitlab_projects:
            self.write('正在添加{}<br />'.format(p['name']))
            self.db_sesion.add(self.schema.project(
                gitlab_id   = p['id'],
                name        = p['name'],
                full_name   = p['name_with_namespace'],
                deploy_name = '',
                description = p['description'],
                repo_ssh    = p['ssh_url_to_repo'],
                repo_htts   = p['http_url_to_repo'],
                lang        = '',
                tags        = ''
            ))
        try:
            self.db_sesion.commit()
            self.write('完成')
        except Exception as e:
            self.db_sesion.rollback()
            import traceback
            self.write(escape.xhtml_escape(str(traceback.format_exc())))
        finally:
            self.finish()
