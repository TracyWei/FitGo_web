# -*- coding: utf-8 -*-
#!/usr/bin/env python
import traceback

def getLike(topic_id,Mongodb):
    retjson = {'code':200,'content':'ok'}
    try:
        if not topic_id:
            retjson['code'] = 400
            retjson['content'] = 'Parameter Lack'
        else:
            try:
                # print act_id
                topic = Mongodb.Topic.find_one({'_id':str(topic_id)}) 
                if topic:
                    keys = topic.keys()
                    content = []
                    for key in keys:
                        if key != '_id':
                            content.append({'uid':key,'name':topic[key]})
                    retjson['content'] = content
                else:
                    Mongodb.Topic.insert({'_id':str(topic_id)})
                    retjson['content'] = []
            except:
                retjson['code'] = 500
                retjson['content'] = 'SQL Error!'
    except:
        retjson['code'] = 400
        retjson['content'] = 'Parameter Lack'
    return retjson