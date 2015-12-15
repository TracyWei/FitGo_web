# -*- coding: utf-8 -*-

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler
from ..databases.tables import ActCache,UsersCache
import json
import traceback
from ActivityController import getJoinUid

class AddActivityHandler(BaseHandler):
    """ 
    get函数：
        参数：
            act_id:活动id
        返回：
            返回活动所有参与的人
        功能：
            获得活动参与人名单页面
    post函数：
        参数：
            uid：用户uid
            act_id：参与活动的id
        返回：

        功能：
            用户参与活动的状态
         """
    def get(self):
        retjson = {'code':200,'content':'ok'}
        try:
            act_id = self.get_argument('act_id')
        except:
            retjson['code'] = 400
            retjson['content'] = 'Parameter Lack'
        retjson = getJoinUid(act_id,self.Mongodb())
        self.render('act_join_people.html',content=retjson)
        # self.write(json.dumps(retjson,ensure_ascii=False,indent=2))

    def post(self):
        retjson = {'code':200,'content':'ok'}
        uid = self.get_argument("uid")
        act_id = self.get_argument('act_id')
        if not uid or not act_id:
            retjson['code'] = 400
            retjson['content'] = 'Parameter Lack'
        else:
            try:
                user = self.db.query(UsersCache).filter(UsersCache.uid == uid).one()
                try:
                    act = self.Mongodb().Act
                    act.update({"_id":act_id},{"$set":{uid:user.name}},True)
                except Exception,e:
                    retjson['code'] = 500
                    retjson['content'] = 'SQL Error!'
            except Exception,e:
                retjson['code'] = 500
                retjson['content'] = 'SQL Error!'
        self.write(json.dumps(retjson,ensure_ascii=False,indent=2))

    # def getJoinUid(self,act_id):
    #     retjson = {'code':200,'content':'ok'}
    #     if not act_id:
    #         retjson['code'] = 400
    #         retjson['content'] = 'Parameter Lack'
    #     else:
    #         try:
    #             act = self.Mongodb().Act.find_one({"_id":act_id})
    #             if act:
    #                 keys = act.keys()
    #                 content = []
    #                 for key in keys:
    #                     if key != '_id':
    #                         content.append({'uid':key,'name':act[key]})
    #                 retjson['content'] = content
    #             else:
    #                 retjson['code'] = 403
    #                 retjson['content'] = 'No this activity!'
    #         except:
    #             retjson['code'] = 500
    #             retjson['content'] = 'SQL Error!'
    #     return retjson
            

