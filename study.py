#! /usr/bin/env python
#-* coding: utf-8 -*

import time
import asyncio

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)


start = now()

loop = asyncio.get_event_loop()
loop.run_until_complete(do_some_work(2))

print('TIME: ', now() - start)