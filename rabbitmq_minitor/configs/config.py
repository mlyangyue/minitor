#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""连接rabbitmq的配置地址"""
CONF_ENV = "produce"

class BaseConfig():
	MQ = {
		"HOST": "127.0.0.1",
		"PORT": 5672,
		"USERNAME": "guest",
		"PASSWORD": "guest",
	}
	QUEUE_MINITOR = {
		# 队列名:{waring:int,error:int}
		"third_platform_push_messages_htg":{"waring":10,"error":20}
	}


class LocalConfig(BaseConfig):
	MQ = {
		"HOST": "127.0.0.1",
		"PORT": 5672,
		"VHOST":"/",
		"USERNAME": "guest",
		"PASSWORD": "guest",
	}


class TestConfig(BaseConfig):
	MQ = {
		"HOST": "192.168.1.11",
		"PORT": 15672,
		"VHOST":"/",
		"USERNAME": "rabbitmq",
		"PASSWORD": "admin@123",
	}


class ProduceConfig(BaseConfig):
	MQ = {
		"HOST": "192.168.6.78",
		"PORT": 15672,
		"VHOST":"/",
		"USERNAME": "rabbitmq",
		"PASSWORD": "s2UUehpWNDv6yhWCp",
	}
	PATH = "/Users/wangranming/log"
SETTINGS = {
	'produce': ProduceConfig,
	'test': TestConfig,
	'local': LocalConfig,
}

RUN = {'daemon' : 'start', 'pid-file' : './minitor.pid', 'log-file' : './minitor.log'}

RUNING_CONFIG = CONF_ENV