#-*- coding: UTF-8 -*-
from mod.auth.Base_Handler import BaseHandler
import pymongo
import tornado.web
import tornado.gen
import tornado.web
import tornado.gen
import json


from pymongo import MongoClient

from ..databases.tables import UsersCache,CookieCache
''' 
   # 推荐用户  你值得拥有。。。。。。传给你你要的可爱妹纸的id 性别 还有可能的配对率

   方法：post
   参数：None
   返回：Json格式的状态码（code）和用户集合（content）。content是一个list。
   测试：已测试，可用。

'''

class RecomUserHandler(BaseHandler):


    @property
    def db(self):
        return self.application.db


    @property
    def Mongodb(self):
      return self.application.Mongodb


    def on_finish(self):
        self.db.close()

    def post (self):

      rejson = {'code':200,'content':'ok'}
      # uid
      user_cookie = self.current_user
      uid = user_cookie.uid
      # uid = 1
      person = self.db.query(UsersCache).filter(UsersCache.uid == uid).first()
      # self.write(str(person.cos))
      cos = float(person.cos)
      users = self.db.query(UsersCache).filter((UsersCache.cos-cos)>-0.9, (UsersCache.cos-cos) < 0.9 ).all()
      users.sort(key = lambda obj:abs(obj.cos-cos),reverse=False)
      
      content1=[]
      n = 1
      for user in users:
        if n > 10:
          break
        n = n + 1
        content = {}
        if user.uid !=uid :
          content['uid'] = str(user.uid)
          content['xiangsidu'] = str(100*(1-abs(user.cos-cos)))+"%"
          if user.name is None:
            content['name'] = str((user.name))
          else:
            content['name'] = str((user.name).encode('utf-8'))
          if user.signature is None:
            content['signature'] = str((user.signature))
          else:
            content['signature'] = str((user.signature).encode('utf-8'))
          

          content['portrait'] = str(user.portrait)
          content['gender'] = str(user.gender)
          content1.append(content)


      rejson['content'] = content1

            
      ret = json.dumps(rejson,ensure_ascii = False, indent = 2)

       
      self.write(ret)

        
