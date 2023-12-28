# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/3 11:48
@ Description: 自动化测试运行程序
"""
import os
import time

import pytest

from api_autotest_demo import log

if __name__ == '__main__':
	current_file = os.path.dirname(__file__)
	os.chdir(current_file)
	
	log.info('测试开始', is_file_out=False)
	pytest.main()
	time.sleep(1)
	
	os.system(r"allure generate ./test_reports/temp -o ./test_reports/report --clean")
