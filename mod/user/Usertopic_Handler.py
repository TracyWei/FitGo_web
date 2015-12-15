# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
import json,time
from time import strftime,localtime
from ..databases.tables import TopicsCache
from ..auth.Base_Handler import BaseHandler
from ..discover.state_like_controller import getLike
from sqlalchemy.orm.exc import NoResultFound
import traceback




class UsertopicHandler(BaseHandler):
    """docstring for WatchUser_handler"""
    def post(self):
        # 获取id
        rejson = {'code':200,'content':'ok'}
        try:
            uid = self.get_argument('uid')
            # uid = self.current_user.uid
            # person = self.db.query(UsersCache).filter(UsersCache.uid == uid).one()
            topics = self.db.query(TopicsCache).filter(TopicsCache.uid == uid).all()
            
            content1 = []
            for row in topics:
                content={}
                topic_content = row.topic_content
                topic_title = row.topic_title
                topic_time = row.topic_time
                content['topic_content'] = topic_content
                content['topic_title'] = topic_title
                content['topic_starers'] = getLike(row.topic_id,self.Mongodb())
                content['time_y'] = strftime("%Y-%m-%d",localtime(int(topic_time)))
                content['time_h'] = strftime("%H:%M",localtime(int(topic_time)))
                content1.append(content)
            rejson['content'] = content1
                # json = json + "{uid:"+str(uid)+",topic_id:"+str(topic_id)+",topic_content:"+str(topic_content)+",topic_pic:"+str(topic_pic)+",topic_title:"+str(topic_title)+",topic_starers:"+str(topic_starers)+"}"
            
            # json = "{"+json+"}"
        except NoResultFound:
            rejson['code'] = 400
            rejson[content] = 'No user'
        except Exception,e:
            print traceback.print_exc()
            rejson['code'] = 500
            rejson['content'] = 'Error'
        ret = json.dumps(rejson,ensure_ascii = False, indent = 2)
        self.render('mystate.html',content=rejson)
        # self.write(ret)

       
      
