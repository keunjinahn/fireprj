print ("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, g
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime, timedelta
import os
import json
from functools import wraps
import openpyxl

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

manager.create_api(EventTbl
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

@app.route('/make-data/event-list', methods=['GET'])
def write_event_list_api():
    file_path = 'C:\\Users\\ansieun\\project\\fireprj\\doc\\화재감시시스템 이벤트 리스트_20240215.xlsx'
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.get_sheet_by_name('Sheet1')
    
    data = []
    for i, row in enumerate(sheet.rows):
        row_data = []
        for j, col in enumerate(row):
            if j < 2: continue
            row_data.append(col.value)
        if row_data[0] is not None: data.append(row_data)
    del data[0]

    table_list = ['system_id_c', 'repeater_id_c', 'sensor_id_c', 'sensor_value_c', 'inout_id_c', 'event_desc']
    for i, row in enumerate(data):
        obj = EventTbl()
        setattr(obj, 'event_idx', i+1)
        for j, col in enumerate(row):
            setattr(obj, table_list[j], col)
        db.session.add(obj)
    db.session.commit()
    return make_response(jsonify(''), 200)

@app.route('/make-data/generate_repeater', methods=['GET'])
def generate_repeater_api():
    receiver_data = FireReceiverTbl.query.all()

    for i, receiver in enumerate(receiver_data):
        for j in range(24):
            obj = FireRepeaterTbl()
            setattr(obj, 'repeater_idx', f'{(i*24)+(j+1):0>3}')
            setattr(obj, 'fk_customer_idx', 1)                      #고객식별자: 00001
            setattr(obj, 'receiver_id', receiver.receiver_id)
            setattr(obj, 'system_id', 0)                        #계통번호: 00
            setattr(obj, 'repeater_id', (i*24)+(j+1))
            db.session.add(obj)
    db.session.commit()
    return make_response(jsonify(''), 200)

@app.route('/make-data/generate_sensor', methods=['GET'])
def generate_sensor_api():
    repeater_data = FireRepeaterTbl.query.all()

    for i, repeater in enumerate(repeater_data):
        for j in range(24):
            obj = FireSensorTbl()
            setattr(obj, 'sensor_idx', (i*24)+(j+1))
            setattr(obj, 'fk_customer_idx', 1)                      #고객식별자: 00001
            setattr(obj, 'receiver_id', repeater.receiver_id)
            setattr(obj, 'system_id', 0)                        #계통번호: 00
            setattr(obj, 'repeater_id', repeater.repeater_id)
            setattr(obj, 'sensor_id', (i*24)+(j+1))
            db.session.add(obj)
        
        # 데이터 많아서 안들어감: 2*24*24 = 1152
        db.session.commit()
        if i > 2: break

    db.session.commit()
    return make_response(jsonify(''), 200)