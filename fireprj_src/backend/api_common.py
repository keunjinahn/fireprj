# -*- coding: utf-8 -*-
print ("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, g
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime
import os
import json
from functools import wraps
import requests

from backend import app, login_manager
from backend_model.table_typhoon import *
from backend_model.table_school import *
from backend import manager
from backend.api_utils import *
import glob
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(id):
    user = DBManager.db.session.query(Users).get(id)
    return user


@app.route('/api/monitor/v1/login', methods=['POST'])
def login_api():
    data = json.loads(request.data)
    result = ''

    if data['user_id'] is not None and data['user_pw'] is not None:
        print("user_id :",data['user_id'],",user_pw :",data['user_pw'])
        if data['login_type'] == 2:  # 회원 및 학교 로그인만 체크
            # https://school0.edufa.or.kr:8443//mgrfa/enu/loginChk.json?userid=M6761&password=0000
            req_url = "https://school0.edufa.or.kr:8443//mgrfa/enu/loginChk.json?userid=" + data['user_id'] + "&password=" + data['user_pw']
#             req_url = "https://school0.edufa.or.kr:8443//mgrfa/enu/loginChk.json?userid=M6761&password=0000"
            res = requests.post(req_url, verify=False)
            res_json = json.loads(res.text)

            if res_json['enuVO']['resultCode'] == "0000":
                loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
                sub_group_name = ''
                sub_school_name = ''
                if loginuser is None:  # Insert
                    fk_school_id = -1
                    if data['user_id'][0] == 'M':
                        sb = SubGroups.query.filter(SubGroups.sub_group_id == data['user_id']).first()
                        if sb is not None:
                            sub_group_name = sb.sub_group_name
                    elif data['user_id'][0] == 'S':
                        ss = SubSchools.query.filter(SubSchools.sub_school_id == data['user_id']).first()
                        if ss is not None:
                            sub_school_name = ss.sub_school_name
                            sub_group_name = ss.sub_group_name

                    new_user = Users()
                    new_user.user_id = data['user_id']
                    new_user.user_pw = password_encoder_512(data["user_pw"])
                    new_user.user_name = res_json['enuVO']['charger_nm']
                    new_user.user_type = 5 if data['user_id'][0] == 'M' else 6
                    new_user.user_status = 1
                    new_user.phone = res_json['enuVO']['tel_no']
                    new_user.email = res_json['enuVO']['user_email']
                    new_user.area_code = res_json['enuVO']['city_nm']
                    new_user.sub_group_name = sub_group_name
                    new_user.sub_school_name = sub_school_name
                    db.session.add(new_user)
                else:  # Update
                    db.session.query(Users).filter(Users.user_id == data["user_id"]) \
                        .update(dict(user_pw=password_encoder_512(data["user_pw"]),
                                     user_name=res_json['enuVO']['charger_nm'],
                                     phone=res_json['enuVO']['tel_no'],
                                     email=res_json['enuVO']['user_email']
                                     ))
                db.session.commit()

        loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()

        if loginuser is None:
            result = {'status': False, 'reason': 1}  # ID 없음
        else:
            print("user_pw :",data["user_pw"])
            if loginuser.user_pw != password_encoder_512(data["user_pw"]):
                result = {'status': False, 'reason': 2} # PW 틀림

            else:  # Login 성공
                if loginuser.user_status == 0:
                    result = {'status': False, 'reason': 3}  # Activation 안됨
                else:
#                     if data['login_type'] == 1 and loginuser.user_type >= 5:
#                         result = {'status': False, 'reason': 4}  # 한국교육시설안전원 탭에서 회원 및 학교로 로그인 했을 경우
#                     elif data['login_type'] == 2 and loginuser.user_type < 5:
#                         result = {'status': False, 'reason': 5}  # 회원 및 학교 탭에서 한국교육시설안전원 계정으로 로그인 했을 경우
#                     else:
                    loginuser.last_logon_time = datetime.now()
                    loginuser.token = generate_token(data['user_id'])
                    db.session.query(Users).filter(Users.user_id == data["user_id"])\
                        .update(dict(last_logon_time=loginuser.last_logon_time, token=loginuser.token))

                    new_access_history = AccessHistory()
                    new_access_history.type = 0  # Login
                    user_agent = request.environ.get('HTTP_USER_AGENT')
                    new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(user_agent)
                    new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    new_access_history.update_time = datetime.now()
                    new_access_history.user_id = loginuser.user_id
                    new_access_history.FK_user_id = loginuser.id
                    db.session.add(new_access_history)
                    db.session.commit()

                    result = {'status': True, 'reason': 0, 'user': loginuser.serialize()}

    return make_response(jsonify(result), 200)

# @app.route('/api/monitor/v1/login', methods=['POST'])
# def login_api():
#     data = json.loads(request.data)
#     result = ''
#     if data['user_id'] is not None and data['user_pw'] is not None:
#         loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
#
#         if loginuser is None:
#             result = {'status': False, 'reason': 1}  # ID 없음
#         else:
#             if loginuser.user_pw != password_encoder_512(data["user_pw"]):
#                 result = {'status': False, 'reason': 2} # PW 틀림
#
#             else:  # Login 성공
#                 if loginuser.user_status == 2:
#                     result = {'status': False, 'reason': 3}  # Activation 안됨
#                 else:
#                     loginuser.last_logon_time = datetime.now()
#                     loginuser.token = generate_token(data['user_id'])
#                     db.session.query(Users).filter(Users.user_id == data["user_id"])\
#                         .update(dict(last_logon_time=loginuser.last_logon_time, token=loginuser.token))
#
#                     new_access_history = AccessHistory()
#                     new_access_history.type = 0  # Login
#                     user_agent = request.environ.get('HTTP_USER_AGENT')
#                     new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(user_agent)
#                     new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#                     new_access_history.update_time = datetime.now()
#                     new_access_history.user_id = loginuser.user_id
#                     new_access_history.FK_user_id = loginuser.id
#                     db.session.add(new_access_history)
#                     db.session.commit()
#
#                     result = {'status': True, 'reason': 0, 'user': loginuser.serialize()}
#
#     return make_response(jsonify(result), 200)

@app.route("/api/monitor/v1/logout", methods=["POST"])
def logout_api():
    print("logout_api 1")
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    result = ''
    if token is None:
        print("token is none")
    print("logout_api 2")
    print("token :",token)
    loginUser = Users.query.filter_by(token=token).first()
    if loginUser is None:
        print("user is none")
    else:
        print("logout_api 3")
        new_access_history = AccessHistory()
        new_access_history.type = 1  # Logout
        userAgent = request.environ.get('HTTP_USER_AGENT')
        new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(userAgent)
        new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        new_access_history.update_time = datetime.now()
        new_access_history.user_id = loginUser.user_id
        new_access_history.fk_user_id = loginUser.id

        db.session.add(new_access_history)
        db.session.commit()
        print("logout_api 4")
    return make_response(jsonify(result), 200)

def generate_token(userID):
    m = hashlib.sha1()

    m.update(userID.encode('utf-8'))
    m.update(datetime.now().isoformat().encode('utf-8'))

    return m.hexdigest()

def validate_token(token):
    user = Users.query.filter_by(token=unicode(token)).first()
    ## 개발시에 주석을 풀고 자동로그인 환경 구성
    ##user = Users.query.filter_by(userID=unicode('sorang.kang@lge.com')).first()

    if user is None:
        return None
    elif user.enable_login is False:
        raise ProcessingException(description="Not Authorized", code=410)
    elif user.userType == app.config['USER_TYPE_USER']:
        manager = Users.query.filter_by(id=user.FK_manager_id).first()
        if manager is not None:
            if manager.enable_login is False:
                raise ProcessingException(description="Not Authorized", code=410)

    return user

def check_token(search_params=None, **kw):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    print("token:",token)
    user = Users.query.filter_by(token=token).first()
    if user is None:
        raise ProcessingException(description="Not Authorized", code=411)
    print("user:",user.user_id)

    #user = dict()

    #return user


def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="headers")
        token = parser.parse_args()["token"]
        print("token:", token)
        user = Users.query.filter_by(token=token).first()
        if user is None:
            raise ProcessingException(description="Not Authorized", code=411)
        print("user:", user.user_id)
        g.user = user
        return fn(*args, **kwargs)
    return decorated


