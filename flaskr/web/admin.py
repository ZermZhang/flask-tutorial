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

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/admin_index')
@login_required
def admin_index():
    return render_template('admin/admin_index.html')
