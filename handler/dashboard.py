#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web

# Local Packages
# CONST

# Class&Function Defination
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')
    def pre_get(self):
        a = self.test()
    def test(self):
        try:
            raise Exception("in func test")
        except Exception as e:
            self.finish(e.__str__())
            self.request.finish()

route = list([
    ('/', IndexHandler),
])

# Logic
if __name__ == '__main__':
    pass
