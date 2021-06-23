#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : auth
@Software       : PyCharm
@Modify Time    : 2021/6/3 18:08
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.libs.forms import LoginForm


# 创建授权蓝图，url_prefix会添加到所有与蓝图相关代的URL前面
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 关联页面 /register 和函数register
# 当Flask收到一个指向/auth/register的请求时会调用register函数并将返回值作为响应
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            # 保存数据库修改结果
            db.commit()
            # url_for根据登录视图的名称生成相应的URL
            # redirect生成URL的一个重定向
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # 表单校验成功，和表中的值进行验证
        db = get_db()
        user = db.execute(
            'SELECT * from user WHERE username = "{}"'.format(form.username.data)
        ).fetchone()

        if user and check_password_hash(user['password'], form.password.data):
            # 用户名存在并且密码验证通过
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            pass
    return render_template('auth/login.html', form=form)


# 注册一个在视图函数之前运行的函数，不论URL是什么
@bp.before_app_request
def load_logged_in_user():
    """
    检查用户id是否已经存储在session中，并存数据库中湖区用户数据
    """
    user_id = session.get('user_id')

    # 存储在g.user中，g.user的持续时间比请求长
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# 注销的时候将用户id从session中移除
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他的视图中进行验证
def login_required(view):
    # 返回一个新的视图
    # 该视图包含了传递给装饰器的原始图
    # 新视图检查用户是否已载入，如果已载入正常执行，否则重定向到登录页面
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
