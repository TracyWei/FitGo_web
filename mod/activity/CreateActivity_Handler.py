# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler
from ..databases.tables import ActCache
import traceback
import time
import json
#/activity/create
class CreateActivityHandler(BaseHandler):
	"""
	post函数：
		功能：
			用户发起活动
		参数：
			活动所需参数
		返回：
			发起活动状态表示是否成功插入
	"""
	def post(self):#发起活动
		retjson = {'code':200,'content':'ok'}
		try:
			user_id = self.get_argument("uid")
			a_act_title = self.get_argument("act_title")
			a_start_time = self.get_argument("start_time")
			a_end_time = self.get_argument("end_time")
			a_location = self.get_argument("location")
			a_details = self.get_argument("details")
			if a_act_title and a_start_time and a_end_time and a_location and a_details:
				try:
					a_start_time = int(time.mktime(time.strptime(a_start_time,"%Y-%m-%d")))
					a_end_time = int(time.mktime(time.strptime(a_end_time,"%Y-%m-%d")))
					activity = ActCache(uid=user_id,act_title=a_act_title,\
						start_time=a_start_time,end_time=a_end_time,act_location=a_location,act_detail=a_details,create_time=int(time.time()))
					self.db.add(activity)
					try:
						self.db.commit()
					except:
						self.db.rollback()
						retjson['code'] = 401
						retjson['content'] = u'Database store is wrong!'
				except Exception,e:
					retjson['code'] = 400
					retjson['content'] = 'failed to create activity'
			else:
				retjson['code'] = 400
				retjson['content'] = 'have null parameter'
			
		except Exception,e:
			retjson['code'] = 400
			retjson['content'] = 'Parameter Lack'
		self.write(json.dumps(retjson,ensure_ascii=False, indent=2))