def password_encoder_512(password):
    h = hashlib.sha512()
    h.update(password.encode('utf-8'))
    return h.hexdigest()


manager.create_api(Schools
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })


def prePasswdUpdate(input_params=None, **kw):
    if 'user_pw' in kw['data']:
        kw['data']['user_pw'] = password_encoder_512(kw['data']['user_pw'])

manager.create_api(Users
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='users'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token,prePasswdUpdate],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })


def post_typhoon_with_paths(result=None, **kw):

    print("parent_typhoon_id :",result['parent_typhoon_id'])
    if result['parent_typhoon_id'] is not -1:
        typhoon = Typhoons.query.filter_by(id=result['parent_typhoon_id']).first()
        print("typhoon :",typhoon.id)
        if typhoon is not None :
            paths_list = Paths.query.filter_by(fk_typhoon_id=typhoon.id).order_by(Paths.latitude.asc()).all()
            print("path len :",len(paths_list))
            for paths in paths_list :
                new_path = Paths()
                new_path.latitude = paths.latitude
                new_path.longitude = paths.longitude
                new_path.center_pressure = paths.center_pressure
                new_path.max_speed_s = paths.max_speed_s
                new_path.max_speed_h = paths.max_speed_h
                new_path.wind_radius = paths.wind_radius
                new_path.storm_radius = paths.storm_radius
                new_path.strength = paths.strength
                new_path.direction = paths.direction
                new_path.move_speed_h = paths.move_speed_h
                new_path.fk_typhoon_id = result['id']
                new_path.direction = paths.direction
                new_path.direction = paths.direction
                new_path.modify_date = paths.modify_date
                new_path.created_date = paths.created_date
                db.session.add(new_path)
            db.session.commit()

