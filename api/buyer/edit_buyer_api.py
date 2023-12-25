# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/9 11:26
@ Description: 新增买家
"""
from typing import Literal

from api_autotest_demo2.base.base_api import BaseApi


class EditBuyerApi(BaseApi):
	
	def edit_buyer(self,
	               buyer_name: str,
	               buyer_mobile: str = None,
	               remark: str = None,
	               mode: Literal['add', 'edit'] = 'add',
	               buyer_id: str = None):
		pass
