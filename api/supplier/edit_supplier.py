# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/27 14:58
@ Description: 编辑货主
"""
from typing import Literal

from api_autotest_demo2.base.base_api import BaseApi


class EditSupplierApi(BaseApi):
	
	def edit_supplier(self,
	                  supplier_name='',
	                  supplier_mobile='',
	                  supplier_type=1,
	                  supplier_id=None,
	                  mode: Literal['add', 'edit'] = 'add'):
		pass
