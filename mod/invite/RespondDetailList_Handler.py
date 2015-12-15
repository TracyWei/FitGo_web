# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,Invite_relation
import json,time
#have been tested
class RespondDetailListHandler(BaseHandler):
	#获得我发的邀请列表详细信息
	def get(self):
		arg_uid = self.current_user.uid
		# arg_uid = self.get_argument("uid")
		arg_id = self.get_argument("_id")
		retjson = {'code':200,'content':'ok'}
		content=[]
		try:
			item = self.db.query(InviteCache).filter(InviteCache._id==arg_id).one()
			if item:
				content1={}
				content1['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(item.start_time)))
				content1['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(item.end_time)))
				content1['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(item.create_time)))
				content1['fit_location'] = item.fit_location
				content1['fit_item'] = item.fit_item
				content1['item_tag'] = item.item_tag
				content1['gender'] = item.gender
				content1['remark'] = item.remark
				print content1
				try:
					participators = self.db.query(Invite_relation).filter(Invite_relation._id==arg_id).all()
					participate=[]
					if participators:
						for n in participators:
							participator={}
							participator['uid_request'] = n.uid_request
							participator['request_name'] = n.request_name
							participate.append(participator)
						content1['participators'] = participate
						content.append(content1)
						retjson['content'] = content
					else:
						content1['participators'] = participate
						content.append(content1)
						retjson['content'] = content
				except Exception,e:
					retjson['code'] = 401
					retjson['content'] = u'failed to query database－Invite_relation!'
			else:
				retjson['content'] = u'No item!'
		except Exception,e:
			retjson['code'] = 401
			retjson['content'] = u'failed to query database－InviteCache!'
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)

