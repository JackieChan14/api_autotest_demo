# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/6 16:48
@ Description: 测试用例文件
"""

import allure
import faker
import pytest

from api_autotest_demo import CommonUtils
from api_autotest_demo.api import *


@allure.epic('xxx')
@allure.feature('xxx项目接口自动化测试用例')
class TestCases:
	fk = faker.Faker(locale='zh_CN')
	
	@pytest.mark.run(order=1)
	@allure.story('登录用例')
	@allure.title('执行登录操作，返回token')
	def test_login(self):
		la = LoginApi()
		token = la.login('username', 'captcha')
		la.set_token(token)
	
	@pytest.mark.run(order=2)
	@allure.story('用户用例')
	@allure.title('获取用获取用户信息，将userid赋值给请求头信息')
	def test_get_user_info(self):
		ua = UserApi()
		user_id = ua.get_user_info()
		ua.set_header('userid', user_id)
	
	@pytest.mark.run(order=3)
	@allure.story('业务用例')
	@allure.title('新增店铺')
	@pytest.mark.skip('店铺新增完毕，跳过执行')
	def test_edit_store(self):
		esa = EditStoreApi()
		for i in range(1, 600):
			esa.edit_store(contact_name=self.fk.name(),
			               contact_mobile=self.fk.phone_number(),
			               store_name=f'测试店铺{CommonUtils.int_to_str3(i.__str__())}')
	
	@pytest.mark.run(order=4)
	@allure.story('权限用例')
	@allure.title('获取店铺权限，将xx_id和yy_id赋值给请求头')
	def test_list_staff_store(self):
		lsa = ListStoreApi()
		xx_id, yy_id = lsa.switch_store(store_name='店铺名称')
		lsa.set_headers({'xx_id': xx_id, 'yy_id': yy_id})
	
	@pytest.mark.run(order=5)
	@allure.story('进货用例')
	@allure.title('向店铺进货')
	def test_buy_stock(self, cursor):
		res = cursor.execute('xxx_sql')
		...
