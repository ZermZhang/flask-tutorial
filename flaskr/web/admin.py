#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : admin
@Software       : PyCharm
@Modify Time    : 2021/6/23 20:57
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.web.auth import login_required
from flaskr.libs.forms import ArticleForm, PostForm
from flaskr.libs.helper import remove_html_tag
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/admin_index')
@login_required
def admin_index():
    return render_template('admin/admin_index.html')


@bp.route('/admin_create', methods=['GET', 'POST'])
@login_required
def admin_create():
    form = ArticleForm(request.form)
    if form.validate_on_submit():
        article_title = form.title.data
        article_content = form.content.data

        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (article_title, article_content, g.user['id'])
        )
        db.commit()
        return redirect(url_for('blog.index'))
    else:
        print("Something wrong!")
    return render_template('admin/admin_create.html', form=form)


@bp.route('/admin_mdeditor', methods=['POST', 'GET'])
@login_required
def admin_mdeditor():
    form = PostForm(request.form)
    if form.validate_on_submit():
        form.content.data = request.form['markdownEditor-html-code']
        if not form.description.data:
            form.description.data = remove_html_tag(form.content.data)[0: 150]

        if form.publish.data:
            article_title = form.title.data
            article_content = form.content.data

            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (article_title, article_content, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        if form.save.data:
            print("This a save action.")
    else:
        print("Something wrong in form!")

    return render_template('admin/admin_mdeditor.html', form=form)
