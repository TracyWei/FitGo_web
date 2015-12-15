# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler
from ..databases.tables import UsersCache,User_tagCache
import json

#/discover/search/friends
class SearchFriendHandler(BaseHandler):
	def post(self):#搜索好友
		a_name = self.get_argument('name')
		a_gender = self.get_argument('gender')
		a_campus = self.get_argument('campus')
		a_school = self.get_argument('school')
		a_user_enjoyment = self.get_argument('user_enjoyment')
		string = ''
		try:
			if a_name:
				string = string + 'name like \'%%%s%%\'' % a_name + ' and '
			if a_campus:
				string = string + 'campus=\'%s\'' % a_campus + ' and '
			if a_school:
				string = string + 'school=\'%s\'' % a_school + ' and '
			if a_gender:
				string = string + 'gender=\'%s\'' % a_gender + ' and '
			if a_user_enjoyment:
				string = string + 'uid in (select uid from User_tag where User_tag.user_enjoyment like \'%%%s%%\')' % a_user_enjoyment + ' and '
		

			
			if string.strip()=='':
				retjson = {'code':400,'content':'all parameters are null'}
			else:
				length0 = len(string)
				length = length0 - 5
				string = string[0:length]
				persons = self.db.execute("select * from Users where %s;" % string).fetchall()
				if persons:
					retjson = {'code':200,'content':'ok'}
					content1 = []
					for n in persons:
						content = {}
						content['uid'] = n.uid
						content['name'] = n.name
						content['signature'] = n.signature
						content['portrait'] = n.portrait
						content1.append(content)
					retjson['content'] = content1
				else:
					retjson = {'code':400,'content':'not match friend'}	


		except Exception,e:
			retjson = {'code':400,'content':'failed to search friend'}
		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
		self.render('discover_friend.html',content=retjson)

		