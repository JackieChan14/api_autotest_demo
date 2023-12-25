# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/11/16 17:31
@ Description: 计算器工具
"""
from decimal import ROUND_HALF_UP, Decimal


class CalcUtils(Decimal):
	
	@staticmethod
	def add(*args) -> Decimal:
		res = Decimal('0')
		for arg in args:
			res = res.__add__(Decimal(arg.__str__()))
		return res
	
	@staticmethod
	def sub(*args) -> Decimal:
		res = Decimal(args[0].__str__())
		for arg in args[1:]:
			res = res.__sub__(Decimal(arg.__str__()))
		return res
	
	@staticmethod
	def mul(*args) -> Decimal:
		res = Decimal('1')
		for arg in args:
			res = res.__mul__(Decimal(arg.__str__()))
		return res.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
	
	@staticmethod
	def div(*args) -> Decimal:
		if 0 in args:
			raise ZeroDivisionError('参数不能有0')
		res = Decimal(args[0].__str__())
		for arg in args[1:]:
			res = res.__truediv__(Decimal(arg.__str__()))
		return res.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)


if __name__ == '__main__':
	calc = CalcUtils()
	print(calc.mul(132, 0.1))
	print(132 * 0.1)
