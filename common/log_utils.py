# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/17 17:01
@ Description: 日志工具类
"""

import logging
import os
import time
from logging import handlers
from typing import Literal

import colorlog

from api_autotest_demo import CommonUtils


class LogUtils:
	"""
    日志类，定制化生成日志
    """
	# 传入的level参数与日志等级的映射关系
	level_relations = {
		"debug": logging.DEBUG,
		"info": logging.INFO,
		"warning": logging.WARNING,
		"error": logging.ERROR,
		"critical": logging.CRITICAL
	}
	
	# 日志等级和颜色的映射关系，只适用于控制台输出的格式控制
	log_colors_config = {
		'DEBUG': 'cyan',
		'INFO': 'green',
		'WARNING': 'yellow',
		'ERROR': 'red',
		'CRITICAL': 'pink'
	}
	
	# 以当天日期划分文件输入日志的名称，由年月组成分组包，年-月-日组成每天的日志
	now = time.localtime(time.time())
	_TODAY = time.strftime("%Y-%m-%d", now)
	_MONTH = time.strftime("%Y%m", now)
	
	def __init__(self, log_name=f'{_TODAY}.log', level='info', when='MIDNIGHT', backup_days=3,
	             fmt="%(asctime)s\t%(levelname)s\t%(funcName)s --- [%(processName)s]\t%(name)s\t: %(message)s",
	             encoding='utf-8', is_output=True, is_file_out=True):
		"""
		:param log_name: 日志生成器名称
		:param level: 日志等级
		:param when: 日志区分单位，MIDNIGHT表示每天生成不同的日志文件
		:param backup_days: 最多存在几次的日志，默认为3，则最多同时存在3天的日志
		:param fmt: 日志基础格式
		:param encoding: 日志文件编码格式
		:param is_output: 是否输出到控制台
		:param is_file_out: 是否输出到文件
		"""
		
		# 日志保存的完整路径
		full_path = CommonUtils.ensure_path_sep(f'/log/{self._MONTH}/{self._TODAY}')
		
		# 初始化日志器和处理器
		self.logger = logging.getLogger(log_name)
		self.logger.setLevel(self.level_relations[level])
		
		self.stream_handler = None
		self.time_handler = None
		
		# 如果今天的日志不存在就新增
		if not os.path.exists(full_path):
			os.makedirs(full_path)
		log_path = os.path.join(full_path, log_name)
		
		if is_output:
			self.stream_handler = logging.StreamHandler()
			# 控制台输入的日志需要加入颜色区分的格式
			s_handler_format = colorlog.ColoredFormatter(fmt=f'%(log_color)s{fmt}', log_colors=self.log_colors_config)
			self.stream_handler.setFormatter(s_handler_format)
			self.logger.addHandler(self.stream_handler)
		
		if is_file_out:
			self.time_handler = handlers.TimedRotatingFileHandler(filename=log_path, when=when, backupCount=backup_days, encoding=encoding)
			# TimedRotating文件输入的日志不加颜色区分
			t_handler_format = logging.Formatter(fmt=fmt)
			self.time_handler.setFormatter(t_handler_format)
			self.logger.addHandler(self.time_handler)
		
		if not is_output and not is_file_out:
			raise ValueError("控制台和文件日志输入不能同时为False")
	
	@classmethod
	@CommonUtils.singleton
	def get_singleton_logger(cls, level: Literal['info', 'error', 'warning']):
		"""
		生成单例模式的Logger实例对象，主要是往每天的总日志文件里输出日志
		:param level: 日志等级，暂时只能从info, error和waring中取值
		:return: 生成单例对象，将不同等级的日志打入同一个文件
		"""
		return cls(level=level, is_output=False)
	
	@classmethod
	def get_logger(cls, level: Literal['info', 'error', 'warning'], is_output=True, is_file_out=True):
		"""
		生成非单例模式的Logger实例对象，主要用于分别往每天的info,warning和error分日志里以及控制台输出日志
		:param level: 只能从info, error和waring中取值
		:param is_output: 是否打在控制台
		:param is_file_out: 是否打入文件
		:return: 不同等级的Logger对象，用于分别将不同等级的日志打入不同的文件
		"""
		return cls(level=level, log_name=f'{cls._TODAY}-{level}.log', is_output=is_output, is_file_out=is_file_out)


class Log:
	@staticmethod
	def print_log(level: Literal['info', 'error', 'warning'], content: str, is_output: bool = True, is_file_out: bool = True):
		"""
		给指定的handler输入日志
		:param level: 日志级别
		:param content: 日志内容
		:param is_output: 是否输入在控制台
		:param is_file_out: 是否输入文件
		:return: None
		"""
		# 非单例日志对象
		log_obj = LogUtils.get_logger(level, is_output=is_output, is_file_out=is_file_out)
		# 单例日志对象
		log_single_obj = LogUtils.get_singleton_logger(level)
		
		if hasattr(log_obj.logger, level) and hasattr(log_single_obj.logger, level):
			getattr(log_obj.logger, level)(content)
			getattr(log_single_obj.logger, level)(content)
		
		# 此步非常重要，非单例的Logger对象需要在每次打完日志之后及时解绑stream_handler和time_handler，避免重复加载handler，出现重复打日志的现象
		log_obj.logger.removeHandler(log_obj.stream_handler)
		log_obj.logger.removeHandler(log_obj.time_handler)
	
	def debug(self, content: str, is_output: bool = True, is_file_out: bool = True):
		raise AttributeError('暂不支持debug级别的日志')
	
	def info(self, content: str, is_output: bool = True, is_file_out: bool = True):
		self.print_log('info', content, is_output, is_file_out)
	
	def waring(self, content: str, is_output: bool = True, is_file_out: bool = True):
		self.print_log('warning', content, is_output, is_file_out)
	
	def error(self, content: str, is_output: bool = True, is_file_out: bool = True):
		self.print_log('error', content, is_output, is_file_out)
	
	def critical(self, content: str, is_output: bool = True, is_file_out: bool = True):
		raise AttributeError('暂不支持critical级别的日志')


log = Log()
