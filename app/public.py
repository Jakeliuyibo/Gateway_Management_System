# -*- coding: utf-8 -*-

import json
import  decimal

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return float(o)
		super(DecimalEncoder, self).default(o)


#公共接口返回
def amis_ret(data,status=0,msg='',errors={}):
	if status==0 and msg=='':
		msg='请求成功'
	elif status==1 and msg=='':
		msg='请求失败'
	t={}
	t['status']=status
	t['msg']=msg
	t['data']=data
	if errors:
		#表单验证
		t['errors']=errors
		t['status']=422
		t['msg']='验证错误'
		pass
	return json.dumps(t,ensure_ascii=False,cls=DecimalEncoder)

