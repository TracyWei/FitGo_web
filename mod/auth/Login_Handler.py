# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from Base_Handler import BaseHandler
from ..databases.tables import UsersCache,CookieCache,PlansCache,ActCache,InviteCache
import json
from time import time
import uuid
import re
import math
import hashlib,random,string
from Code_Handler import identify_code
class LoginHandler(BaseHandler):
    def get(self):
        if not self.current_user:  
            self.redirect('/')
            # self.render('login.html') 
        else:  
            self.redirect('/')  
        
    def delete(self):
        retjson = {'code':200,'content':'ok'}
        user_cookie=self.current_user
        if user_cookie :
            users=self.db.query(UsersCache).filter(UsersCache.uid == user_cookie.uid).one()
            self.db.delete(user_cookie)
            self.db.delete(users)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
                retjson['code'] = 401
                retjson['content'] = u'Database store is wrong!'
        else :
            retjson['code'] = 402
            retjson['content'] = u'Current_user is False!'
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)

    def post(self):
        info_email=self.get_argument("info_email")
        user_password=str(self.get_argument("user_password"))
        code=self.get_argument("code")
        is_remember = self.get_argument('is_remember')
        code_random = self.get_argument('code_random')
        retjson = {'code':200,'content':'ok'}
        if not info_email or not user_password or not code:
            retjson['code'] = 400
            retjson['content'] = u'Arguments are empty'
        elif identify_code(self.Mongodb(),code_random,code) :
            retjson['code'] = 403
            retjson['content'] = u'Code is wrong'
        else:
            try:
                #user is right?
                person=self.db.query(UsersCache).filter(UsersCache.info_email==info_email).one()
                passwd = hashlib.md5(person.salt.join(user_password)).hexdigest()
                if passwd == person.password:
                    # self.count(person.uid)
                    self.count(person.uid)
                    #yes => set cookie
                    cookie_uuid=uuid.uuid1()
                    if is_remember == '1' :
                        self.set_secure_cookie("username",str(cookie_uuid),expires_days=30,expires=int(time())+2592000)
                    else:
                        self.set_secure_cookie('username',str(cookie_uuid),expires_days=None)
                    #ok => store
                    status = CookieCache(cookie=cookie_uuid,uid=person.uid)
                    self.db.add(status)
                    try:
                        self.db.commit()
                    except Exception,e:
                        self.db.rollback()
                        retjson['code'] = 401
                        retjson['content'] = u'Database store is wrong!'
                else :
                    retjson['code'] = 402
                    retjson['content'] = u'User name or password is wrong!'
            except Exception, e:
                retjson['code'] = 402
                retjson['content'] = u'User name or password is wrong!'
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)



    def count(self,user_id):
      uid = user_id
      cos = 0
      x0 = 10
      y0 = 0
      x1 = 0
      y1 = 10

      plan = self.db.query(PlansCache).filter(PlansCache.uid == uid).first()
      # fit_item = str((plan.fit_item).encode('UTF-8'))
      # self.write(fit_item)
      if plan is None:

        cos = 0
      else:
        fit_item = (plan.fit_item).encode('UTF-8')
        if fit_item == '拳击':
          x1 = 10
          y1 = 0
        elif fit_item == '滑板':
          x1 = 9
          y1 = 1

        elif fit_item == '立卧撑':
          x1 = 8
          y1 = 2
        elif fit_item == '杠铃' or fit_item == '平板支撑':
          x1 = 7
          y1 = 3
        elif fit_item == '游泳':
          x1 = 6
          y1 = 4

        elif fit_item == '足球' or fit_item == '篮球':
          x1 = 5
          y1 = 5
        elif fit_item == '引体向上':
          x1 = 4
          y1 = 6
        elif fit_item == '羽毛球':
          x1 = 3
          y1 = 7
        elif fit_item == '自行车':
          x1 = 2
          y1 = 8
        elif fit_item == '舞蹈':
          x1 = 1
          y1 = 9
        elif fit_item == '健身操':
          x1 = 0
          y1 = 10
        elif fit_item == '乒乓球':
          x1 = -1
          y1 = 9
        elif fit_item == '瑜伽':
          x1 = -2
          y1 = 8

        elif fit_item == '快走':
          x1 = -3
          y1 = 7
        elif fit_item == '俯卧撑' or fit_item == '双杠曲臂撑':
          x1 = -4
          y1 = 6
        elif fit_item == '慢跑':
          x1 = -5
          y1 = 5

        elif fit_item == '仰卧举腿':
          x1 = -6
          y1 = 4
        elif fit_item == '徒手深蹲':
          x1 = -7
          y1 = 3

        elif fit_item == '哑铃':
          x1 = -8
          y1 = 2

        elif fit_item == '慢跑':
          x1 = -9
          y1 = 1
        elif fit_item == '太极拳':
          x1 = -10
          y1 = 0      
        else:
          x1 = 0
          y1 = 10

        if x1 == 0 and y1 == 10:
          cos = 0;
        else:
          cos = (x0*x1 + y0*y1)/(math.sqrt(abs(x0*x0+y0*y0))*math.sqrt(abs(x1*x1+y1*y1)))
      t1 = self.db.query(UsersCache).filter(UsersCache.uid == uid)


      t1.update({UsersCache.cos:cos})

      t2 = self.db.query(ActCache).filter(ActCache.uid == uid)
      if t2 is not None:
        t2.update({ActCache.cos:cos})       

      t3 = self.db.query(InviteCache).filter(InviteCache.uid == uid)
      if t3 is not None:
        t3.update({InviteCache.cos:cos})             
      self.db.commit()

