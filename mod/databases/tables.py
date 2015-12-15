#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float 
from sqlalchemy.orm import relationship,backref
from db import engine,Base

class UsersCache(Base):
	__tablename__ = 'Users'

	uid = Column(VARCHAR(64),primary_key=True)
	name = Column(VARCHAR(64),nullable=True)
	student_card = Column(VARCHAR(64),nullable=True)
	student_id = Column(VARCHAR(64),nullable=True)
	gender = Column(VARCHAR(64))
	signature = Column(VARCHAR(64))
	school = Column(VARCHAR(64))
	campus = Column(VARCHAR(64))
	password = Column(VARCHAR(64))
	salt = Column(VARCHAR(64))
	info_email = Column(VARCHAR(64))
	info_phone = Column(VARCHAR(64))
	portrait = Column(VARCHAR(64))
	cos = Column(Float)
class CookieCache(Base):
	__tablename__ = "Cookie"

	id = Column(Integer,primary_key=True)
	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'))
	cookie = Column(VARCHAR(64))

class PlansCache(Base):
	__tablename__ = 'Plans'

	plan_id = Column(Integer,primary_key=True)
	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'))
	fit_item = Column(VARCHAR(64))


class InviteCache(Base):
	__tablename__ = 'Invite'

	_id = Column(Integer,primary_key = True)
	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'))
	name = Column(VARCHAR(64),nullable=True)
	start_time = Column(VARCHAR(64))
	end_time = Column(VARCHAR(64))
	create_time = Column(VARCHAR(64))
	fit_location = Column(VARCHAR(64))
	fit_item = Column(VARCHAR(64))
	item_tag = Column(VARCHAR(64))#自定义和系统提供
	gender = Column(VARCHAR(64))
	remark = Column(VARCHAR(64))#备注
	cos = Column(Float)
class Invite_relation(Base):
	__tablename__ = 'Invite_relation'

	id = Column(Integer,primary_key = True)
	uid_request = Column(VARCHAR(64))
	request_name = Column(VARCHAR(64))
	uid_respond = Column(VARCHAR(64))#发起项目的人
	respond_name = Column(VARCHAR(64))
	respond_phone = Column(VARCHAR(64))
	fit_item = Column(VARCHAR(64))
	state = Column(VARCHAR(8)) 
	grade = Column(VARCHAR(64))
	_id = Column(Integer,ForeignKey('Invite._id',ondelete='CASCADE'))
	fit_item = Column(VARCHAR(64))
	score = Column(VARCHAR(64))
	comment = Column(VARCHAR(64))
	comment_state = Column(VARCHAR(8))#0->not able to comment,1->able to comment
	
	relationship('Invite',backref='Invite_relation')

class User_tagCache(Base):
	__tablename__ = 'User_tag'

	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'),primary_key=True)
	user_enjoyment = Column(VARCHAR(64))
	user_join_times = Column(Integer)
	user_score = Column(VARCHAR(64))
	user_join_event = Column(VARCHAR(64))
class ActCache(Base):
	__tablename__ = 'Act'

	act_id = Column(Integer,primary_key=True)
	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'))
	create_time = Column(VARCHAR(64))
	act_title = Column(VARCHAR(64))
	start_time = Column(VARCHAR(64))
	end_time = Column(VARCHAR(64))
	act_location = Column(VARCHAR(64))
	act_detail = Column(VARCHAR(64))
	act_join_uid = Column(Integer)
	cos = Column(Float)
class TopicsCache(Base):
	__tablename__ = 'Topics'

	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'))
	topic_id = Column(Integer,primary_key=True)
	topic_time = Column(VARCHAR(64))
	topic_content = Column(VARCHAR(64))
	topic_pic = Column(VARCHAR(64))
	pic_shape = Column(VARCHAR(64))
	topic_title = Column(VARCHAR(64))
	topic_starers = Column(Integer)
class SystemTagCache(Base):
	__tablename__ = "SystemTag"

	id = Column(Integer,primary_key=True)
	tag = Column(VARCHAR(64))
	hot_tag = Column(VARCHAR(64))
class RecommendItemCache(Base):
	__tablename__ = 'RecommendItem'

	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'),primary_key=True)
	item_id = Column(Integer)
	item_name = Column(VARCHAR(64))
# class CommentCache(Base):
# 	__tablename__ = 'Comment'

# 	uid = Column(VARCHAR(64),ForeignKey('Users.uid', ondelete='CASCADE'),primary_key=True)
# 	comment_id = Column(VARCHAR(64),nullable=True)
# 	score = Column(VARCHAR(64))
# 	comment = Column(VARCHAR(64))
# 	comment_state = Column(VARCHAR(8))#0->not comment,1->able to comment
