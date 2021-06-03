#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : setup.py
@Software       : PyCharm
@Modify Time    : 2021/6/3 19:44
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
