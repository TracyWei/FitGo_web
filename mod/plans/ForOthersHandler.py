# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado.web
import tornado.gen
from mod.auth.Base_Handler import BaseHandler

class ForOthersHandler(BaseHandler):
	def get(self):
		self.render('forothers.html',user=self.current_user)