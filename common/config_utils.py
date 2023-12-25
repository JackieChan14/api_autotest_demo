# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/6 15:05
@ Description: 获取配置文件
"""
import json

from api_autotest_demo2.common.common_utils import CommonUtils
from api_autotest_demo2.common.yaml_utils import YamlUtils


class ConfigUtils:
	config = YamlUtils.read_yaml(CommonUtils.ensure_path_sep('/conf/base_url.yml'))
	
	@classmethod
	def get_url(cls) -> str:
		url = ''
		if hasattr(cls.config, 'get'):
			url = cls.config.get('url').get(cls.get_env())
		return url
	
	@classmethod
	def get_mysql(cls) -> dict:
		mysql_config = dict()
		if hasattr(cls.config, 'get'):
			mysql_config.update(cls.config.get('mysql').get(cls.get_env()))
		return mysql_config
	
	@classmethod
	def get_appid(cls) -> str:
		app_id = ''
		if hasattr(cls.config, 'get'):
			app_id = cls.config.get('appid').get(cls.get_env())
		return app_id
	
	@staticmethod
	def get_base_json_path():
		return CommonUtils.ensure_path_sep('/conf/base_info.json')
	
	@classmethod
	def read_base_json(cls, encoding='utf-8') -> dict:
		with open(cls.get_base_json_path(), encoding=encoding) as f:
			return json.loads(f.read())
	
	@classmethod
	def get_env(cls) -> str:
		return cls.read_base_json().get('env')


if __name__ == '__main__':
	print(ConfigUtils.get_mysql())
	print(ConfigUtils.get_base_json_path())
	print(ConfigUtils.get_env())
