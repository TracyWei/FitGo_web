# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler,UsersCache
from ..databases.tables import TopicsCache
from time import mktime,strptime,strftime,time,localtime
from state_like_controller import getLike
import json,string
# from sqlalchemy import func

#/discover/search/state
class SearchStateHandler(BaseHandler):
	def post(self):#搜索动态
		a_topic_title = self.get_argument('topic_title')
		a = a_topic_title
		if a_topic_title:
			try:
				
				topics = self.db.execute("select * from Topics where topic_title like \'%%%s%%\';" % a_topic_title).fetchall()

				
				if topics:
					retjson = {'code':200,'content':'ok'}
					content1 = []
					for n in topics:
						content = {}
						content['uid'] = n.uid
						user = self.db.query(UsersCache).filter(UsersCache.uid == n.uid).one()
						content['name'] = user.name
						content['topics_id'] = n.topic_id
						content['topic_title'] = n.topic_title
						content['topic_content'] = n.topic_content
						content['topic_pic'] = n.topic_pic
						content['pic_shape'] = n.pic_shape
						content['topic_starers'] = getLike(n.topic_id,self.Mongodb())
						content1.append(content)
					retjson['content'] = content1
					# print retjson
				else:
					retjson = {'code':400,'content':'not match topics_title'}
			except Exception,e:
				retjson = {'code':400,'content':'failed to search state'}
		else:
			retjson = {'code':400,'content':'topic_title is null'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		# print ret

		self.render('discover_state.html',content=retjson)