# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/7 9:45
@ Description: 获取用户信息接口
"""
import json

import requests
from api_autotest_demo2.base.base_api import BaseApi


class UserApi(BaseApi):
	
	def get_user_info(self):
		response = requests.get(self.ensure_url_sep('/xxx/url'), headers=self.header)
		user_id = json.loads(response.content).get('data').get('userId')
		return user_id
