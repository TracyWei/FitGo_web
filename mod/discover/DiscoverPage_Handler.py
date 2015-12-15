# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler,UsersCache
from ..databases.tables import TopicsCache
import traceback
from state_like_controller import getLike
from sqlalchemy.orm.exc import NoResultFound

#/discover/discover_page
class DiscoverPageHandler(BaseHandler):
    def get(self):#发现主页面
        if self.current_user:
            self.render('discoverpage.html',state=1,user=self.current_user)
        else:
            self.render('index.html',state=0,user=self.current_user)
    def post(self):
        try:
            times = self.get_argument("times")#刷新次数［0,1，2，。。。。］
            start = int(times)*12
            end = start + 12
            try:
                topics = self.db.query(TopicsCache).order_by((TopicsCache.topic_time+0).desc())[start:end]#topic_time参数格式未解决
                if topics:
                    retjson = {'code':200,'content':'success to query state'}
                    content1 = []
                    for n in topics:
                        content = {}
                        content['uid'] = n.uid
                        try:
                            user = self.db.query(UsersCache).filter(UsersCache.uid==n.uid).one()
                        except NoResultFound:
                            break
                        content['name'] = user.name
                        content['topics_id'] = n.topic_id
                        content['topic_time'] = n.topic_time
                        content['topic_content'] = n.topic_content
                        content['topic_pic'] = n.topic_pic
                        content['pic_shape'] = n.pic_shape
                        content['topic_title'] = n.topic_title
                        content['topic_starers'] = getLike(n.topic_id,self.Mongodb())
                        content1.append(content)
                    retjson['content'] = content1
                else:
                    retjson = {'code':400,'content':'have no state'}
            except Exception,e:
                retjson = {'code':400,'content':'failed to query state'}
            self.render('discover_state.html',content=retjson)
        except Exception,e:
            retjson = {'code':400,'content':'no parameter'}