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
from datetime import timedelta, datetime

from flask import Flask
from flask_bootstrap import Bootstrap

from .web import auth, blog, admin
from . import db
from flaskr.libs.extensions import get_login_manager

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def register_template_context(app):
    """
    :param app: flask app 实例
    :return: 全局变量
    """
    @app.context_processor
    def generate_template_context():
        db_cursor = db.get_db()
        posts = db_cursor.execute('SELECT id, username from user').fetchall()
        admin = [ele[1] for ele in posts if ele[1] == 'admin']
        current_year = datetime.now().year
        return {"admin": admin, "current_year": current_year}


def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1),
        UPLOAD_FOLDER=os.path.join(basedir, 'flaskr/uploads')
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

    # 调用环境变量函数
    register_template_context(app)
    login_manager = get_login_manager()
    login_manager.init_app(app)

    # 导入并注册蓝图
    app.register_blueprint(auth.bp)

    app.register_blueprint(admin.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app
