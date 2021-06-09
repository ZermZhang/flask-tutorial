#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : __init__.py
@Software       : PyCharm
@Modify Time    : 2021/6/3 17:22
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
import os
from flask import Flask
from datetime import timedelta

from . import db
from . import auth
from . import blog

from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config is passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    # 导入并注册蓝图
    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app
