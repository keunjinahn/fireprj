# -*- coding: utf-8 -*-
print ("module [backend.api_monitor] loaded")

from backend.api_common import *
from backend_model.table_typhoon import *
from sqlalchemy import sql
import random
db = DBManager.db
