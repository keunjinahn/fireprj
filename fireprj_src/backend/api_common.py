print ("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, g
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime
import os
import json
from functools import wraps
# import requests

from backend import app, login_manager
from backend_model.table_fireprj import *
# from backend_model.table_typhoon import *
# from backend_model.table_school import *
from backend import manager
# from backend.api_utils_ import *
import glob
db = DBManager.db

@app.route('/fireprj/test', methods=['GET'])
def fireprj_test():
    test = UserTbl.query.all()
    t = test[0]
    result = {col.name: getattr(t, col.name) for col in t.__table__.columns}
    print(result)
    return make_response(jsonify(''), 200)

manager.create_api(FireSensorTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1/sensor'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(FireRepeaterTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1/repeater'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(FireReceiverTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1/receiver'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)