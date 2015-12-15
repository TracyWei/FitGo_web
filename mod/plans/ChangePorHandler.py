# -*- coding: utf-8 -*-
import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler

class ChangePorHandler(BaseHandler):
	def get(self):
		if self.current_user:
			self.render('changePor.html',state=1,user=self.current_user)
		else:
			self.render('index.html',state=0,user=self.current_user)
