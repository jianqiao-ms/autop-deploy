#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

from __future__ import absolute_import
from proj.celery import App

from proj._customTorndb import Connection
from celery.signals import worker_process_init
from celery.signals import worker_process_shutdown

db_conn = None
db_conf = dict(
    host        = '192.168.0.195',
    database    = 'autop',
    user        = 'cupid',
    password    = 'everyone2xhfz'
)

@worker_process_init.connect
def init_worker(**kwargs):
    global db_conn
    print('Initializing database connection for worker.')
    db_conn = Connection(**db_conf)


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global db_conn
    if db_conn:
        print('Closing database connectionn for worker.')
        db_conn.close()

@App.task
def mysql_query(cmd):
    return db_conn.query(cmd)

@App.task
def mysql_get(cmd):
    return db_conn.query(cmd)