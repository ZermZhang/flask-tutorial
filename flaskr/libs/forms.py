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
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
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
            Length(3, 24, message='密码应在 8 到 24 个字符之间')
        ]
    )
    remember = BooleanField()


class ArticleForm(FlaskForm):
    title = StringField(
        validators=[DataRequired('文章名不能为空')]
    )

    content = StringField(
        validators=[DataRequired('文章内容不能为空')]
    )


class PostForm(FlaskForm):
    """
    通过markdown编辑和提交文章
    """
    title = StringField(
        validators=[
            DataRequired(u'标题不能为空'),
            Length(max=60, message=u'标题不要超过60个字符')
        ]
    )
    content_markdown = TextAreaField()
    content = TextAreaField()
    # categories = SelectMultipleField(
    #     validators=[
    #         DataRequired(u'必须选择一个分类')
    #     ],
    #     coerce=int
    # )
    can_comment = BooleanField(label=u'允许评论')
    description = TextAreaField(
        validators=[
            Length(max=150, message=u'描述信息不要超过150个字符')
        ]
    )
    publish = SubmitField(u'发布')
    save = SubmitField(u'保存为草稿')


class NewCatrgoryForm(FlaskForm):
    name = StringField(validators=[
        DataRequired("分类名不能为空"),
        Length(max=12, message="分类名最长不能超过12个字符")
    ])
    alias = StringField(validators=[
        Length(max=24, message="别名最长不超过24个字符")
    ])
    show = BooleanField()
