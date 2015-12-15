# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler
#/invite/user_page
class InvitePageHandler(BaseHandler):
	# @tornado.web.authenticated
    def get(self):#约健身主页
        if self.current_user:
            self.render('invite.html',state=1,user=self.current_user)
        else:
            self.render('index.html',state=0,user=self.current_user)
