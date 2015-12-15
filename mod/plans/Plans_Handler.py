# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 

import tornado.web
import tornado.gen
import tornado.web
import tornado.gen
import json


from ..databases.tables import PlansCache
from ..databases.tables import UsersCache

from ..auth.Base_Handler import BaseHandler
import json,time
from time import strftime,localtime


class PlansHandler(BaseHandler):
     """
     get函数：
        展示plan主页面
     post函数:
        发表plan

    plan的json格式:
        {
            '_id':'',
            'content':{
                'target':'',
                'signature':'',
                'start_time':'',
                'end_time':'',
                '1':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '2':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '3':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '4':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '5':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '6':{
                    'selectValue':[],
                    'inputValue':[]
                },
                '7':{
                    'selectValue':[],
                    'inputValue':[]
                }
            },
            'star':{
                {uid}:{name}
                ...
            }
        }

    其中，selectValue共11个,其中0,1,2是有氧运动三个选择框,3,4,5,6,7是无氧运动,8,9,10是拉伸运动
          inputValue共3个，分别对应有氧，无氧以及拉伸运动的用户自定义输入
     """
     def get(self):
        if self.current_user:
            self.render('plans.html',state=1,user=self.current_user)
        else:
            self.render('index.html',state=0,user=self.current_user)
        # self.render('plans.html',state=1,user=self.current_user)

     def post(self):
        retjson = {'code':200,'content':'ok'}
        planJson = self.get_argument('plan')
        plan = json.loads(planJson)
        plan['uid'] = self.current_user.uid
        plan['create_y'] = strftime("%Y-%m-%d",localtime(time.time()))
        plan['create_h'] = strftime("%H:%M",localtime(time.time()))
        try:
            self.Mongodb().Plan.insert(plan)
        except Exception,e:
            retjson['code'] = 400
            retjson['content'] = 'New Plan Error!'
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)
        
        Dict = plan['content']
        Dict.pop('end_time')
        # Dict.pop('start_time')

        Dict.pop('target')
        Dict.pop('signature')
        del Dict['start_time']
        uid = self.current_user.uid
        if Dict is not None :
            # print Dict['1']['selectValue'][0]
            for k,v in Dict.items():
                fit_item = Dict[str(k)]['selectValue'][0]
                status_cookie = PlansCache(uid = uid,fit_item = fit_item)

                self.db.add(status_cookie)

                self.db.commit()


