# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
import tornado.web
import tornado.gen
import json
import uuid
import re
from time import time

from ..databases.tables import TopicsCache
from ..databases.tables import UsersCache 
from ..databases.tables import User_tagCache

from ..auth.Base_Handler import BaseHandler



class UserPageHandler(BaseHandler):
    """修改个人信息"""
    def get(self,user_id):
        if self.current_user:
            self.render('infochange.html',state=1,user=self.current_user)
        else:
            self.render('index.html',state=0,user=self.current_user)

    def post(self,user_id):
        # 获取id
        # uid = self.get_argument('id')
        retjson = {'code':200,'content':'ok'}
        uid = user_id
        try:
            gender = self.get_argument('gender') 
            name = self.get_argument('name') 
            school = self.get_argument('school') 
            campus = self.get_argument('campus') 
            tag = self.get_argument('tag') 
            info_phone = self.get_argument('info_phone') 
            signature = self.get_argument('signature') 
            # self.write(campus+info_email+info_phone+portrait+user_name)

            if name:
                string = 'name=\'%s\'' % name + ','
                if gender:
                    string = string + 'gender=\'%s\'' % gender + ','
                if school:
                    string = string + 'school=\'%s\'' % school + ','
                if campus:
                    string = string + 'campus=\'%s\'' % campus + ','
                if info_phone:
                    string = string + 'info_phone=\'%s\'' % info_phone + ','
                if signature:
                    string = string + 'signature=\'%s\'' % signature + ','
                length0 = len(string)
                length = length0 - 1
                string = string[0:length]
                try:
                    self.db.execute("update Users set %s where uid=\'%s\';" % (string,uid))
                except Exception,e:
                    retjson = {'code':400,'content':'Users failed to update'}
                if tag:
                    try:
                        self.db.execute("update User_tag set user_enjoyment=\'%s\' where uid=\'%s\';" % (tag,uid))
                    except Exception,e:
                        retjson = {'code':400,'content':'User_tag failed to update'}
                try:
                    self.db.commit()
                except:
                    self.db.rollback()
                    retjson['code'] = 401
                    retjson['content'] = u'Database store is wrong!'
            else:
                retjson = {'code':400,'content':"name is null"}
           
        except Exception,e:
            retjson['code'] = 400
            retjson['content'] = u'Arguments is empty'
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)


        
