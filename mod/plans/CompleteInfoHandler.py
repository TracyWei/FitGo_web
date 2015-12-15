# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler

class CompleteInfoHandler(BaseHandler):
	def get(self):
		if self.current_user:
			self.render('completeInfo.html',state=1,user=self.current_user)
		else:
			self.render('index.html',state=0,user=self.current_user)