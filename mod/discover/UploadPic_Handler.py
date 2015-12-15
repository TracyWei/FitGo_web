#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import shutil
import os
from mod.auth.Base_Handler import BaseHandler
import json
import hashlib
#/discover/create/state/pic
class UploadPicHandler(BaseHandler):
    def post(self):
        # upload_path=os.path.join(os.path.dirname('mod'),'static/picture')  #文件的暂存路径
        upload_path = '/static/picture'
        save_path = 'static/picture'
        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        if file_metas:
            retjson = {'code':200,'content':'picture upload success!'}
            for meta in file_metas:
                filename=meta['filename']
                houzhui = filename.split('.')[-1:][0]
                sha1obj = hashlib.md5()
                sha1obj.update(meta['body'])
                hash = sha1obj.hexdigest()
                filepath = save_path +'/'+ sha1obj.hexdigest() + '.' + houzhui
                with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])

            retjson['content'] = '/'+filepath
        else:
            retjson = {'code':400,'content':'failed to upload picture'}
        self.write(json.dumps(retjson,ensure_ascii=False, indent=2))

