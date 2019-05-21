#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import logging
import json
import secrets
import hashlib

# 3rd-party Packages
from tornado.web import stream_request_body
from tornado.web import HTTPError

# Local Packages
from classes import BashRequestHandler

# CONST

# Class&Function Defination
class CIScriptGenerator(BashRequestHandler):
    """
    scripts executed by gitlab-runner after build projects.
    错误码：
      101: 编译过程出错，跳过上传
    """
    def get(self):
        self.finish(json.dumps(self.application.catm, indent=2))

    async def post(self):
        "BUILD失败后执行"
        if 'BUILD_STATUS' in self.request.arguments:
            if not bool(int(self.get_form_data('BUILD_STATUS'))):
                raise HTTPError(403, reason="编译过程出错，跳过上传")

        ci_args = dict(
            ci_gitlab_project_id = int(self.request.arguments['GITLAB_PROJECT_ID'][0]),
            ci_commit_short_sha = self.request.arguments['COMMIT_SHA'][0].decode()[0:8])
        ci_args['ci_branch_name'] = await self.get_ci_branch_from_commit(
            ci_args['ci_gitlab_project_id'], ci_args['ci_commit_short_sha'])

        # TODO: 根据curl post过来的PROJECT_ID 和 COMMIT_SHA，调用gitlab api获取更新列表。
        #       根据更新列表，过滤数据库中保存的gitlab project序列，得到最终需要上传artifacts的project序列
        # 测试使用的临时数据
        build_cmd = "mvn -P prod -f warranty-parent/pom.xml clean install"
        artifacts = [
            dict(
                project_id = 0,
                artifact   = 'warranty-client/target/warranty-client.jar'
            ),
            dict(
                project_id=0,
                artifact='warranty-manager/target/warranty-manager.jar'
            )
        ]

        # 生成token字典, 每个token对应一个project 对象（从orm中获取）和相对应的ci信息
        # 保存在Application.catm中，供CIArtifactReceiver创建文件使用
        # {
        #   token：{
        #     project : {
        #         project_id : int
        #         artifact : artifact
        #     }
        #     ci_gitlab_project_id: ci_gitlab_project_id
        #     ci_commit_short_sha: ci_commit_short_sha
        #     ci_branch_name : ci_branch_name
        #   }
        # }
        token_map = dict(
            (secrets.token_urlsafe(16), dict(
                project = artifact,
                **ci_args
            )) for artifact in artifacts
        )
        await self.render('bash_scripts/default_ci_script.sh',build_cmd = build_cmd, token_map = token_map)
        self.application.catm.update(token_map)

    async def get_ci_branch_from_commit(self, project_id, commit):
        return json.loads(await self.application.gitlab.read_api('/projects/{id}/repository/commits/{sha}/refs'.format(
            id=project_id, sha=commit
        )))[0]["name"]


@stream_request_body
class CIArtifactReceiver(BashRequestHandler):
    """
    接收CI Runner上传的文件
    需要从Application.catm中获取到文件(包)名称，CI运行环境的branch和commit

    错误码：
      201: 创建文件出错
      202: 上传文件出错, sha356 checksum 不一致
    """
    def prepare(self):
        try:


            token_map           = self.application.catm[self.request.headers['Artifact-Token']]
            self.ci_filename    = os.path.basename(token_map['project']['artifact'])
            self.filename       = self.ci_filename + "---{branch}---{commit}".format(
                branch = token_map['ci_branch_name'],
                commit = token_map['ci_commit_short_sha']
            )
            self.fp             = open(os.path.join('upload', self.filename), 'wb')
            self.ci_sha         = self.request.headers['SHA']
            self.hash_sha256    = hashlib.sha256()
        except:
            logging.exception("创建文件出错")
            self.application.catm.pop(self.request.headers['Artifact-Token'])
            raise HTTPError(503, reason="echo 服务器创建文件出错 && exit 201")
    def put(self):
        if self.hash_sha256.hexdigest() == self.ci_sha:
            self.fp.close()
            self.finish("echo 上传文件完成!Local : {} Remote : {}".format(self.ci_filename, self.fp.name))
            self.application.catm.pop(self.request.headers['Artifact-Token'])
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