#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : extensions
@Software       : PyCharm
@Modify Time    : 2021/6/10 19:34
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
from flask_login import LoginManager
from flaskr.db import get_db


def get_login_manager():
    login_manager = LoginManager()

    @login_manager.user_loader
    def get_user(uid):
        db_cursor = get_db()
        posts = db_cursor.execute('SELECT id, username from user').fetchall()
        admin = [ele[1] for ele in posts if ele[1] == 'admin']
        return admin

    login_manager.login_view = 'web.login'
    login_manager.login_message = '无法访问页面，请先登录'
    login_manager.login_message_category = 'error'

    return login_manager
