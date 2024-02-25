from backend_model.database import DBManager
db = DBManager.db

class CustomerTbl(db.Model):
    __tablename__ = 'customer_tbl'

    customer_idx = db.Column('customer_idx', db.Integer, primary_key=True)
    customer_name = db.Column('customer_name', db.String(45))
    customer_tel = db.Column('customer_tel', db.String(12))
    customer_address = db.Column('customer_address', db.String(45))

class EventLogTbl(db.Model):
    __tablename__ = 'event_log_tbl'

    event_log_idx = db.Column('event_log_idx', db.Integer, primary_key=True)
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    event_id = db.Column('event_id', db.Integer)
    receiver_type = db.Column('receiver_type', db.Integer)
    receiver_id = db.Column('receiver_id', db.Integer)
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer)
    sensor_id = db.Column('sensor_id', db.Integer)
    sensor_value = db.Column('sensor_value', db.Integer)
    inout_id = db.Column('inout_id', db.Integer, default='00')
    event_datetime = db.Column('event_datetime', db.DateTime)
    customer = db.relationship('CustomerTbl')

class EventTbl(db.Model):
    __tablename__ = 'event_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    event_idx = db.Column('event_idx', db.String(12))
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_type = db.Column('receiver_type', db.Integer)
    event_type = db.Column('event_type', db.Integer)
    event_id = db.Column('event_id', db.Integer)
    sensor_id = db.Column('sensor_id', db.Integer, default='00')
    event_desc = db.Column('event_desc', db.String(100))
    customer = db.relationship('CustomerTbl')

class FireReceiverTbl(db.Model):
    __tablename__ = 'fire_receiver_tbl'
    
    id = db.Column('id', db.Integer, primary_key=True)
    receiver_idx = db.Column('receiver_idx', db.String(11), primary_key=True)
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_type = db.Column('receiver_type', db.Integer)
    receiver_id = db.Column('receiver_id', db.Integer)
    customer = db.relationship('CustomerTbl')

class FireRepeaterTbl(db.Model):
    __tablename__ = 'fire_repeater_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    repeater_idx = db.Column('repeater_idx', db.String(11), primary_key=True)
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_id = db.Column('receiver_id', db.Integer)
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer)
    customer = db.relationship('CustomerTbl')

class FireSensorTbl(db.Model):
    __tablename__ = 'fire_sensor_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    sensor_idx = db.Column('sensor_idx', db.String(17), primary_key=True)
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_id = db.Column('receiver_id', db.Integer)
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer)
    sensor_id = db.Column('sensor_id', db.Integer)
    customer = db.relationship('CustomerTbl')

class UserTbl(db.Model):
    __tablename__ = 'user_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(10), primary_key=True)
    user_pwd = db.Column('user_pwd', db.String(10))
    user_name = db.Column('user_name', db.String(45))
    user_status = db.Column('user_status', db.Integer, default='1')
    user_role = db.Column('user_role', db.Integer, default='1')