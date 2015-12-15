# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import Invite_relation,InviteCache
import json,time

class EvaluateHandler(BaseHandler):
	def post(self):#评论评分
		retjson = {'code':200,'content':'ok'}
		arg_id = self.get_argument('id')
		arg_score = self.get_argument('score')
		arg_comment = self.get_argument('comment')
		try:
			invitation = self.db.execute("select * from Invite_relation where id = %s;" % arg_id).fetchall()
			print invitation
			if invitation:
				print "aa"
				invitation.score = arg_score
				invitation.comment = arg_comment
				self.db.add(invitation)
				try:
					self.db.commit()
				except Exception,e:
					self.db.rollback()
					retjson['code'] = 401
					retjson['content'] = u'Database store is wrong!'
			else:
				retjson['content'] = u'no invitation!'
		except Exception, e:
			retjson['code'] = 401
			retjson['content'] = u'failed to query Invite_relation!'
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)
