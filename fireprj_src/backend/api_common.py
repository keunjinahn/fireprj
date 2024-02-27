print ("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, g
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime, timedelta
import os
import json
from functools import wraps

from backend import app, login_manager
from backend_model.table_fireprj import *
from backend import manager
db = DBManager.db

manager.create_api(FireSensorTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='sensor'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(FireRepeaterTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='repeater'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(FireReceiverTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='receiver'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

def get_realtime_sensor(result=None, **kw):
    res = result['objects']
    all_logs = EventLogTbl.query.all()
    for sensor in res:
        sensor['regist_status'] = True #등록상태: 센서의 데이터가 존재하면 무조건 True
        last_sensor_log = list(filter(lambda x: x.sensor_id == sensor['sensor_id'], all_logs))
        if len(last_sensor_log) > 0: last_sensor_log = last_sensor_log[-1]
        else: sensor['action_status'] = sensor['network_status'] = sensor['battery_status'] = False; continue
        offset_time = datetime.now() - timedelta(minutes=1)
        sensor['receiver_type'] = last_sensor_log.receiver_type
        sensor['event_datetime'] = last_sensor_log.event_datetime
        sensor['action_status'] = sensor['network_status'] = sensor['battery_status'] \
        = True if last_sensor_log.event_datetime >= offset_time else False #1분 이내의 데이터가 있으면 True

manager.create_api(FireSensorTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='sensor_event'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , postprocessors={
                       'GET_MANY': [get_realtime_sensor]
                   })

manager.create_api(EventLogTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='event_list'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(EventTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='sensor_analysis'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

manager.create_api(UserTbl
                   , results_per_page=10000
                   , url_prefix='/api/v1'
                   , collection_name='user'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True)

