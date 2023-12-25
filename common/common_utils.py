# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/3 11:33
@ Description: 公共工具类
"""
import os

from functools import wraps

from typing import Text


class CommonUtils:
	base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	
	@classmethod
	def ensure_path_sep(cls, path: Text) -> Text:
		"""
		绝对路径追加地址
		:param path: 需要追加的地址
		:return: 与base_path连接组成的实际地址(绝对路径表示)
		"""
		"""兼容windows和linux的路径格式"""
		if "/" in path:
			path = os.sep.join(path.split("/"))
		
		if "\\" in path:
			path = os.sep.join(path.split("\\"))
		return cls.base_path + path
	
	@classmethod
	def int_to_str3(cls, num_str: str) -> str:
		while len(num_str) < 3:
			num_str = '0' + num_str
		return num_str
	
	@staticmethod
	def singleton(func):
		"""
		单例装饰器，被其修饰的函数会返回单例对象
		:param func: 被修饰的函数
		:return: 语法糖修饰，则会返回同名函数，该函数已经具有生成单例对象的功能
		"""
		__instance = dict()
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			if func not in __instance:
				__instance[func] = func(*args, **kwargs)
			return __instance[func]
		
		return wrapper


if __name__ == '__main__':
	print(CommonUtils.int_to_str3('10'))
