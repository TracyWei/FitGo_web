# -*- coding: utf-8 -*-

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler
from ..databases.tables import TopicsCache,UsersCache
from state_like_controller import getLike
import json
import traceback

class JoinStateHandler(BaseHandler):
    def get(self):
        topic_id = self.get_argument('topic_id')
        
        retjson = getLike(topic_id,self.Mongodb())
        self.write(json.dumps(retjson,ensure_ascii=False,indent=2))
        # self.render('',content=retjson)


    def post(self):
        retjson = {'code':200,'content':'ok'}
        uid = self.current_user.uid
        topic_id = self.get_argument('topic_id')
        if not uid or not topic_id:
            retjson['code'] = 400
            retjson['content'] = 'Parameter Lack'
        else:
            try:
                user = self.db.query(UsersCache).filter(UsersCache.uid == uid).one()
                try:
                    topic = self.Mongodb().Topic
                    topic.update({"_id":topic_id},{"$set":{uid:user.name}},True)
                except Exception,e:
                    retjson['code'] = 500
                    retjson['content'] = 'SQL Error!'
            except Exception,e:
                retjson['code'] = 500
                retjson['content'] = 'SQL Error!'
        self.write(json.dumps(retjson,ensure_ascii=False,indent=2))