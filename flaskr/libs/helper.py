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
