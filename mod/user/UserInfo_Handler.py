# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
import tornado.web
import tornado.gen
import json
from sqlalchemy.orm.exc import NoResultFound
from ..databases.tables import UsersCache 
from ..databases.tables import User_tagCache
from ..auth.Base_Handler import BaseHandler



class UserinfoHandler(BaseHandler):
    """
    get函数：
        访问个人主页
        tips：
            如果用户不存在，跳转到首页
            如果用户是自己，跳转到自己个人主页
    post函数:
        获取个人信息

    """
    def get(self,uid):
        try:
            if uid==self.current_user.uid:
                self.redirect('/plans')
            else:
                person = self.db.query(UsersCache).filter(UsersCache.uid == uid).one()
                content={
                    'name':person.name,
                    'signature':person.signature,
                    'pic':person.portrait
                }
                self.render("forothers.html",state=1,uid=uid,content=content,user = self.current_user)
        except NoResultFound:
            self.redirect('/')
    def post(self,user_id):
        # 获取id
        # uid = self.get_argument('id')
        retjson = {'code':200,'content':'ok',
                                    'info':'',
                                    'tag':
                                    {
                                        'user_enjoyment':[],
                                        'user_join_times':[],
                                        'user_score':[],
                                        'user_join_event':[]
                                        }
                    }
        try:
            person = self.db.query(UsersCache).filter(UsersCache.uid == user_id).one()
            retjson['info'] = {
                                    'name':person.name,
                                    'student_card':person.student_card,
                                    'student_id':person.student_id,
                                    'gender':person.gender,
                                    'school':person.school,
                                    'campus':person.campus,
                                    'info_email':person.info_email,
                                    'info_phone':person.info_phone,
                                    'portrait':person.portrait,
                                    'signature':person.signature
                                    }
                                
            try:
                tags = self.db.query(User_tagCache).filter(User_tagCache.uid == person.uid).one()
                retjson['tag'] = {
                                    'user_enjoyment':tags.user_enjoyment,
                                    'user_join_times':tags.user_join_times,
                                    'user_score':tags.user_score,
                                    'user_join_event':tags.user_join_event
                                }
                temptag = []
                if tags.user_enjoyment:
                    tag = tags.user_enjoyment.split(',')
                    for i in tag:
                        temptag.append(i)
                retjson['tag']['user_enjoyment'] = temptag
            except NoResultFound:
                user = User_tagCache(uid=person.uid)
                self.db.add(user)
                try:
                    self.db.commit()
                except:
                    retjson['code'] = 401
                    retjson['content'] = 'system error'
        except NoResultFound:
            retjson['code'] = 400
            retjson['content'] = 'No User!'
        ret = json.dumps(retjson,ensure_ascii = False, indent = 2)
        self.write(ret)
    