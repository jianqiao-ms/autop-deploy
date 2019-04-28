#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import secrets
import logging

# 3rd-party Packages

# Local Packages



# CONST

# Class&Function Defination
class CIArtifactTokenManager(dict):
    """"
    Gitlab CI 编译完成后，将部分变量传递过来申请一个上传文件的token，tokenmanager将token作为key保存相关联的即将上传的文件信息。
    CI Runner 将token放进header里面，使用PUT方法上传文件。平台根据tokenmanager里面的文件信息保存接受到的文件。
    """
    def add_map(self, map:dict):
        self.update(map)

    def get_artifact(self, token:str):
        return self[token]



# Logic
if __name__ == '__main__':
    token_manager = CIArtifactTokenManager()
    print(token_manager.items())
