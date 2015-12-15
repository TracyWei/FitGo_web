# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from Base_Handler import BaseHandler
from ..databases.tables import UsersCache,CookieCache
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_
import uuid
import re
from time import time
import json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import urllib
import traceback
import hashlib,random,string

class RegisterHandler(BaseHandler):
    def get(self):
        if not self.current_user:  
            self.render('login.html')  
        else:  
            self.redirect('/') 
    def post(self):
        retjson = {'code':200,'content':'ok'} # define a dict
        arg_name=self.get_argument("name")#get 
        arg_password=self.get_argument("password")
        arg_uid=self.get_argument("uid")
        if not arg_password or not arg_name or not arg_uid:
            retjson['code'] = 400
            retjson['content'] = u'Arguments is empty~'
        elif len(arg_password) < 6 :
            retjson['code'] = 403
            retjson['content'] = u'Your password is too short'
        else:
            try:
                #store password and name
                t1=self.db.query(UsersCache).filter(UsersCache.uid==arg_uid) #UserCache object
                salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                arg_password = hashlib.md5(salt.join(arg_password)).hexdigest()
                t1.update({UsersCache.name:arg_name,UsersCache.password : arg_password,UsersCache.salt:salt})
                #create cookie and store
                cookie_uuid=uuid.uuid1()
                self.set_secure_cookie("username",str(cookie_uuid),expires_days=30,expires=int(time())+2592000)
                status_cookie = CookieCache(cookie=cookie_uuid,uid=arg_uid)
                self.db.add(status_cookie)
                # commit to sql
                self.db.execute("update Users set portrait='/static/portrait/1.png' where uid=\'%s\';" % arg_uid)
                try:
                    self.db.commit()
                except Exception, e:
                    self.db.rollback()
                    retjson['code'] = 401
                    retjson['content'] = u'Database store is wrong!'
            except NoResultFound:
                retjson['code'] = 402
                retjson['content'] = "Sql store is wrong!Try again!"
        #format json
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)


class VerifyHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        retjson = {'code':200,'content':'ok'}
        arg_info_email=self.get_argument('info_email')
        arg_student_card=self.get_argument('student_card')
        arg_student_id = self.get_argument('student_id')
        if not arg_info_email or not arg_student_id or not arg_student_card :
            retjson['code'] = 400
            retjson['content'] = u'Arguments is empty~'
        elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", arg_info_email) == None :
            retjson['code'] = 404
            retjson['content'] = u'Your email format is wrong'
        else :
            if arg_student_card != '123456' or arg_student_id != '123456':
                try:
                    client = AsyncHTTPClient()
                    login_url = 'http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action'
                    login_value = {
                                    'queryStudentId':arg_student_card,
                                    'queryAcademicYear':'15-16-1'

                    }
                    request = HTTPRequest(
                                            login_url,
                                            method='POST',
                                            body = urllib.urlencode(login_value),
                                            request_timeout = 5                                        
                                            )

                    response = yield tornado.gen.Task(client.fetch, request)
                    page = response.body
                    xuehao=re.compile('学号:([A-Z,0-9]+)').findall(page)
                    yikatong=re.compile('一卡通号:([A-Z,0-9]+)').findall(page)
                    if response.headers :
                        if arg_student_card == yikatong[0] and arg_student_id == xuehao[0] :
                            retjson['content'] = 'right'
                        else :
                            retjson['code'] = 404
                            retjson['content'] = u'Your student_card or id not right'
                            ret = json.dumps(retjson,ensure_ascii=False, indent=2)
                            self.write(ret)
                            self.finish()
                            return
                    else :
                        retjson['code'] = 404
                        retjson['content'] = u'Your student_card or id not found'
                        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
                        self.write(ret)
                        self.finish()
                        return

                except Exception, e:
                    retjson['code'] = 404
                    retjson['content'] = u'search card and id failed '
                    ret = json.dumps(retjson,ensure_ascii=False, indent=2)
                    self.write(ret)
                    self.finish()
                    return
            else:
                retjson['content'] = 'right'
            if retjson['content'] == 'right':
                try:
                    if arg_student_card == '123456' and arg_student_id == '123456':
                        person = self.db.query(UsersCache).filter(UsersCache.info_email==arg_info_email).one()
                        retjson['code'] = 401
                        retjson['content'] = u'user %s has exited!' % (person.info_email)
                    else :
                        person = self.db.query(UsersCache).filter(or_(UsersCache.student_card==arg_student_card,UsersCache.info_email==arg_info_email)).one()
                        retjson['code'] = 401
                        if person.info_email == arg_info_email:
                            retjson['content'] = u'user %s has exited!' % (person.info_email)
                        else:
                            retjson['content'] = u'user %s has exited!' % (person.student_card)
                except NoResultFound :
                    uid_uuid = uuid.uuid5(uuid.NAMESPACE_DNS,str(arg_info_email))
                    status_users = UsersCache(student_card = arg_student_card,student_id = arg_student_id,uid = uid_uuid,info_email = arg_info_email)
                    self.db.add(status_users)
                    try:
                        self.db.commit()
                        retjson['content'] = {'uid':str(uid_uuid),'content':'Verify pass!'}
                    except Exception, e:
                        self.db.rollback()
                        retjson['code'] = 401
                        retjson['content'] = u'Database store is wrong!'
            else :
                pass
        ret = json.dumps(retjson,ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()