manager.create_api(Typhoons
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='typhoons'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   },postprocessors={
                        'POST': [post_typhoon_with_paths]
                   })


manager.create_api(Paths
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='paths'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })


manager.create_api(Accidents
                   , results_per_page=10000
                   , max_results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='accidents'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })

def post_AccidentPredictList(result=None, **kw):
    res = result['objects']


manager.create_api(AccidentsPredict
                   , results_per_page=10000
                   , max_results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='accidents_predict'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   },
                   postprocessors={
                        'GET_MANY': [post_AccidentPredictList]
                   })

manager.create_api(Deeps
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })

def post_typoonreport_past_list(result=None, **kw):
    res = result['objects']
    for acci_past in res:
        print("acci_past['fk_typhoon_id'] :",acci_past['fk_typhoon_id'])
        typhoon = Typhoons.query.filter_by(id=acci_past['fk_typhoon_id']).first()
        # print(" fk_typhoon_id : ",acci_past['fk_typhoon_id'])
        print("sub2_disaster_naming 1 :",acci_past['sub2_disaster_naming'])
        if typhoon is not None :
            acci_past['sub2_disaster_naming'] = get_typhoon_name_from_db(typhoon)
        else :
            acci_past['sub2_disaster_naming'] = str(acci_past['sub2_disaster_naming']).replace('&#39;',' ').rstrip()
            name = str(acci_past['sub2_disaster_naming']).replace('(',' ').replace(')',' ').rstrip()
            # print(" name 1: ",name)
            name = name.split(' ')[-1]
            # print(" name 2: ",name)
            typhoon2 = Typhoons.query.filter_by(typhoon_v_type=0).filter(Typhoons.typhoon_name.like("%" + name + "%")).first()
            if typhoon2 is not None :
                # print(" typhoon name: ",typhoon2.typhoon_name)
                # print(" sub2_disaster_naming name: ",get_typhoon_name_from_db(typhoon2))
                acci_past['sub2_disaster_naming'] = get_typhoon_name_from_db(typhoon2)
        print("sub2_disaster_naming 2 :",acci_past['sub2_disaster_naming'])
