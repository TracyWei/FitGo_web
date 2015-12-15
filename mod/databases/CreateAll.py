#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db import engine, Base
from tables import UsersCache,CookieCache,User_tagCache,ActCache,TopicsCache

Base.metadata.create_all(engine) #create all of Class which belonged to Base Class