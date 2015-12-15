# -*- coding: utf-8 -*-
#@date  :2015-3-from

import tornado.web

class HeaderMoudle(tornado.web.UIModule):
    def render(self):
        return self.render_string('header.html')

class FooterMoudle(tornado.web.UIModule):
    def render(self):
        return self.render_string('footer.html')
class activity_itemMoudle(tornado.web.UIModule):
    def render(self,content):
        return self.render_string('activity_item.html',content=content,icon=icon,num=num)
class act_join_peopleMoudle(tornado.web.UIModule):
    def render(self,content):
        return self.render_string('act_join_people.html',content=content)
class plan_itemMoudle(tornado.web.UIModule):
	def render(self,content1,content2):
		return self.render_string('plan_items.html',content=content1,content2=content2)
class Plan_show_itemMoudle(tornado.web.UIModule):
    def render(self,content_id,content):
        return self.render_string('plan_show_item.html',content_id=content_id,content=content)
class State_showMoudle(tornado.web.UIModule):
    def render(self,content_id,content):
        return self.render_string('mystate_show.html',content_id=content_id,content=content)
class DiscoverStateMoudle(tornado.web.UIModule):
    def render(self,content):
        return self.render_string('discover_state.html',content=content)
class DiscoverFriendMoudle(tornado.web.UIModule):
    def render(self,content):
        return self.render_string('discover_friend.html',content=content)
class Plan_showMoudle(tornado.web.UIModule):
    def render(self,content):
        return self.render_string('testlala.html',content=content)