#     for acci_past in res:
#         #print("app : ", app)
#         arry_data15 = str(acci_past['s3_data15']).split(',')
#         data15_list = []
#         for data15 in arry_data15:
#             code_set = TB_CODE_SET.query.filter_by(code=data15).first()
#             if code_set is not None :
#                 data15_list.append(code_set.name)
#         acci_past['s3_data15'] = ','.join(data15_list)
#
#         arry_data16 = str(acci_past['s3_data16']).split(',')
#         data16_list = []
#         for data16 in arry_data16:
#             code_set = TB_CODE_SET.query.filter_by(code=data16).first()
#             if code_set is not None :
#                 data16_list.append(code_set.name)
#         acci_past['s3_data16'] = ','.join(data16_list)
#
#         arry_data17 = str(acci_past['s3_data17']).split(',')
#         data17_list = []
#         for data17 in arry_data17:
#             code_set = TB_CODE_SET.query.filter_by(code=data17).first()
#             if code_set is not None :
#                 data17_list.append(code_set.name)
#         acci_past['s3_data17'] = ','.join(data17_list)

manager.create_api(TB_TYPOONREPORT
                   , results_per_page=10000
                   , max_results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='accidentpast'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   },postprocessors={
                        'GET_MANY': [post_typoonreport_past_list]
                   })

def get_os_browser_from_useragent(userAgent):
    os_ver = "Unknown"
    browser_ver = "Unknown"

    if userAgent.find("Linux") != -1:
        os_ver = "Linux"
    elif userAgent.find("Mac") != -1:
        os_ver = "MacOS"
    elif userAgent.find("X11") != -1:
        os_ver = "UNIX"
    elif userAgent.find("Win") != -1:
        os_ver = "Windows"

    if userAgent.find("MSIE 6") != -1:
        browser_ver = "Internet Explorer 6"
    elif userAgent.find("MSIE 7") != -1:
        browser_ver = "Internet Explorer 7"
    elif userAgent.find("MSIE 8") != -1:
        browser_ver = "Internet Explorer 8"
    elif userAgent.find("MSIE 9") != -1:
        browser_ver = "Internet Explorer 9"
    elif userAgent.find("MSIE 10") != -1:
        browser_ver = "Internet Explorer 10"
    elif userAgent.find("Trident") != -1 or userAgent.find("trident") != -1:
        browser_ver = "Internet Explorer 11"
    elif userAgent.find("Firefox") != -1:
        browser_ver = "Firefox"
    elif userAgent.find("Opera") != -1:
        browser_ver = "Opera"
    elif userAgent.find("Chrome") != -1:
        browser_ver = "Chrome"
    elif userAgent.find("Safari") != -1 or userAgent.find("Chrome") == -1:
        browser_ver = "Safari"
    elif userAgent.find("Edge") != -1 or userAgent.find("edge") != -1:
        browser_ver = "Microsoft Edge"

    return os_ver, browser_ver


def date_encoder(thing):
    list_date = str(thing).split(":")

    if hasattr(thing, 'isoformat'):
        if len(list_date[0]) == 1:
            return "0" + thing.isoformat()
        return thing.isoformat()
    else:
        if len(list_date[0]) == 1:
            return "0" + str(thing)
        return str(thing)

manager.create_api(AccessHistory
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='access_history'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })

def post_community_list(result=None, **kw):
    res = result['objects']
    for community in res:
        resComm = Community.query.filter_by(parent_id=community['id']).first()
        if resComm is not None :
            community['response_id'] = resComm.id

manager.create_api(Community
                   , results_per_page=10000
                   , url_prefix='/api/monitor/v1'
                   , collection_name='community'
                   , methods=['GET', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
#                         'GET_MANY': [check_token]
                   },postprocessors={
                        'GET_MANY': [post_community_list]
                   })

@app.route('/api/monitor/v1/login_overlap', methods=['POST'])
def login_overlap_api():
    data = json.loads(request.data)
    result = ''
    print("data:",data)
    if data['user_id'] is not None:
        loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
        if loginuser is not None:  # Insert
            result = {'status': True, 'reason': 0, 'overlap_result': 0}
        else :
            result = {'status': True, 'reason': 0, 'overlap_result': 1}

    return make_response(jsonify(result), 200)

