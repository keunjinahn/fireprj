# -*- coding: utf-8 -*-
print ("module [backend.api_monitor] loaded")

from backend_model.table_typhoon import *
from sqlalchemy import sql
import json
def get_typhoon_name(typhoon_name):
    try :
        _typhoon_name = str(typhoon_name).split(',')[0].replace("태풍",'').strip()

        if _typhoon_name[0] != '제' :
             typhoon = Typhoons.query.filter(Typhoons.typhoon_name.like('%' +_typhoon_name + '%')).first()
             if typhoon is not None:
                new_typhoon_name = '제' + typhoon.typhoon_number[4:6] + '호 태풍 ' + _typhoon_name
                return new_typhoon_name
    except :
        pass
    return typhoon_name

def get_school_info_from_json(json_data,group_key,cost_key,group_key2=None,cost_key2=None,ext_cost_key=None):
    info = {
        "count":0,
        "cost":0
    }
    try :
        data_ = json.loads(json_data)
        #print("data :",json_data)
        if group_key is not None and group_key in data_.keys() :
            info["count"] = sum(1 if cost_key in item.keys() and  item[cost_key] != '' else 0 for item in data_[group_key] )
            info["cost"] = sum(item[cost_key] if cost_key in item.keys()  and  item[cost_key] != '' else 0 for item in data_[group_key] )
    #         if ext_cost_key is not None:
    #             info["count"] += sum(1 if ext_cost_key in item.keys() and item[ext_cost_key] != '' else 0 for item in data_[group_key2] )
    #             info["cost"] += sum(item[ext_cost_key] if ext_cost_key in item.keys()  and  item[ext_cost_key] != ''  else 0 for item in data_[group_key] )
    #             print("info ==>:",info)
        if group_key2 is not None and group_key2 in data_.keys() :
            info["count"] += sum(1 if cost_key2 in item.keys() and item[cost_key2] != '' else 0 for item in data_[group_key2] )
            info["cost"] += sum(item[cost_key2] if cost_key2 in item.keys() and  item[cost_key2] != '' else 0 for item in data_[group_key2] )

    except :
        pass
    return info

def get_school_info_from_json_ext(school_info,json_data,group_key,cost_key,group_key2=None,cost_key2=None,ext_cost_key=None):
    info = {
        "count":0,
        "cost":0
    }
    try :
        data_ = json.loads(json_data)
        #print("data :",json_data)
        if group_key is not None and group_key in data_.keys() :
            info["count"] = sum(1 if cost_key in item.keys() and  item[cost_key] != '' else 0 for item in data_[group_key] )
            info["cost"] = sum(item[cost_key] if cost_key in item.keys()  and  item[cost_key] != '' else 0 for item in data_[group_key] )
    #         if ext_cost_key is not None:
    #             info["count"] += sum(1 if ext_cost_key in item.keys() and item[ext_cost_key] != '' else 0 for item in data_[group_key2] )
    #             info["cost"] += sum(item[ext_cost_key] if ext_cost_key in item.keys()  and  item[ext_cost_key] != ''  else 0 for item in data_[group_key] )
    #             print("info ==>:",info)
        if group_key2 is not None and group_key2 in data_.keys() :
            info["count"] += sum(1 if cost_key2 in item.keys() and item[cost_key2] != '' else 0 for item in data_[group_key2] )
            info["cost"] += sum(item[cost_key2] if cost_key2 in item.keys() and  item[cost_key2] != '' else 0 for item in data_[group_key2] )
        if cost_key == 's3_total_3':
            info["cost"] =school_info.sub6_gubun234
        elif cost_key == 's3_total_7':
            info["cost"] =school_info.sub6_gubun7
        elif cost_key == 's3_total_5':
            info["cost"] =school_info.sub6_gubun5
        elif cost_key == 's3_total_9':
            info["cost"] =school_info.sub6_gubun910
    except :
        pass
    return info

def get_typhoon_name_from_db(typhoon):
    _typhoon_num = typhoon.typhoon_number[4:]
    typhoon_name = '제' + str(_typhoon_num) + "호 태풍 " + typhoon.typhoon_name
    return typhoon_name

def getJsonGroup12(json_data):
    info = {
        "count":0,
        "cost":0
    }
    try :
        data_ = json.loads(json_data)
        #print("data :",json_data)
        for data in data_['s3_12']:
            if 'final_total' in data :
                info['count'] += 1
                info['cost'] += data['final_total']
    except :
        pass
    #print("info :",info)
    return info
