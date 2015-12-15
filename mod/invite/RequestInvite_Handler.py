# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,Invite_relation
import json,time
#/invite/request
class RequestInviteHandler(BaseHandler):
	# @tornado.web.authenticated
	def post(self):#发送请求
		arg_uid_request = self.current_user.uid
		arg_uid_respond = self.get_argument('uid')
		retjson = {'code':200,'content':'ok'}
		arg_id = self.get_argument('_id')
		id_save = Invite_relation(uid_request=arg_uid_request,_id = arg_id,state = '0',uid_respond = arg_uid_respond)
		#0->not defination 1->ok  2->refuse
		self.db.add(id_save)
		try:
			self.db.commit()
		except Exception, e:
			self.db.rollback()
			retjson['code'] = 401
			retjson['content'] = u'Database store _id is wrong!'
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)