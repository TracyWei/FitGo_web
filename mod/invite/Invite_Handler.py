# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,Invite_relation
import json,time
#have been tested
#/invite
class InviteHandler(BaseHandler):
	# @tornado.web.authenticated
	def post(self):#发布健身
		retjson = {'code':200,'content':'ok'}
		try:
			print "aa"
			# arg_uid = self.current_user.uid
			# arg_name = self.current_user.name
			arg_uid = self.get_argument("uid")
			arg_name = self.get_argument("name")
			arg_start_time = self.get_argument("start_time")
			arg_end_time = self.get_argument("end_time")
			arg_create_time = int(time.time())
			arg_fit_location = self.get_argument("fit_location")
			arg_fit_item = self.get_argument("fit_item")
			arg_item_tag = self.get_argument("item_tag")
			arg_gender = self.get_argument("gender")
			arg_remark = self.get_argument("remark")#备注
			arg_id = time.time()
			if not arg_uid or not arg_item_tag or not arg_start_time or not arg_end_time:
				retjson['code'] = 400
				retjson['content'] = 'Some arguments are empty'
			else:
				try:
					arg_start_time = int(time.mktime(time.strptime(arg_start_time,"%Y-%m-%d %H:%M")))
					arg_end_time = int(time.mktime(time.strptime(arg_end_time,"%Y-%m-%d %H:%M")))
					status = InviteCache(uid=arg_uid,name=arg_name,start_time=arg_start_time,end_time=arg_end_time,\
						create_time=arg_create_time,fit_location=arg_fit_location,fit_item=arg_fit_item,\
						item_tag=arg_item_tag,gender=arg_gender,remark=arg_remark)
					self.db.add(status)
					try:
						self.db.commit()
					except Exception,e:
						self.db.rollback()
						retjson['code'] = 401
						retjson['content'] = u'Database store is wrong!'
				except Exception, e:
					self.db.rollback()
					retjson['code'] = 401
					retjson['content'] = u'Something bad in database!'
		except Exception,e:
			retjson = {'code':400,'content':'no parameters'}
			
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)