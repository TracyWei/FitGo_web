# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from Base_Handler import BaseHandler
from ..databases.tables import UsersCache,CookieCache
#/auth/logout
class LogoutHandler(BaseHandler):
    # @tornado.web.authenticated
    def delete(self):#用户登出，删除cookie
        status = self.current_user
        if status:
            self.db.delete(status)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
        else:
            pass