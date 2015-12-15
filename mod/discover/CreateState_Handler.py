# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
import json
import time,random
from ..databases.tables import TopicsCache
from mod.auth.Base_Handler import BaseHandler
import time
#/discover/create
class CreateStateHandler(BaseHandler):
	def post(self):#发布动态
		try:
			user_id = self.current_user.uid
			a_topic_title = self.get_argument('topic_title')
			a_topic_content = self.get_argument('topic_content')
			a_topic_pic = self.get_argument('topic_pic')
			a_topic_time = int(time.time())
			if not a_topic_pic:
				a_topic_pic = '/static/sys_pic/%d.jpg' % random.randint(1,12)
			retjson = {'code':200,'content':'ok'}
			try:
				topics = TopicsCache(uid=user_id,topic_title=a_topic_title,\
					topic_content=a_topic_content,topic_pic=a_topic_pic,topic_time=int(time.time()))
				self.db.add(topics)
				
				if a_topic_title and a_topic_content:
					try:
						self.db.commit()
					except:
						self.db.rollback()
						retjson['code'] = 401
						retjson['content'] = u'Database store is wrong!'
				else:
					retjson = {'code':400,'content':'have null parameter '}
	         
			except Exception,e:
				retjson = {'code':400,'content':'failed to create state'}
		except Exception,e:
			retjson = {'code':400,'content':'no parameter'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)
