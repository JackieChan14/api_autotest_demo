# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/6 15:02
@ Description: conftest配置文件
"""
import os
import sys
import time

import pymysql
import pytest
from _pytest.terminal import TerminalReporter

from api_autotest_demo import ConfigUtils, log

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
cursor = None


@pytest.fixture(scope='session', name='cursor')
def mysql_conn():
	mysql_config = ConfigUtils.get_mysql()
	conn = pymysql.connect(**mysql_config)
	global cursor
	cursor = conn.cursor()
	
	yield cursor
	
	conn.commit()
	
	cursor.close()
	conn.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
	outcome = yield
	rep = outcome.get_result()
	if rep.when == "call" and rep.failed:
		mode = 'a' if os.path.exists('failure') else 'w'
		with open('failure', mode) as f:
			extra = f'{item.funcargs["tmpdir"]}' if 'tmpdir' in item.fixturenames else ''
			f.write(rep.nodeid + extra + '\t' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
	
	function_name = item.function.__name__[5:]
	if rep.when == 'call':
		if rep.outcome == 'passed':
			log.info(f'用例{function_name}执行成功')
		if rep.outcome == 'failed':
			log.error(f'用例{function_name}执行失败')
		if rep.outcome == 'error':
			log.waring(f'用例{function_name}执行异常')
	
	if rep.outcome == 'skipped':
		log.waring(f'用例{function_name}跳过执行')


def pytest_terminal_summary(terminalreporter: TerminalReporter):
	"""
	收集测试结果，记录测试结果并打入日志
	"""
	_PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
	_ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
	_FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
	_SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
	_TOTAL = getattr(terminalreporter, '_numcollected')
	_TIMES = time.time() - getattr(terminalreporter, '_sessionstarttime')
	
	log.info(f'用例总数: {_TOTAL}', is_file_out=False)
	log.info(f"成功用例数: {_PASSED}")
	log.error(f"失败用例数: {_FAILED}")
	log.waring(f"异常用例数: {_ERROR}")
	log.waring(f"跳过用例数: {_SKIPPED}")
	log.info(f"用例执行时长: {_TIMES:.2f}s", is_file_out=False)
	
	try:
		_RATE = _PASSED / _TOTAL * 100
		log.info(f"用例成功率: {_RATE:.2f}%", is_file_out=False)
	except ZeroDivisionError:
		log.info("用例成功率: 0.00 %", is_file_out=False)
	finally:
		log.info('本次用例执行完毕', is_file_out=False)
		log.info('=' * 30, is_file_out=False)
