#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""rabbitmq监控"""
import daemon
import sys
import threading
from configs.config import RUN
from queue_minitor import  minitor as qm #监控队列

if __name__ == "__main__":
	RUN['daemon'] = sys.argv[1]
	print RUN
	daemon.daemon_exec(RUN)
	t = threading.Thread(target=qm.main)
	t.start()
	t.join()