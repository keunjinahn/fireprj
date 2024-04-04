from backend_model.database import DBManager
db = DBManager.db

class CustomerTbl(db.Model):
    __tablename__ = 'customer_tbl'

    customer_idx = db.Column('customer_idx', db.Integer, primary_key=True)
    customer_name = db.Column('customer_name', db.String(45))
    customer_tel = db.Column('customer_tel', db.String(12))
    customer_address = db.Column('customer_address', db.String(45))


class EventTbl(db.Model):
    __tablename__ = 'event_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    event_idx = db.Column('event_idx', db.String(12))
    system_id_c = db.Column('system_id_c', db.String)
    repeater_id_c = db.Column('repeater_id_c', db.String)
    sensor_id_c = db.Column('sensor_id_c', db.String)
    sensor_value_c = db.Column('sensor_value_c', db.String)
    inout_id_c = db.Column('inout_id_c', db.String)
    event_desc = db.Column('event_desc', db.String)
    event_category = db.Column('event_category', db.String)



class FireReceiverTbl(db.Model):
    __tablename__ = 'fire_receiver_tbl'
    
    id = db.Column('id', db.Integer, primary_key=True)
    receiver_idx = db.Column('receiver_idx', db.String(11))
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_type = db.Column('receiver_type', db.Integer)
    receiver_id = db.Column('receiver_id', db.Integer)
    customer = db.relationship('CustomerTbl')
    
class EventLogTbl(db.Model):
    __tablename__ = 'event_log_tbl'

    event_log_idx = db.Column('event_log_idx', db.Integer, primary_key=True)
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    event_id = db.Column('event_id', db.Integer,db.ForeignKey(EventTbl.id))
    event_idx = db.Column('event_idx', db.Integer)
    receiver_type = db.Column('receiver_type', db.Integer)
    receiver_id = db.Column('receiver_id', db.Integer,db.ForeignKey(FireReceiverTbl.receiver_id))
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer)
    sensor_id = db.Column('sensor_id', db.Integer)
    sensor_value = db.Column('sensor_value', db.String)
    inout_id = db.Column('inout_id', db.Integer, default='00')
    event_datetime = db.Column('event_datetime', db.DateTime)
    customer = db.relationship('CustomerTbl')
    event = db.relationship('EventTbl')
    receiver = db.relationship('FireReceiverTbl')


class FireRepeaterTbl(db.Model):
    __tablename__ = 'fire_repeater_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    repeater_idx = db.Column('repeater_idx', db.String(11))
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_id = db.Column('receiver_id', db.Integer,db.ForeignKey(FireReceiverTbl.receiver_id))
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer)
    customer = db.relationship('CustomerTbl')
    register_status = db.Column('register_status', db.Integer)
    action_status = db.Column('action_status', db.Integer)
    com_status = db.Column('com_status', db.Integer)
    battery_status = db.Column('battery_status', db.Integer)    
    last_event_time = db.Column('last_event_time', db.DateTime)
    receiver = db.relationship('FireReceiverTbl')

class FireSensorTbl(db.Model):
    __tablename__ = 'fire_sensor_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    sensor_idx = db.Column('sensor_idx', db.String(17))
    fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
    receiver_id = db.Column('receiver_id', db.Integer,db.ForeignKey(FireReceiverTbl.receiver_id))
    system_id = db.Column('system_id', db.Integer, default='00')
    repeater_id = db.Column('repeater_id', db.Integer,db.ForeignKey(FireRepeaterTbl.repeater_id))
    sensor_id = db.Column('sensor_id', db.Integer)
    customer = db.relationship('CustomerTbl')
    register_status = db.Column('register_status', db.Integer)
    action_status = db.Column('action_status', db.Integer)
    com_status = db.Column('com_status', db.Integer)
    battery_status = db.Column('battery_status', db.Integer)
    last_event_time = db.Column('last_event_time', db.DateTime)
    repeater = db.relationship('FireRepeaterTbl')
    receiver = db.relationship('FireReceiverTbl')

class UserTbl(db.Model):
    __tablename__ = 'user_tbl'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(10))
    user_pwd = db.Column('user_pwd', db.String(10))
    user_name = db.Column('user_name', db.String(45))
    user_status = db.Column('user_status', db.Integer, default='1')
    user_role = db.Column('user_role', db.Integer, default='1')
    token = db.Column('token', db.String(128))  # added
    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "user_status": self.user_status
            , "user_role": self.user_role
            , "token": self.token
        }
        return resultJSON    

# class EventLogTempTbl(db.Model):
#     __tablename__ = 'event_log_temp_tbl'

#     event_log_idx = db.Column('event_log_idx', db.Integer, primary_key=True)
#     fk_customer_idx = db.Column('fk_customer_idx', db.Integer, db.ForeignKey(CustomerTbl.customer_idx))
#     event_id = db.Column('event_id', db.Integer)
#     receiver_type = db.Column('receiver_type', db.Integer)
#     receiver_id = db.Column('receiver_id', db.Integer)
#     system_id = db.Column('system_id', db.Integer, default='00')
#     repeater_id = db.Column('repeater_id', db.Integer)
#     sensor_id = db.Column('sensor_id', db.Integer)
#     sensor_value = db.Column('sensor_value', db.String)
#     inout_id = db.Column('inout_id', db.Integer, default='00')
#     event_datetime = db.Column('event_datetime', db.DateTime)
#     customer = db.relationship('CustomerTbl')