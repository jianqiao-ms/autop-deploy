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
from classes import TableProject

# CONST

# Class&Function Defination
class CIScriptGenerator(BashRequestHandler):
    """
    scripts executed by gitlab-runner after build projects.
    基本逻辑:
        开始 ==> 获取request arguments ==> 生成token字典,保存上传文件信息 ==> 生成ci脚本并返回
    token 结构:
        uuid(16)：{
            project : TableProjectType(role='project')
            ci_commit_short_sha: ci_commit_short_sha
            ci_branch_name : ci_branch_name
        }
    """
    def get(self):
        self.finish(json.dumps(self.application.catm, indent=2))

    async def post(self):
        ci_gitlab_project_id    = int(self.request.arguments['GITLAB_PROJECT_ID'][0])
        ci_commit_short_sha     = self.request.arguments['COMMIT_SHA'][0].decode()[0:8]
        ci_branch_name          = await self.get_ci_branch_from_commit(
            ci_gitlab_project_id, ci_commit_short_sha
        )
        # TODO: 根据curl post过来的PROJECT_ID 和 COMMIT_SHA，调用gitlab api获取更新列表。
        #       根据更新列表，过滤数据库中保存的gitlab project序列，得到最终需要上传artifacts的project序列
        # 生成token字典, 每个token对应一个project 对象（从orm中获取）和相对应的ci信息
        # 保存在Application.catm中，供CIArtifactReceiver创建文件使用
        __build_cmd, __projects = self.get_projects(ci_gitlab_project_id)

        __token_map = dict((
            secrets.token_urlsafe(16),
            dict(
                project = p,
                commit  = ci_commit_short_sha,
                branch  = ci_branch_name
            )
        ) for p in __projects)
        await self.render('bash_scripts/default_ci_script.sh',build_cmd = __build_cmd, token_map = __token_map)
        self.application.catm.update(__token_map)

    def get_projects(self, gitlab_id:int):
        """
        根据ci脚本传过来的gitlab_id, 从数据库中获取可以发布的project列表返回
        :param gitlab_id:
        :return: (build_cmd, [TableProject(role=product)...])
        """
        project_from_db = self.application.session.query(TableProject). \
            filter(TableProject.gitlab_id == gitlab_id).one()
        return (project_from_db.build_cmd,
            list(project_from_db) if project_from_db.role == 'project' else \
                list(filter(lambda x:x if x.role == 'project' else None, project_from_db.children))
        )

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


            pcb                 = self.application.catm[self.request.headers['Artifact-Token']]
            self.ci_filename    = os.path.basename(pcb['project'].artifact_path)
            self.filename       = self.ci_filename + "---{branch}---{commit}".format(
                branch = pcb['branch'],
                commit = pcb['commit']
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