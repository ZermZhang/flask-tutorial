#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : forms
@Software       : PyCharm
@Modify Time    : 2021/6/10 19:25
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired('用户名不能为空'),
            Length(3, 10, message='用户名应该在3到10字符之间')
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired('密码不能为空'),
            Length(8, 24, message='密码应在 8 到 24 个字符之间')
        ]
    )
    remeber = BooleanField()
