#! /usr/bin/env python
#-* coding: utf-8 -*

from tornado.process import Subprocess
import shlex

async def run_command(command):
    """run command"""
    process = Subprocess(
        shlex.split(command),
        stdout=Subprocess.STREAM,
        stderr=Subprocess.STREAM
    )
    out, err = await process.stdout.read_until_close(), process.stderr.read_until_close()
    return (out,err)