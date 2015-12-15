# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import ActCache
from time import mktime,strptime,strftime,time,localtime
from sqlalchemy.orm.exc import NoResultFound
from ActivityController import getJoinUid
import json,string
from config import icon
import random
#/activity/activity_page
class ActivityPageHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.render('activity.html',state=1,user=self.current_user)
        else:
            self.render('index.html',state=0,user=self.current_user)
    def post(self):
        nowtime = int(time())
        retjson = {'code':200,'content':''}
        try:
            act = self.db.query(ActCache).filter(ActCache.create_time>nowtime-86400).order_by(ActCache.act_id.desc())
            all_content = []
            for i in act:
                contentTemp = {
                    'id':i.act_id,
                    'uid':i.uid,
                    'create_time':strftime("%Y-%m-%d",localtime(string.atoi(i.create_time))),
                    'title':i.act_title,
                    'start':strftime("%Y-%m-%d",localtime(int(i.start_time))),
                    'end':strftime("%Y-%m-%d",localtime(int(i.end_time))),
                    'location':i.act_location,
                    'detail':i.act_detail,
                    'join_uid':getJoinUid(i.act_id,self.Mongodb())
                }
                all_content.append(contentTemp)
            retjson['content'] = all_content
        except NoResultFound:
            retjson['code'] = 402
            retjson['content'] = 'No fresh content'
        num = []
        length = len(retjson['content'])
        for i in range(length):
            num.append(random.randint(0, 4))
        self.render('activity_item.html',ret=retjson,icon=icon,num=num)
        # self.write(json.dumps(retjson,ensure_ascii=False, indent=2))
