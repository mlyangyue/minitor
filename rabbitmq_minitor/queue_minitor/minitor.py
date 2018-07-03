#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""监控rabbitmq队列消息数量是否触发预警阀值和重度积压阀值"""
from configs.config import SETTINGS, CONF_ENV, RUN
import json
import sys
import requests
import urllib
import socket
import logging
import daemon
import time
from LogUtil import addTimedRotatingFileHandler

settings = SETTINGS[CONF_ENV]
logpath = settings.PATH
addTimedRotatingFileHandler(
		filename=logpath + '/minitor.log',
		logLevel = 'INFO',
		backupCount=120,
	)
logger = logging.getLogger()

class Minitor():
	def __init__(self):
		self.vhost = settings.MQ["VHOST"]
		self.host = settings.MQ["HOST"]
		self.port = settings.MQ["PORT"]
		self.username = settings.MQ["USERNAME"]
		self.password = settings.MQ["PASSWORD"]

	def connect(self):
		url = "http://{host}:{port}/api/queues/{vhost}/".format(
			host=self.host,
			port=self.port,
			vhost=urllib.quote(self.vhost, safe=''),
		)
		try:
			r = requests.get(url, auth=(self.username, self.password), timeout=5)
		except socket.error:
			logger.error("UNKNOWN: Could not connnet to %s:%s" % (self.host, self.port))
			return 2
		except Exception as E:
			logger.error("connect error = %s"%E)
			return 2
		status_code = r.status_code
		if status_code > 299:
			logger.error("UNKNOWN: Unexpected API error :%s" % r.content)
			return 3
		return r.content


def main():
	m = Minitor()
	while True:
		resp_payload = json.loads(m.connect())
		for item in resp_payload:
			queue_name = item['name']  # 队列名
			messages_ready = item['messages_ready']  # 准备好的消息数
			msg_cnt_total = item["messages"]
			messages_unacknowledged = item["messages_unacknowledged"]  # 未确认的消息数
			consumers = item["consumers"]
			# print "队列名:{queue_name},准备好的消息数:{messages_ready},消费者数:{consumers},待处理的消息:{msg_cnt_total}".format(
			# 	queue_name=queue_name, messages_ready=messages_ready, consumers=consumers, msg_cnt_total=msg_cnt_total
			# )
			if messages_ready > 1 or consumers < 1:  # 队列准备好的数据大于1或者消费者小于1
				msg = "error 队列名={queue_name} 积压消息数={messages_ready},消费者数量={consumers}".format(
					queue_name = queue_name,
					messages_ready=messages_ready,
					consumers=consumers
				)
				logger.error("%s" % msg)
		time.sleep(3)

if __name__ == "__main__":
	RUN['daemon'] = sys.argv[1]
	print RUN
	daemon.daemon_exec(RUN)
	main()