@app.route('/api/monitor/v1/user_register', methods=['POST'])
def user_register_api():
    data = json.loads(request.data)
    result = ''
    print("data:",data)
    if data['user_id'] is not None:
        user = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
        if user is None:  # Insert
            new_user = Users()
            new_user.user_id = data['user_id']
            new_user.user_pw = password_encoder_512(data["user_passwd"])
            new_user.user_name = data['user_name']
            new_user.user_type = data['user_type']
            new_user.area_code = data['area_code']
            new_user.dept_name = data['dept_name']
            new_user.user_status = data['user_status']
            new_user.phone = data['phone']
            new_user.telephone = data['telephone']
            new_user.email = data['user_id'] + '@koies.or.kr'
            new_user.fk_school_id = -1
            db.session.add(new_user)
            db.session.commit()
            result = {'status': True, 'reason': 0, 'register_result': 1}
        else :
            result = {'status': True, 'reason': 0, 'register_result': 0}

    return make_response(jsonify(result), 200)

@app.route('/api/monitor/v1/user_update', methods=['POST'])
@token_required
def user_update_api():
    data = json.loads(request.data)
    result = ''
    print("data:",data)
    if data['id'] is not None:
        user = db.session.query(Users).filter(Users.id == data["id"]).first()
        if user is not None:  # Update
            object = {}
            if "user_id" in data :
                object['user_id'] = data['user_id']
            if "user_name" in data :
                object['user_name'] = data['user_name']
            if "user_type" in data :
                object['user_type'] = data['user_type']
            if "area_code" in data :
                object['area_code'] = data['area_code']
            if "user_status" in data :
                object['user_status'] = data['user_status']
            if "phone" in data :
                object['phone'] = data['phone']
            if "telephone" in data :
                object['telephone'] = data['telephone']
            if "dept_name" in data :
                object['dept_name'] = data['dept_name']
            if "user_passwd" in data :
                object['user_pw'] = password_encoder_512(data["user_passwd"])
            print("Object : ",object)
            db.session.query(Users).filter(Users.id == user.id).update(object)
            db.session.commit()
            result = {'status': True, 'reason': 0, 'update_result': 1}
        else :
            result = {'status': True, 'reason': 0, 'update_result': 0}

    return make_response(jsonify(result), 200)

manager.create_api(Settings
                   , results_per_page=1
                   , url_prefix='/api/monitor/v1'
                   , collection_name='settings'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [check_token]
                   })


@app.route('/api/monitor/v1/update_typhoon_paths_from_csv', methods=['POST'])
def update_typhoon_paths_from_csv_api():
    npd_file_search_path = './data/*'
    print("npd_file_search_path :",npd_file_search_path)
    files = glob.glob(npd_file_search_path)
    for file in files:
        print("file : ", file)
        typhoon_num = file.split('/')[-1].split('.')[0].split('\\')[-1]
        print("typhoon_num :",typhoon_num)
        typhoon = Typhoons.query.filter_by(typhoon_number=typhoon_num).filter_by(typhoon_v_type=0).first()
        if typhoon is not None:
            db.session.query(Paths).filter_by(fk_typhoon_id=typhoon.id).delete()
            db.session.commit()
            f = open(file, 'r',encoding='euc-kr')
            lines = f.readlines()
            print("lines len : ",len(lines))
            for index,line in reversed(list(enumerate(lines))):
                print("index :",index,",line : ",line)
                line_array = line.replace('\ufeff','').split(',')
                new_path = Paths()
                new_path.created_date = datetime.strptime(line_array[0],"%Y-%m-%d %H:%M")
                new_path.modify_date = datetime.strptime(line_array[0],"%Y-%m-%d %H:%M")
                
                new_path.latitude = float(line_array[1])
                new_path.longitude = float(line_array[2])
                new_path.center_pressure = int(line_array[3])
                new_path.max_speed_s = int(line_array[4])
                new_path.max_speed_h = int(line_array[5])
                new_path.wind_radius = -1 if line_array[6]== '-' else int(line_array[6])
                new_path.storm_radius = str(line_array[7])
                new_path.strength = line_array[8]
                new_path.direction = line_array[9]
                new_path.move_speed_h = int(line_array[10])
                new_path.fk_typhoon_id = typhoon.id
                db.session.add(new_path) 
            db.session.commit()                 
            f.close()              
    return make_response(jsonify(''), 200)