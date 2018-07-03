#coding=utf8
import os
import logging
import logging.handlers


def addTimedRotatingFileHandler(filename, **kwargs):
    """给logger添加一个时间切换文件的handler。
    默认时间是0点，30个备份。如果不指定logger，则使用logging.getLogger()，也就是RootLogger。
    """
    dname = os.path.dirname(filename)
    if dname and not os.path.isdir(dname):
        os.makedirs(dname, 0755)
    conf = {
        'when': 'midnight',
        'backupCount': 30,
        'format': '[%(asctime)s][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
        'logger': logging.getLogger(),
    }
    conf.update(kwargs)
    if conf.has_key('logLevel'):
        if isinstance(conf['logLevel'], str):
            conf['logLevel'] = getattr(logging, conf['logLevel'])
        conf['logger'].setLevel(conf['logLevel'])
    handler = logging.handlers.TimedRotatingFileHandler(
        filename = filename,
        when = conf['when'],
        backupCount = conf['backupCount'],
    )
    handler.setFormatter(
        logging.Formatter(conf['format'])
    )
    conf['logger'].addHandler(handler)


def addRotatingFileHandler(filename, **kwargs):
    """给logger添加一个大小切换文件的handler。
    默认大小是10M，30个备份。如果不指定logger，则使用logging.getLogger()，也就是RootLogger。
    """
    dname = os.path.dirname(filename)
    if dname and not os.path.isdir(dname):
        os.makedirs(dname, 0755)
    conf = {
        'maxBytes': 1024 * 1024 * 100,
        'backupCount': 30,
        'format': '[%(asctime)s][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
        'logger': logging.getLogger(),
    }
    conf.update(kwargs)
    if conf.has_key('logLevel'):
        if isinstance(conf['logLevel'], str):
            conf['logLevel'] = getattr(logging, conf['logLevel'])
        conf['logger'].setLevel(conf['logLevel'])
    handler = logging.handlers.RotatingFileHandler(
        filename = filename,
        maxBytes = conf['maxBytes'],
        backupCount = conf['backupCount'],
    )
    handler.setFormatter(
        logging.Formatter(conf['format'])
    )
    conf['logger'].addHandler(handler)
    
def addNoRotatingFileHandler(filename, **kwargs):
    """给logger添加一个没有日志轮转的handler。
    
    用于多进程写同一日志，轮转出现问题情况
    适用于日志记录内容比较少的情况
    """
    dname = os.path.dirname(filename)
    if dname and not os.path.isdir(dname):
        os.makedirs(dname, 0755)
    conf = {
        'format': '[%(asctime)s][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
        'logger': logging.getLogger(),
    }
    conf.update(kwargs)
    if conf.has_key('logLevel'):
        if isinstance(conf['logLevel'], str):
            conf['logLevel'] = getattr(logging, conf['logLevel'])
        conf['logger'].setLevel(conf['logLevel'])
    handler = logging.FileHandler(
        filename = filename
    )
    handler.setFormatter(
        logging.Formatter(conf['format'])
    )
    conf['logger'].addHandler(handler)
