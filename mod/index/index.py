# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from ..auth.Base_Handler import BaseHandler

class IndexHandler(BaseHandler):
    # @tornado.web.authenticated
   
    def get(self):
        # if not self.current_user:
        #     print " no user redirect to login "
        #     self.redirect("/auth/login")
        # return
        self.render('index.html',state=1,user=self.current_user)