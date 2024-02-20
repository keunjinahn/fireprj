# -*- coding: utf-8 -*-

print ("module [backend_model.table_school.py] loaded")
from backend_model.database import DBManager
db = DBManager.db

from datetime import datetime
class Schools(db.Model):
    __tablename__ = 'tb_school_info'
    id = db.Column('id', db.Integer, primary_key=True)
    school_id = db.Column('school_id', db.String(50), primary_key=True)
    school_name = db.Column('school_name', db.String(50))
    school_number = db.Column('school_number', db.String(50))
    school_type = db.Column('school_type', db.String(50))
    school_address = db.Column('school_address', db.String(100))
    latitude = db.Column('latitude', db.Float)
    longitude = db.Column('longitude', db.Float)
    acci_occu_count = db.Column('acci_occu_count', db.Integer, default=0)
    total_cost = db.Column('total_cost', db.Integer, default=0)


class Areas(db.Model):
    __tablename__ = 'tb_area'
    id = db.Column('id', db.Integer, primary_key=True)
    area_name = db.Column('area_name', db.String(50))


class SubGroups(db.Model):
    __tablename__ = 'tb_sub_group'
    id = db.Column('id', db.Integer, primary_key=True)
    sub_group_id = db.Column('sub_group_id', db.String(50))
    sub_group_name = db.Column('sub_group_name', db.String(50))
    sub_group_type = db.Column('sub_group_type', db.String(50))
    group_location = db.Column('group_location', db.String(50))
    user_name = db.Column('user_name', db.String(50))
    user_email = db.Column('user_email', db.String(50))
    user_tel = db.Column('user_tel', db.String(50))
    user_mobile = db.Column('user_mobile', db.String(50))
    sub_group_post = db.Column('sub_group_post', db.String(50))
    sub_group_address = db.Column('sub_group_address', db.String(50))
    created_date = db.Column('created_date', db.DateTime)
    modify_date = db.Column('modify_date', db.DateTime)


class SubSchools(db.Model):
    __tablename__ = 'tb_sub_school_info'

    id = db.Column('id', db.Integer, primary_key=True)
    sub_school_id = db.Column('sub_school_id', db.String(50))
    sub_school_name = db.Column('sub_school_name', db.String(50))
    sub_group_name = db.Column('sub_group_name', db.String(50))
    sub_school_email = db.Column('sub_school_email', db.String(50))
    sub_school_sub = db.Column('sub_school_sub', db.String(50))
    sub_school_type = db.Column('sub_school_type', db.String(50))
    sub_school_loc = db.Column('sub_school_loc', db.String(50))
    sub_school_alive_type = db.Column('sub_school_alive_type', db.String(50))
    sub_school_tel = db.Column('sub_school_tel', db.String(50))
    sub_school_mobile = db.Column('sub_school_mobile', db.String(50))
    sub_school_address = db.Column('sub_school_address', db.String(50))
    fk_sub_group_id = db.Column('fk_sub_group_id', db.Integer, db.ForeignKey(SubGroups.id))
    subgroups = db.relationship('SubGroups')
    latitude = db.Column('latitude', db.Float)
    longitude = db.Column('longitude', db.Float)
    sub_school_establish = db.Column('sub_school_establish', db.Integer)
    created_date = db.Column('created_date', db.DateTime)
    modify_date = db.Column('modify_date', db.DateTime)
    fk_area_id = db.Column('fk_area_id', db.Integer)


