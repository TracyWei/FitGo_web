# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler
from ..databases.tables import ActCache
import json
import random
from config import icon
import json,string
from time import mktime,strptime,strftime,time,localtime
from ActivityController import getJoinUid
#/activity/search/
class SearchActivityHandler(BaseHandler):
	def post(self):#搜索活动
		a_act_title = self.get_argument("act_title")
		a_start_time = self.get_argument("start_time")
		a_location = self.get_argument("location")
		string = ''
		retjson = {'code':200,'content':'ok'}
		
		try:
			if a_act_title:
				string = string + 'act_title like \'%%%s%%\'' % a_act_title + ' and '
			if a_start_time:
				a_start_time = int(mktime(strptime(a_start_time,"%Y-%m-%d")))
				string = string + 'start_time=\'%s\'' % a_start_time + ' and '
			if a_location:
				string = string + 'act_location=\'%s\'' % a_location + ' and '

			if string.strip()=='':
				retjson = {'code':400,'content':'all parameters are null'}
			else:
				length0 = len(string)
				length = length0 - 5
				string = string[0:length]
				activitys = self.db.execute("select * from Act where %s;" % string).fetchall()
				if activitys:
					content1 = []
					for n in activitys:
						content = {}
						content['uid'] = n.uid
						content['id'] = n.act_id
						content['title'] = n.act_title
						content['start'] = strftime("%Y-%m-%d",localtime(int(n.start_time)))
						content['end'] = strftime("%Y-%m-%d",localtime(int(n.end_time)))
						content['location'] = n.act_location
						content['detail'] = n.act_detail
						content['create_time'] = strftime("%Y-%m-%d",localtime(int(n.create_time)))
						content['join_uid'] = getJoinUid(n.act_id,self.Mongodb())
						content1.append(content)
					retjson['content'] = content1
				else:
					retjson = {'code':400,'content':'not match activity'}
		except Exception, e:
			retjson = {'code':400,'content':'failed to search activity'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		num = []
		length = len(retjson['content'])
		for i in range(length):
			num.append(random.randint(0, 4))
		self.render('activity_item.html',ret=retjson,icon=icon,num=num)
		# self.write(ret)
