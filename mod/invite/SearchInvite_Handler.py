# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import InviteCache,SystemTagCache
import json,time,string
# have been tested
#/invite/search/
class SearchInviteHandler(BaseHandler):
	# @tornado.web.authenticated
	def post(self):#搜索invitation
		arg_uid = self.get_argument("uid")
		arg_item_tag = self.get_argument("item_tag")
		arg_start_time = self.get_argument("start_time")
		arg_fit_location = self.get_argument("fit_location")
		arg_fit_item = self.get_argument("fit_item")
		arg_gender = self.get_argument("gender")
		# arg_uid = self.current_user.uid
		retjson = {'code':200,'content':'ok'}
		sql = "select * from Invite where uid!=\'%s\' and " % arg_uid
		string = ''
		try:
			if arg_item_tag:
				string = string + 'item_tag like \'%%%s%%\'' % arg_item_tag + ' and '
			if arg_start_time:
				time_now=time.time()
				string = string + 'start_time >= %s' % arg_start_time + ' and start_time >= %s' % str(time_now) + 'and' 
			if arg_fit_location:
				string = string + 'fit_location like \'%%%s%%\'' % arg_fit_location + ' and '
			if arg_fit_item:
				string = string + 'fit_item like \'%%%s%%\'' % arg_fit_item + ' and '
			if arg_gender:
				string = string + 'gender=\'%s\'' % arg_gender + ' and '
			if string.strip()=='':
				retjson = {'code':400,'content':'all parameters are null'}
			else:
				sql = sql + string
				length0 = len(sql)
				length = length0 - 5
				sql = sql[0:length]
			try:
				invitations = self.db.execute(sql).fetchall()#[0:40]
				content1 = []
				for i in invitations:
					content = {}
					content['uid'] = i.uid
					content['name'] = i.name
					content['start_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.start_time)))
					content['end_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.end_time)))
					content['create_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.create_time)))
					content['fit_location'] = i.fit_location
					content['fit_item'] = i.fit_item
					content['gender'] = i.gender
					content['remark'] = i.remark
					content['_id'] = i._id
					content1.append(content)
				retjson['content'] = content1
			except Exception, e:
				retjson['code'] = 401
				retjson['content'] = u'Nothing found!Please try other conditions'
		except Exception,e:
			retjson = {'code':400,'content':'failed to search invitation'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.write(ret)
	# def get(self):#根据热门标签获得invitation
	# 	retjson = {'code':200,'content':'ok'}
	# 	arg_hot_tag = self.get_argument('hot_tag')
	# 	try:
	# 		items = self.db.query(SystemTagCache).filter(SystemTagCache.hot_tag==arg_hot_tag).all()
			# if items:
			# 	content1 = []
			# 	for i in invitations:
			# 		content = {}
			# 		content['uid'] = i.uid
			# 		content['name'] = i.name
			# 		content['start_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.start_time)))
			# 		content['end_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.end_time)))
			# 		content['create_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(i.create_time)))
			# 		content['fit_location'] = i.fit_location
			# 		content['fit_item'] = i.fit_item
			# 		content['gender'] = i.gender
			# 		content['remark'] = i.remark
			# 		content['_id'] = i._id
			# 		content1.append(content)
			# 	retjson['content'] = content1

			# else:
			# 	retjson['content'] = u'Nothing to found!'
	# 	except Exception,e:
		# 	retjson = {'code':400,'content':'failed to search invitation'}
		# ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		# self.write(ret)

