#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----description---------
# create new log level
# 创建新的log级别
# logger RotatingFile file
# 限定日志文件大小
# log pre frame
# 打印调用日志的函数/文件/行号
# -----description---------
import logging
import logging.handlers

import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


# write log to file when write log to mongo
LOG_TO_FILE = True
LOG_FILE = "/var/log/log.log"
TRACE_LOG_FILE = "/var/log/trace.log"
# log keys
# priority
LOG_KEYWORD_PRIORITY = "priority"
# result
LOG_KEYWORD_RESULT = "result"
# message
LOG_KEYWORD_MESSAGE = "message"
# module
LOG_KEYWORD_MODULE = "module"
# category
LOG_KEYWORD_CATEGORY = "category"
# create time
LOG_KEYWORD_CREATED = "created"
# log priority keys
LOG_PRIORITY_EMERG = 0
LOG_PRIORITY_ALERT = 1
LOG_PRIORITY_CRIT = 2
LOG_PRIORITY_ERR = 3
LOG_PRIORITY_WARNING = 4
LOG_PRIORITY_NOTICE = 5
LOG_PRIORITY_INFO = 6
LOG_PRIORITY_DEBUG = 7
LOG_PRIORITY_TRACE = 8
logging.addLevelName(LOG_PRIORITY_TRACE, 'TRACE')


FLOG_Handle = None
LOG_Handle = None
MLOG_Handle = None
TRACE_Handle = None


class Log:

    def __init__(self):
        # log to file when LOG_TO_FILE is True
        global FLOG_Handle, TRACE_Handle
        if FLOG_Handle:
            self.logger = FLOG_Handle
        else:
            logger_name = "SuperMC"
            file_logger = logging.getLogger(logger_name)
            file_logger.setLevel(logging.DEBUG)
            fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10000000, backupCount=1)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fh.setFormatter(formatter)
            file_logger.addHandler(fh)
            FLOG_Handle = file_logger
            self.logger = FLOG_Handle
        if TRACE_Handle:
            self.tracer = TRACE_Handle
        else:
            trace_logger = logging.getLogger("TRACE")
            trace_logger.setLevel(1)
            tfh = logging.handlers.RotatingFileHandler(TRACE_LOG_FILE, maxBytes=100000000, backupCount=2)
            tfh.setLevel(1)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            tfh.setFormatter(formatter)
            trace_logger.addHandler(tfh)
            TRACE_Handle = trace_logger
            self.tracer = TRACE_Handle

    def log(self, msg, priority, category, module, result):
        superior_frame = sys._getframe().f_back
        program_name_list = ["trace", "log", "debug", "info", "notice", "warn", "error", "alert", "emerg"]
        while superior_frame.f_code.co_name in program_name_list:
            superior_frame = superior_frame.f_back
        superior_frame_info = ">>> %s %s %s : " % (
            superior_frame.f_code.co_name, superior_frame.f_code.co_filename, superior_frame.f_lineno)
        message = superior_frame_info + '''%s:%s,%s:%s,%s:%s,%s:%s,%s:%s,''' % (
            LOG_KEYWORD_PRIORITY, priority, LOG_KEYWORD_RESULT, result, LOG_KEYWORD_MESSAGE, msg,
            LOG_KEYWORD_MODULE, module, LOG_KEYWORD_CATEGORY, category)
        if priority == LOG_PRIORITY_TRACE:
            self.tracer.log(LOG_PRIORITY_TRACE, message)
        elif priority == LOG_PRIORITY_DEBUG:
            self.logger.debug(message)
        elif priority >= LOG_PRIORITY_NOTICE:
            self.logger.info(message)
        elif priority == LOG_PRIORITY_WARNING:
            self.logger.warn(message)
        elif priority == LOG_PRIORITY_ERR:
            self.logger.error(message)
        else:
            self.logger.critical(message)

    def trace(self, trace_switch, msg, *args, **kwargs):
        if version_print(trace_switch):
            superior_frame = sys._getframe().f_back
            while superior_frame.f_code.co_name == "trace":
                superior_frame = superior_frame.f_back
            superior_frame_info = ">>> %s %s %s : " % (
                superior_frame.f_code.co_filename, superior_frame.f_lineno, superior_frame.f_code.co_name)
            self.tracer.log(LOG_PRIORITY_TRACE, superior_frame_info + msg + '\n', *args, **kwargs)

    def debug(self, msg, category, module, result, priority=LOG_PRIORITY_DEBUG):
        self.log(msg, priority, category, module, result)

    def info(self, msg, category, module, result, priority=LOG_PRIORITY_INFO):
        self.log(msg, priority, category, module, result)

    def notice(self, msg, category, module, result, priority=LOG_PRIORITY_NOTICE):
        self.log(msg, priority, category, module, result)

    def warn(self, msg, category, module, result, priority=LOG_PRIORITY_WARNING):
        self.log(msg, priority, category, module, result)

    def error(self, msg, category, module, result, priority=LOG_PRIORITY_ERR):
        self.log(msg, priority, category, module, result)

    def crit(self, msg, category, module, result, priority=LOG_PRIORITY_CRIT):
        self.log(msg, priority, category, module, result)

    def alert(self, msg, category, module, result, priority=LOG_PRIORITY_ALERT):
        self.log(msg, priority, category, module, result)

    def emerg(self, msg, category, module, result, priority=LOG_PRIORITY_EMERG):
        self.log(msg, priority, category, module, result)

