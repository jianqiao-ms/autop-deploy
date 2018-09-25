#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import json

# 3rd-party Packages
import tornado.web
from tornado.escape import json_decode, json_encode

from sqlalchemy.exc import IntegrityError

# Local Packages
from classes.appliacation import LOGGER
from classes.appliacation import Application
from classes.handlers import NotInitialized
from classes.schema.SchemaDeploy import SchemaProjectType, SchemaProject, \
    SchemaAutoRule, SchemaAutoHistory, SchemaManul

# CONST

# Class&Function Defination


class DeployHandler(tornado.web.RequestHandler):
    def get(self):
        headers = {"Content-Type":""}
        headers.update(self.request.headers)

        self.finish(self.__json__) if headers["Content-Type"] == "application/json" else \
            self.render(self.__prefix__ + self.__view__, object = self.__object__)

    def post(self, *args, **kwargs):
        print(self.request.body)
        item = self.__schema__(**json_decode(self.request.body))

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            LOGGER.exception()
            self.application.mysql.rollback()
            self.finish('{} named {} already exist!'.format(kwargs['item'], item.visiblename))
            return
        except:
            self.application.mysql.rollback()
            LOGGER.exception('Except during Create {}'.format(kwargs['item']))
            return
        self.finish(str(item.id))

    @property
    def __arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

    @property
    def __object__(self):
        return self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all() if \
            self.__schema__ is not NotInitialized else \
            None

    @property
    def __json__(self):
        records = self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all()
        rst = json.dumps([r.json() for r in records], ensure_ascii=False, indent=2)
        return rst if self.__schema__ is not NotInitialized else \
            json.dumps({"ERROR":"Not supported Content-Type"})

    @property
    def __schema__(self):
        return NotInitialized

    @property
    def __prefix__(self):
        return 'deploy/'

    @property
    def __view__(self):
        return 'deploy.html'

class ProjectTypeHandler(DeployHandler):
    @property
    def __schema__(self):
        return SchemaProjectType

    @property
    def __view__(self):
        return 'project_type.html'

class ProjectHandler(DeployHandler):
    @property
    def __schema__(self):
        return SchemaProject

    @property
    def __view__(self):
        return 'project.html'

class AutoRuleHandler(DeployHandler):
    @property
    def __schema__(self):
        return SchemaAutoRule

    @property
    def __view__(self):
        return 'auto.html'

class ManulHandler(DeployHandler):
    @property
    def __schema__(self):
        return SchemaManul

    @property
    def __view__(self):
        return 'manul.html'

# application
app_deploy = Application([
    ('/deploy', DeployHandler),
    ('/deploy/projecttype', ProjectTypeHandler),
    ('/deploy/project', ProjectHandler),
    ('/deploy/auto', AutoRuleHandler),
    ('/deploy/manul', ProjectHandler),
])

# Logic
if __name__ == '__main__':
    pass
