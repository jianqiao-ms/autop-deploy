#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import json
import hashlib

# 3rd-party Packages
from tornado.web import stream_request_body

# Local Packages
from classes import RequestHandler
from classes import CIArtifactTokenManager
from classes import log

# CONST

# Class&Function Defination
class CIScriptGenerator(RequestHandler):
    """
    scripts executed by gitlab-runner after build projects.
    错误码：
      101: 编译过程出错，跳过上传
    """
    scripts = """
#!/bin/bash
"""
    async def post(self):
        ci_build_status            = bool(int(self.request.arguments['BUILD_STATUS'][0]))
        if not ci_build_status:
            self.write("""echo "编译过程出错，跳过上传" && exit 101""")
            return

        ci_project_id              = int(self.request.arguments['PROJECT_ID'][0])
        ci_commit_short_sha        = self.request.arguments['COMMIT_SHA'][0].decode()[0:8]
        ci_branch_from_gitlab_api  = json.loads(
            await self.application.gitlab.read_api('/projects/{id}/repository/commits/{sha}/refs'.format(
                id = ci_project_id, sha = ci_commit_short_sha
        )))[0]['name']
        ci_args = dict(
            ci_project_id = ci_project_id,
            ci_commit_short_sha = ci_commit_short_sha,
            ci_branch_name = ci_branch_from_gitlab_api
        )

        # 测试使用的临时数据
        artifacts = [
            'warranty-client/target/warranty-client.jar',
            'warranty-manager/target/warranty-manager.jar'
        ]

        # 生成上传使用的脚本
        self.scripts += ''.join([
            self.application.catm.gen_token(x, ci_args) for x in artifacts
        ])
        self.write(self.scripts)

@stream_request_body
class CIArtifactReceiver(RequestHandler):
    """
    错误码：
      201: 创建文件出错
      202: 上传文件出错, sha356 checksum 不一致
    """
    def prepare(self):
        try:
            token_map           = self.application.catm[self.request.headers['Artifact-Token']]
            filename            = token_map['filename'] + "---{branch}---{commit}".format(
                branch = token_map['branch_name'],
                commit = token_map['commit_sha']
            )
            self.fp             = open(os.path.join('upload', filename), 'wb')
            self.ci_sha         = self.request.headers['SHA']
            self.hash_sha256    = hashlib.sha256()
        except:
            log.exception("创建文件出错")
            self.finish("echo 服务器创建文件出错 && exit 201")
    def put(self):
        if self.hash_sha256.hexdigest() == self.ci_sha:
            self.fp.close()
            self.application.catm.pop(self.request.headers['Artifact-Token'])
            self.finish("echo 上传文件完成!")
        else:
            del self.fp
            self.application.catm.pop(self.request.headers['Artifact-Token'])
            self.finish("echo 上传文件出错, sha356 checksum 不一致! && exit 202")
    async def data_received(self, chunk: bytes):
        self.fp.write(chunk)
        self.hash_sha256.update(chunk)


# Logic
if __name__ == '__main__':
    from tornado.ioloop import IOLoop
    from tornado.web import Application
    import tornado.options

    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    application = Application([
        (r"/api/v1/gitlab/jobscripts", CIScriptGenerator),
        (r"/api/v1/gitlab/receiver", CIArtifactReceiver)
    ])
    application.listen(60000)
    IOLoop.current().start()