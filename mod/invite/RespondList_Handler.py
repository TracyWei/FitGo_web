# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,Invite_relation
import json,time
#have been tested
class RespondListHandler(BaseHandler):
	#获得我发的邀请列表
	def get(self):#{'code':'200','content':[{'_id':'1','participator':'2',name':"d"},{'_id':'2','participator':'2',name':"d"}]}
		arg_uid = self.current_user.uid
		# arg_uid = self.get_argument("uid")
		retjson = {'code':200,'content':'ok'}
		#0->not defination 1->ok  2->refuse
		try:
			response = self.db.query(Invite_relation).filter(Invite_relation.uid_respond==arg_uid,\
				Invite_relation.state==0).order_by(Invite_relation.id.desc()).all()
			if response:
				dic_1={}#{_id:counter}s
				dic_2={}#{_id:fit_item}
				for n in response:
					if n._id in dic_1:
						dic_1[n._id] += 1
					else:
						dic_1[n._id] = 1
				for n in response:
					if n._id not in dic_2:
						dic_2[n._id] = n.fit_item
				print dic_1
				print dic_2
				items=[]
				for key1 in dic_1:
					item={}
					for key2 in dic_2:
						
						if key1==key2:
							item["_id"]=key1
							item["participator"]=dic_1[key1]
							item["fit_item"]=dic_2[key2]
					items.append(item)
				retjson['content'] = items
			else:
				retjson['content'] = u'No response!'
		except Exception,e:
			retjson['code'] = 401
			retjson['content'] = u'failed to query database!'
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)


						
