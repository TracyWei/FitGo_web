# -*- coding: utf-8 -*-
#!/usr/bin/env python
#@date  :2015-3-from
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
from tornado.options import define, options
import pymongo
from pymongo import MongoClient

from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from UI_moudles.UI_moudle import *
from mod.auth.Code_Handler import CodeHandler

from mod.auth.Login_Handler import LoginHandler
from mod.auth.Logout_Handler import LogoutHandler
from mod.auth.Register_Handler import RegisterHandler,VerifyHandler
from mod.auth.Base_Handler import BaseHandler
from mod.auth.Password_Handler import PasswordHandler

from mod.user.UserInfo_Handler import UserinfoHandler
from mod.user.Usertopic_Handler import UsertopicHandler
from mod.user.UserPage_Handler import UserPageHandler
from mod.user.UploadPortrait_Handler import UploadPortraitHandler

from mod.plans.Plans_Handler import PlansHandler
from mod.plans.CompleteInfoHandler import CompleteInfoHandler
from mod.plans.Lookplans_Handler import LookplansHandler
from mod.plans.ChangePorHandler import ChangePorHandler
from mod.plans.ForOthersHandler import ForOthersHandler

from mod.index.index import IndexHandler
from mod.index.Hot_Handler import HotHandler

from mod.activity.ActivityPage_Handler import ActivityPageHandler
from mod.activity.CreateActivity_Handler import CreateActivityHandler
from mod.activity.SearchActivity_Handler import SearchActivityHandler
from mod.activity.AddActivity_Handler import AddActivityHandler

from mod.invite.InvitePage_Handler import InvitePageHandler
from mod.invite.Invite_Handler import InviteHandler
from mod.invite.SearchInvite_Handler import SearchInviteHandler
from mod.invite.RequestInvite_Handler import RequestInviteHandler
from mod.invite.RespondInvite_Handler import RespondInviteHandler
from mod.invite.RespondList_Handler import RespondListHandler
from mod.invite.RespondDetailList_Handler import RespondDetailListHandler
from mod.invite.Evaluate_Handler import EvaluateHandler
from mod.invite.EvaluateList_Handler import EvaluateListHandler

from mod.recom.RecomUser_Handler import RecomUserHandler
from mod.recom.RecomInvite_Handler import RecomInviteHandler
from mod.recom.RecomActivity_Handler import RecomActivityHandler

from mod.discover.DiscoverPage_Handler import DiscoverPageHandler
from mod.discover.CreateState_Handler import CreateStateHandler
from mod.discover.SearchState_Handler import SearchStateHandler
from mod.discover.UploadPic_Handler import UploadPicHandler
from mod.discover.JoinState_Handler import JoinStateHandler
from mod.discover.AddFriend_Handler import AddFriendHandler
from mod.discover.AllFriends_Handler import AllFriendsHandler
from mod.discover.DeleteFriend_Handler import DeleteFriendHandler
from mod.discover.SearchFriend_Handler import SearchFriendHandler
# from mod.discover.RecomUser_Handler import RecomUserHandler
# from mod.recommend.RecomUser_Handler import RecomUserHandler

# from mod.recommend.RecomUser_Handler import RecomPicHandler




define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',IndexHandler),
            (r'/body',BodyHandler),
            (r'/auth/code/(\d+[.]\d+)',CodeHandler),
            (r'/auth/login',LoginHandler),
            (r'/auth/logout', LogoutHandler),
            (r'/auth/register/verify',VerifyHandler),
            (r'/auth/register',RegisterHandler),
            (r'/auth/password',PasswordHandler),
            (r'/hot',HotHandler),
            
            (r'/user/usertopic',UsertopicHandler),
            (r'/user/userpage/([\S]+)',UserPageHandler),
            (r'/user/userinfo/([\S]+)',UserinfoHandler),
            (r'/user/userinfopic/portrait',UploadPortraitHandler),

            (r'/invite/user_page',InvitePageHandler),
            (r'/invite',InviteHandler),
            (r'/invite/search',SearchInviteHandler),
            (r'/invite/request',RequestInviteHandler),
            (r'/invite/respond',RespondInviteHandler),
            (r'/invite/respondlist',RespondListHandler),
            (r'/invite/responddetaillist',RespondDetailListHandler),
            (r'/invite/evaluate',EvaluateHandler),
            (r'/invite/evaluatelist',EvaluateListHandler),


            (r'/activity',ActivityPageHandler),
            (r'/activity/create',CreateActivityHandler),
            (r'/activity/search',SearchActivityHandler),
            (r'/activity/add',AddActivityHandler),

            (r'/discover/discover_page',DiscoverPageHandler),
            (r'/discover/add/(\d+)',AddFriendHandler),
            (r'/discover/delete/(\d+)',DeleteFriendHandler),
            (r'/discover/allfriends',AllFriendsHandler),
            (r'/discover/search/friends',SearchFriendHandler),
            (r'/discover/create',CreateStateHandler),
            (r'/discover/search/state',SearchStateHandler),
            (r'/discover/create/state/pic',UploadPicHandler),
            (r'/discover/join',JoinStateHandler),
            
            (r'/plans',PlansHandler),
            (r'/plans/Info',CompleteInfoHandler),
            (r'/plans/detail',LookplansHandler),
            (r'/plans/Info/changePor',ChangePorHandler),
            (r'/plans/forothers',ForOthersHandler),
            
            (r'/recom/recomuser',RecomUserHandler),
            (r'/recom/recomactivity',RecomActivityHandler),
            (r'/recom/recominvite',RecomInviteHandler),
            ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            auth_path=os.path.join(os.path.dirname(__file__),'auth'),
            discover_path=os.path.join(os.path.dirname(__file__),'discover'),
            activity_path=os.path.join(os.path.dirname(__file__),'activity'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={
                        'header':HeaderMoudle,
                        'footer':FooterMoudle,
                        'act_join_people':act_join_peopleMoudle,
                        'plan_item':plan_itemMoudle,
                        'discover_state':DiscoverStateMoudle,
                        'discover_friend':DiscoverFriendMoudle,
                        'plan_show_item':Plan_show_itemMoudle,
                        'plan_show':Plan_showMoudle,
                        'mystate_show':State_showMoudle
                        },

            # xsrf_cookies=True,
            login_url="/auth/login",
            # static_url_prefix = os.path.join(os.path.dirname(__file__), '/images/'),
            debug=True
            # "lohin_url":"/auth/LoginHandler"
            
        )

        conn = MongoClient('115.28.27.150', 27017)
        self.Mongodb = conn["fitgo"]
        self.Mongodb.authenticate('fitgouser','fitgo2015')
        #conn = pymongo.Connection("123.57.221.18", 27017)
        #self.db = conn["fitgo"]

        tornado.web.Application.__init__(self, handlers,**settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))
class BodyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('body.html')

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
