# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,Invite_relation,UsersCache
import json,time
import traceback
#have been tested
#/invite/respond
class RespondInviteHandler(BaseHandler):
	def post(self):#确认消息
		arg_uid_respond = self.get_argument('uid_respond')
		arg_uid_request = self.get_argument('uid_request')
		arg_id = self.get_argument('_id')
		arg_state = self.get_argument('state')
		retjson = {'code':200,'content':'ok'}
		try:
			relation = self.db.query(Invite_relation).filter(Invite_relation.uid_request==arg_uid_request,\
				Invite_relation.uid_respond==arg_uid_respond,Invite_relation._id==arg_id).one()
			if relation:
				relation.state = arg_state
				self.db.add(relation)
				try:
					self.db.commit()
				except Exception,e:
					self.db.rollback()
					retjson['code'] = 401
					retjson['content'] = u'Database store is wrong!'
			else:
				retjson['content'] = u'no relations!'
		except Exception, e:
			retjson['code'] = 401
			retjson['content'] = u'failed to query Invite_relation!'
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)