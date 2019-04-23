#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import secrets

# 3rd-party Packages

# Local Packages
from logger import log


# CONST

# Class&Function Defination
class CIArtifactTokenManager(dict):
    def gen_token(self, ci_artifact: str, ci_args:dict):
        secrets16 =  secrets.token_urlsafe(16)
        self[secrets16] = dict(
            filename = os.path.basename(ci_artifact),
            filepath = ci_artifact,
            project_id = ci_args['ci_project_id'],
            commit_sha = ci_args['ci_commit_short_sha'],
            branch_name = ci_args['ci_branch_name']
        )

        return """curl -H "Artifact-Token:{token}" -H "SHA:`sha256sum {file0}|awk '{{print $1}}'`" -T {file1}  http://192.168.2.200:60000/api/v1/gitlab/receiver | bash\n""".format(
            token=secrets16,
            file0=ci_artifact,
            file1=ci_artifact
        )

    def add_map(self, map:dict):
        self.update(map)

    def get_artifact(self, token:str):
        return self[token]

# Logic
if __name__ == '__main__':
    token_manager = CIArtifactTokenManager()
    token_manager.gen_token('warranty-client/target/warranty-client.jar')
    print(token_manager.items())
