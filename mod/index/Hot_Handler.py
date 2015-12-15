# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,UsersCache
import json,time,string
import traceback

class HotHandler(BaseHandler):
	def get(self):
		retjson = {'code':200,'content':{
								'invite':[],
								'act':[],
								'topics':[]

		}}
		time_now=time.time()
		sql_invite = "select * from Invite where start_time >= %s order by start_time desc limit 2;" % str(time_now)
		sql_act = "select *from Act where start_time >= %s order by start_time desc limit 1;" % str(time_now)
		sql_topics = "select * from Topics order by topic_time desc limit 3;"
		try:
			contentall1=[]
			invitations=self.db.execute(sql_invite).fetchall()
			for i in invitations:
				content={}
				content['start_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.start_time)))
				content['fit_item'] = i.fit_item
				content['user_tag'] = i.user_tag
				content['remark'] = i.remark
				content['location'] = i.fit_location
				contentall1.append(content)
			retjson['content']['invite']=contentall1

			contentall2=[]
			activities=self.db.execute(sql_act).fetchall()
			for n in activities:
				content={}
				content['title'] = n.act_title
				content['start'] = time.strftime("%Y-%m-%d",time.localtime(int(n.start_time)))
				content['detail'] = n.act_detail
				content['act_location'] = n.act_location
				contentall2.append(content)
			retjson['content']['act']=contentall2

			contentall3=[]
			activities=self.db.execute(sql_topics).fetchall()
			for n in activities:
				content={}
				content['topic_time'] = time.strftime("%Y-%m-%d",time.localtime(int(n.topic_time)))
				content['topic_content'] = n.topic_content
				content['topic_title'] = n.topic_title
				contentall3.append(content)
			retjson['content']['topics']=contentall3
			
		except Exception, e:
			retjson['code'] = 401
			retjson['content'] = u'Nothing found!Please try other conditions'
			
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)