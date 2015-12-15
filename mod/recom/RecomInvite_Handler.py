#-*- coding: UTF-8 -*-
from mod.auth.Base_Handler import BaseHandler
import pymongo
import tornado.web
import tornado.gen
import tornado.web
import tornado.gen
import json,time


from pymongo import MongoClient

from ..databases.tables import UsersCache,CookieCache,ActCache,InviteCache
#/discover/add
class RecomInviteHandler(BaseHandler):
    def get (self):
      """
        推荐invite，不需要参数，post方法。返回json值。json值是推荐的活动集合

        方法：post
        参数：None
        返回：Json格式的  code：状态码  content： invite集合。content是一个list。
        测试：已测试，可用。
        注意事项：数据库 act_item 不可为空

      """

      rejson = {'code':200,'content':'ok'}
      # uid
      user_cookie = self.current_user
      # uid = user_cookie.uid
      uid = self.current_user.uid
      person = self.db.query(InviteCache).filter(InviteCache.uid == uid).first()

      # cos = float(person.cos)
      if person is None:
        cos = 0.0
        acts = self.db.query(InviteCache).filter().all() 

      else:
        # cos = float(person.cos)
        cos = person.cos
        fit_item = person.fit_item
        acts = self.db.query(InviteCache).filter(InviteCache.fit_item == fit_item,InviteCache.uid != uid).all()

      acts.sort(key = lambda obj:abs(obj.cos-cos),reverse=False)
      content1=[]
      n = 1
      for act in acts:
        # print act.uid
        if n >20:
          break
        n = n + 1
        content = {}
        person = self.db.query(UsersCache).filter(UsersCache.uid == act.uid).first()

        content['uid'] = str(act.uid)
        
        if person.name is None:
          content['name'] = str((person.name))
        else:
          content['name'] = str((person.name).encode('utf-8'))
        if person.signature is None:
          content['signature'] = str((person.signature))
        else:
          content['signature'] = str((person.signature).encode('utf-8'))
          

        content['portrait'] = str(person.portrait)


        content['fit_item'] = str(act.fit_item)
        content['gender'] = str(act.gender)
     
        content['_id'] = str(act._id)
        content['create_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(act.create_time)))
        content['duration'] = str(act.duration)
        content['start_time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(act.start_time)))
        if act.fit_location is None:
          content['fit_location'] = str((act.fit_location))
        else:
        # else:  
          content['fit_location'] = str((act.fit_location).encode('UTF-8'))

        if act.user_tag is None:
          content['user_tag'] = str((act.user_tag))
        else:
          content['user_tag'] = str((act.user_tag).encode('UTF-8'))

        if act.remark is None:
          content['remark'] = str((act.remark))
        else:
          content['remark'] = str((act.remark).encode('UTF-8'))
         

        content1.append(content)
     

      rejson['content'] = content1

            
      ret = json.dumps(rejson,ensure_ascii = False, indent = 2)

      self.render("invite_item.html",ret=rejson)
      # self.write(ret)