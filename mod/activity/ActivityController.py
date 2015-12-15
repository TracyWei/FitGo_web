# -*- coding: utf-8 -*-
#!/usr/bin/env python
import traceback

def getJoinUid(act_id,Mongodb):
        retjson = {'code':200,'content':'ok'}
        if not act_id:
            retjson['code'] = 400
            retjson['content'] = 'Parameter Lack'
        else:
            try:
                # print act_id
                act = Mongodb.Act.find_one({"_id":str(act_id)}) #!!!!坑死我了，通过postman传入的是str，这里从数据库取出的是整数，所以必须转换
                if act:
                    keys = act.keys()
                    content = []
                    for key in keys:
                        if key != '_id':
                            content.append({'uid':key,'name':act[key]})
                    retjson['content'] = content
                else:
                    Mongodb.Act.insert({"_id":str(act_id)})
                    retjson['content'] = []
            except:
                retjson['code'] = 500
                retjson['content'] = 'SQL Error!'
        # print retjson
        return retjson