import logging
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    def __init__(self, info_log, error_log, slow_action, level_no, client_identification):
        # create logger
        self.logger = logging.getLogger(client_identification)
        self.logger.setLevel(logging.DEBUG)
        # self.logger.propagate = False

        self.error_handler = TimedRotatingFileHandler(error_log, when='midnight', backupCount=10)
        self.error_handler.setLevel(logging.DEBUG)

        # create slow_query_handler to write slow query log.
        self.slow_action_handler = TimedRotatingFileHandler(slow_action, when='midnight', backupCount=10)
        self.slow_action_handler.setLevel(logging.DEBUG)

        self.info_handler = TimedRotatingFileHandler(info_log, when='midnight', backupCount=10)
        self.info_handler.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(message)s')
        self.error_handler.setFormatter(formatter)
        self.slow_action_handler.setFormatter(formatter)
        self.info_handler.setFormatter(formatter)

    def inside_error(self, message: str):
        self.logger.handlers = list()  # removeHandler移除无效, 必须将处理方法列表置为空才能解决同一日志记录多次写入的问题
        self.logger.addHandler(self.error_handler)
        self.logger.debug(self.inside_error.__name__ + ': ' + str(message), exc_info=True)

    def outside_error(self, message: str):
        self.logger.handlers = list()
        self.logger.addHandler(self.error_handler)
        self.logger.debug(self.outside_error.__name__ + ': ' + str(message), exc_info=True)
        # self.logger.debug(message, stack_info=True)

    def slow_action(self, message: str):
        self.logger.handlers = list()
        self.logger.addHandler(self.slow_action_handler)
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.handlers = list()
        self.logger.addHandler(self.info_handler)
        self.logger.debug(message)

