# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/3 17:28
@ Description:
"""
import time

from api_autotest_demo import ConfigUtils


class BaseApi:
	token: str = ''
	header: dict = ConfigUtils.read_base_json().get('header')
	
	def __init__(self,
	             cursor=None,
	             data: dict = ConfigUtils.read_base_json().get('data')):
		self.cursor = cursor
		self.data = data
	
	@staticmethod
	def get_timestamp():
		stamp = time.time()
		return int(stamp * 1000).__str__()
	
	@staticmethod
	def get_base_url() -> str:
		return ConfigUtils.get_url()
	
	@classmethod
	def ensure_url_sep(cls, url: str) -> str:
		return cls.get_base_url() + url
	
	@classmethod
	def get_header(cls) -> dict:
		return cls.header
	
	@classmethod
	def set_header(cls, key, value):
		cls.header[key] = value
	
	@classmethod
	def set_headers(cls, new_header_dict: dict):
		cls.header.update(new_header_dict)
	
	def get_data(self):
		return self.data
	
	def set_data(self, new_data_dict: dict):
		self.data.update(new_data_dict)
	
	@staticmethod
	def get_appid():
		return ConfigUtils.get_appid()
	
	@classmethod
	def get_token(cls):
		return cls.token
	
	@classmethod
	def set_token(cls, token, is_insert_header: bool = True):
		cls.token = token
		if is_insert_header:
			cls.set_header(key='x-auth-token', value=cls.get_token())
