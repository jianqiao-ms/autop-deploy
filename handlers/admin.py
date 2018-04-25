#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape
from tornado.web import RequestHandler
# system packages

# self packages
from handlers.base import BaseHandler
from handlers.base import authenticated
from handlers.base import async_authenticated

admin_items = {
    'environment':{
        'link':'/admin/environment',
        'handler':None,
        'text':'环境'
    },
    'host':{
        'link': '/admin/host',
        'handler': None,
        'text': '主机'
    },
    'hostgroup': {
        'link': '/admin/hostgroup',
        'handler': None,
        'text': '主机组'
    },
    'apptype': {
        'link': '/admin/apptype',
        'handler': None,
        'text': '应用类型'
    },
    'app': {
        'link': '/admin/app',
        'handler': None,
        'text': '应用'
    },
    '发布规则': {
        'link': '/admin/deployrule',
        'handler': None,
        'text': '发布规则'
    }
}


class AdminPage(BaseHandler):
    @authenticated
    def get(self, item):
        if not item:
            self.render('admin/admin.html', admin_items = admin_items)
        else:
            pass

class DbInitHandler(BaseHandler):
    @async_authenticated
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
