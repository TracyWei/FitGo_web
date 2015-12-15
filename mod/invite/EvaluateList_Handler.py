# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import Invite_relation,InviteCache
import json,time
#have been tested
class EvaluateListHandler(BaseHandler):
	def get(self):#获取未评价的活动
		retjson = {'code':200,'content':'ok'}
		# arg_uid = self.current_user.uid
		arg_uid = self.get_argument("uid")
		try:
			print arg_uid
			#获得所有作为参与者未评价的项目
			invitation_1 = self.db.execute("select * from Invite_relation where uid_request = %s and comment_state=1 and comment is null and score is null;" % arg_uid).fetchall()
			#获得所有作为发起者未评价的项目
			invitation_2 = self.db.execute("select * from Invite_relation where uid_respond = %s and comment_state=1 and comment is null and score is null;" % arg_uid).fetchall()
			print invitation_1
			print invitation_2
			content = []
			if invitation_1:
				for i in invitation_1:
					content1 = {}
					content1['id'] = i.id
					content1['_id'] = i._id
					content1['fit_item'] = i.fit_item
					print content1
					content.append(content1)
			else:
				if invitation_2:
					for i in invitation_2:
						content1 = {}
						content1['id'] = i.id
						content1['_id'] = i._id
						content1['fit_item'] = i.fit_item
						content.append(content1)
				else:
					retjson = {'code':400,'content':'no comment'}
			retjson['content'] = content
		except Exception, e:
			retjson = {'code':400,'content':'failed to search comment'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)
	def post(self):#获得未评价活动详情
		retjson = {'code':200,'content':'ok'}
		arg_id = self.get_argument("_id")
		try:
			invitation = self.db.execute("select * from Invite where _id = %s;" % arg_id).fetchall()
			print invitation
			content = []
			if invitation:
				for i in invitation:
					content1={}
					content1['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(i.start_time)))
					content1['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(i.end_time)))
					content1['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(i.create_time)))
					content1['fit_location'] = i.fit_location
					content1['fit_item'] = i.fit_item
					content1['item_tag'] = i.item_tag
					content1['gender'] = i.gender
					content1['remark'] = i.remark
					content.append(content1)
			else:
				retjson = {'code':400,'content':'no comment'}
			retjson['content'] = content
		except Exception, e:
			retjson = {'code':400,'content':'failed to search comment'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)

