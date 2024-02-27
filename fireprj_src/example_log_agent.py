import MySQLdb
from datetime import datetime, timedelta
import time
import numpy as np

class ExampleLogAgent(object):
    def __init__(self):
        self.event_log_filed = 'fk_customer_idx, event_id, receiver_type, '\
                                + 'receiver_id, system_id, repeater_id, sensor_id, '\
                                + 'sensor_value, inout_id, event_datetime'
    
    def connect_to_db(self):
        try:
            self.db = MySQLdb.connect(
                host="localhost",
                user="dbadmin",
                passwd="p#ssw0rd",
                db='fireprjdb',
                charset='utf8',
                use_unicode=True
            )
            self.db.autocommit(True)
            return True
        except:
            return False
    
    def get_cursor(self):
        if self.db is None:
            return None
        return self.db.cursor(MySQLdb.cursors.DictCursor)
    
    def disconnect(self):
        if self.db:
            self.db.close()
    
    def create_example_dataset(self, sensor_len):
        """데이터 생성: return [센서1의 샘플, 센서2의 샘플...]"""
        def create_example_data(example_type):
            result = []
            judge = 5 if example_type == 0 else 3
            for n in range(60 * 24):
                offset = 0
                x = np.linspace(0, 20*np.pi, 1000)
                if n % judge == 0:
                    offset = 1
                y = np.sin(x) + offset
                result += list(y)
            return result
        
        data_list = [None] * sensor_len
        for i in range(sensor_len):
            if i % 2 == 0: data_list[i] = create_example_data(0) #정상 데이터
            else: data_list[i] = create_example_data(1) #홀수번째 센서는 이상 데이터
        return data_list
    
    def add_example_log(self, cursor, example_data: list):
        values_string = [str(x) if type(x) != str else x for x in example_data]
        sql_string = '''
        INSERT INTO event_log_tbl({0}) values({1})
        '''.format(self.event_log_filed, ', '.join(values_string))
        try:
            cursor.execute(sql_string)
        except MySQLdb.DataError as e:
            print(e)
            print(values_string)
    
    def example_logging(self, cursor):
        sensor_list_sql = '''
        SELECT * FROM fire_sensor_tbl
        '''
        cursor.execute(sensor_list_sql)
        sensor_list = [row for row in cursor.fetchall()]
        
        is_error_cnt = 0
        while is_error_cnt < 1: #샘플 데이터가 없으면 새로 만드는 반복문
            data_list = self.create_example_dataset(len(sensor_list))
            is_error_cnt += 1
            while True:
                print('running...')
                try:
                    for _ in range(1000):
                        for i, sensor in enumerate(sensor_list):
                            data = [1, 1, 1, sensor["receiver_id"], sensor["system_id"], sensor["repeater_id"]\
                                    , sensor["sensor_id"], round(data_list[i].pop(0), 4), 0, f'"{datetime.now()}"']
                            self.add_example_log(cursor, data)
                except IndexError as e: #모든 데이터를 pop했다면 상위 while문으로 돌아가 데이터를 만듦
                    print(e)
                    is_error_cnt -= 1
                    break
                time.sleep(10)

    def run(self):
        print("eventLogAgent run...")
        if not self.connect_to_db():
            print("DB CONNECT FAILED")
            return
        cursor = self.get_cursor()
        self.example_logging(cursor)
        self.disconnect()

if __name__ == "__main__":
    print("start...")
    example_agent = ExampleLogAgent()
    example_agent.run()