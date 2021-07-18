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
import json
import os
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, Response
)

from flaskr.web.auth import login_required
from flaskr.web.blog import get_post
from flaskr.libs.forms import ArticleForm, PostForm, NewCatrgoryForm
from flaskr.libs.helper import remove_html_tag, get_form_error_items
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


@bp.route('/admin_categories', methods=['POST', 'GET'])
@login_required
def admin_categories():
    form = NewCatrgoryForm(request.form)
    print(form)
    fields_names, fields_errors = get_form_error_items(form)
    print(fields_names)
    print(fields_errors)
    return render_template('admin/admin_categories.html', form=form,
                           fields_errors=fields_errors,
                           fields_names=fields_names)


@bp.route('/admin_articles', methods=['POST', 'GET'])
@login_required
def admin_articles():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, created'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('admin/admin_articles.html', posts=posts)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def admin_update(id):
    post = get_post(id)

    form = PostForm(request.form)

    if form.validate_on_submit():
        form.content.data = request.form['markdownEditor-html-code']
        if not form.description.data:
            form.description.data = remove_html_tag(form.content.data)[0:150]

        if form.publish.data:
            article_title = form.title.data
            article_content = form.content.data
            ori_md_body =request.form['markdownEditor-markdown-doc']

            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, md_body = ?'
                ' WHERE id = ?',
                (article_title, article_content, ori_md_body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

        if form.save.data:
            print('This is a saveaction.')
    return render_template('admin/admin_update.html', post=post, form=form)


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
                'INSERT INTO post (title, body, md_body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (article_title, article_content, form.content_markdown.data, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        if form.save.data:
            print("This a save action.")
    else:
        print("Something wrong in form!")

    return render_template('admin/admin_mdeditor.html', form=form)


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        res = {
            'success': 1,
            'message': '上传成功',
            'url': url_for('admin.uploaded_image', name=filename)
        }
    return jsonify(res)


@bp.route('/uploaded_image/<name>')
@login_required
def uploaded_image(name):
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], name), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp
