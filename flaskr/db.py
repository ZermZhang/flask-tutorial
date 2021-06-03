#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : db
@Software       : PyCharm
@Modify Time    : 2021/6/3 17:47
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    # Flask在返回相应之后进行清理时会调用该函数
    app.teardown_appcontext(close_db)

    # 添加一个新的可以与flask一起工作的命令
    # 在工厂中导入并调用这个函数
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    clear the existing data and create new tables
    """
    init_db()
    click.echo('Initializer the database')
