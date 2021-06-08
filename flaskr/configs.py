#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File           : configs
@Software       : PyCharm
@Modify Time    : 2021/6/8 20:12
@Author         : zermzhang
@version        : 1.0
@Desciption     :
"""
import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(BaseConfig):
    """
    开发环境配置类
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


class TestConfig(BaseConfig):
    """
    测试环境配置类
    """
    pass


class ProductionConfig(BaseConfig):
    """
    生产环境配置类
    """
    pass


# 配置类字典，根据传递的 key 选择不同的配置类
configs = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}