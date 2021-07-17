#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : helper
@Software       : PyCharm
@Modify Time    : 2021/7/6 08:46
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
import re


def remove_html_tag(html_str):
    regex = re.compile('<[^>]*>')
    return regex.sub('', html_str).replace('\n', '').replace('\r', '').replace(' ', '')


def get_form_error_items(form):
    """
    获取表单验证失败的字段名称及错误信息
    :param form: 表单类实例
    :return: 验证失败的字段名称列表和错误信息列表组成的元祖
    """
    form_error_items = form.errors.items()
    fields_name = []
    fields_errors = []
    if form_error_items:
        for field_name, errors in form_error_items:
            fields_name.append(field_name)
            fields_errors += errors
    return fields_name, fields_errors