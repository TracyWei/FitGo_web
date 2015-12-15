#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import shutil
import os
import hashlib
import json
from ..auth.Base_Handler import BaseHandler
from ..databases.tables import UsersCache
import hashlib,json
 
class UploadPortraitHandler(BaseHandler):
    def get(self):
        self.render("upload_portrait.html")
 
    def post(self):
         # upload_path=os.path.join(os.path.dirname('mod'),'static/picture')  #文件的暂存路径
        upload_path = '/static/portrait'
        save_path = 'static/portrait'
        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        if file_metas:
            retjson = {'code':200,'content':'portrait upload success!'}
            for meta in file_metas:
                filename=meta['filename']
                houzhui = filename.split('.')[-1:][0]
                sha1obj = hashlib.md5()
                sha1obj.update(meta['body'])
                hash = sha1obj.hexdigest()
                filepath = save_path +'/'+ sha1obj.hexdigest() + '.' + houzhui
                database_path = upload_path  +'/'+ sha1obj.hexdigest() + '.' + houzhui
                with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
        
            try:
                a_uid = self.current_user.uid
                self.db.execute("update Users set portrait=\'%s\' where uid=\'%s\';" % (database_path,a_uid))  
                
                try:
                    self.db.commit()
                except:
                    self.db.rollback()
                    retjson['code'] = 401
                    retjson['content'] = u'Database store is wrong!'
                retjson['content'] = 'success to add to database'
            except Exception,e:
                retjson['content'] = 'failed to add to database'
        else:
            retjson = {'code':400,'content':'failed to upload portrait'}
        self.write(json.dumps(retjson,ensure_ascii=False, indent=2))
 