class Users(db.Model):
    __tablename__ = 'tb_users'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(48))
    user_pw = db.Column('user_pw', db.String(256))
    user_name = db.Column('user_name', db.String(48))
    sub_group_name = db.Column('sub_group_name', db.String(48))
    sub_school_name = db.Column('sub_school_name', db.String(48))
    area_code = db.Column('area_code', db.String(48))
    user_type = db.Column('user_type', db.Integer, default=4)  # 1:관리자, 2:공제사업처, 3:지역본부, 4:사용자, 5:회원(M~), 6:학교(S~)
    user_status = db.Column('user_status', db.Integer, default=1)  # 1:Active, 2:Deactive
    phone = db.Column('phone', db.String(30))
    telephone = db.Column('telephone', db.String(30))
    email = db.Column('email', db.String(48))
    token = db.Column('token', db.String(128))  # added
    last_logon_time = db.Column('last_logon_time', db.DateTime)
    created_date = db.Column('created_date', db.DateTime, default=datetime.now)
    password_date = db.Column('password_date', db.DateTime, default=datetime.now)
    dept_name = db.Column('dept_name', db.String(128))
    fk_school_id = db.Column('fk_school_id', db.Integer)

    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "sub_group_name": self.sub_group_name
            , "sub_school_name": self.sub_school_name
            , "area_code": self.area_code
            , "user_type": self.user_type
            , "user_status": self.user_status
            , "phone": self.phone
            , "telephone": self.telephone
            , "email": self.email
            , "token": self.token
            , "last_logon_time": self.last_logon_time
            , "created_date": self.created_date
            , "password_date": self.password_date
            , "dept_name": self.dept_name
            , "fk_school_id": self.fk_school_id
        }
        return resultJSON

class AccessHistory(db.Model):  # 접속 이력 테이블
    __tablename__ = 'tb_access_history'

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now)  # 생성시간
    user_id = db.Column('user_id', db.String(48)) # 유저 ID
    type = db.Column('type', db.Boolean)  # 0:로그인, 1:로그아웃
    update_time = db.Column('update_time', db.DateTime)  # 사용자 접속 시간
    ip_addr = db.Column('ip_addr', db.String(20))  # 사용자 접속IP
    os_ver = db.Column('os_ver', db.String(48))  # 사용자 접속 OS버전
    browser_ver = db.Column('browser_ver', db.String(48))  # 사용자 접속 브라우져 버전
    fk_user_id = db.Column('fk_user_id', db.Integer, db.ForeignKey(Users.id))
    user = db.relationship('Users')

class SCHOOL_XL(db.Model):
    __tablename__ = 'tb_school_xl_upload'
    id = db.Column('id', db.Integer, primary_key=True)
    unique_id = db.Column('unique_id', db.Integer)
    establish = db.Column('establish',db.String(50))
    local = db.Column('local',db.String(50))
    member_name = db.Column('member_name', db.String(50))
    school_name = db.Column('school_name', db.String(50))
    last_joined = db.Column('last_joined',db.String(50))
    building_num = db.Column('building_num', db.String(50))
    building_name = db.Column('building_name',db.String(50))
    class_use = db.Column('class_use', db.String(50))
    construction = db.Column('construction', db.String(50))
    floor = db.Column('floor', db.String(50))
    construct_year = db.Column('construct_year',db.String(50))

class Community(db.Model):
    __tablename__ = 'tb_community'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(48))
    contents = db.Column('contents', db.String(4096))
    response_contents = db.Column('response_contents', db.String(4096))
    attatch_file_path = db.Column('attatch_file_path', db.String(2048))
    attatch_file_name = db.Column('attatch_file_name', db.String(2048))
    community_type = db.Column('community_type', db.Integer, default=1)
    user_id = db.Column('user_id', db.String(48))
    user_name = db.Column('user_name', db.String(48))
    created_date = db.Column('created_date', db.DateTime)
    updated_date = db.Column('updated_date', db.DateTime)
    open = db.Column('open', db.Integer, default=0)
    open_range = db.Column('open_range', db.Integer, default=0)
    view_cnt = db.Column('view_cnt', db.Integer, default=0)
    parent_id = db.Column('parent_id', db.Integer, default=-1)

    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "title": self.title
            , "contents": self.contents
            , "response_contents": self.response_contents
            , "attatch_file_path": self.attatch_file_path
            , "attatch_file_name": self.attatch_file_name
            , "community_type": self.community_type
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "created_date": self.created_date
            , "updated_date": self.updated_date
            , "open": self.open
            , "open_range": self.open_range
            , "view_cnt": self.view_cnt
            , "parent_id": self.parent_id
        }
        return resultJSON
