import sqlite3,base64,uuid,queue,threading,requests,time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class dbhubIO:
    
    executor = ThreadPoolExecutor(max_workers=1)
    
    def __init__(self):
        self.apikey = "2TSzSrLb6sU4rOHOlBJiwznwDKa"
        self.dbname = "data.db"
        self.dbowner = "quantbeans"
        self.dbendpoint = "https://api.dbhub.io/v1/execute"
        self.uuid = str(uuid.uuid1())
        self.request_queue = queue.Queue()
        
        # Start the process_queue method in a separate thread
        self.process_queue_thread = threading.Thread(target=self.process_queue)
        self.process_queue_thread.daemon = True  # Set the thread as a daemon so it stops when the main thread ends
        self.process_queue_thread.start()
    
    def __del__(self):
        return
    
    def close_connection(self):
        return

    def insert_data(self, table_name, df):
        try:
            df['uuid'] = self.uuid
            sql_statement = self.generate_sql_insert(table_name, df)
            sql_b64 = self.encode_to_base64(sql_statement)
            payload = {
                "apikey": self.apikey,
                "dbowner": self.dbowner,
                "dbname": self.dbname,
                "sql": sql_b64
                }
            self.request_queue.put(payload)

        except Exception as e:
            pass
    
    def process_queue(self):
        while True:  # Run the process_queue method continuously
            payload = self.request_queue.get()
            self.send_request(payload)
            time.sleep(0.1)  # Sleep for 0.1 seconds before checking the queue again
            
    def send_request(self, payload):
        response = requests.post(self.dbendpoint, data=payload)
        # if response.status_code == 200:
        #     print(response.json())
        # else:
        #     print("Error:", response.status_code)
        #     print(response.text)
    
    def encode_to_base64(self, input_string):
        # Convert the input string to bytes (required for base64 encoding)
        input_bytes = input_string.encode('utf-8')

        # Encode the bytes to base64
        encoded_bytes = base64.b64encode(input_bytes)

        return encoded_bytes
    
    def generate_sql_insert(self,table_name, df):

        columns = ', '.join(['"' + col + '"' for col in df.columns])
        values = ', '.join(['(' + ', '.join([f"'{str(val)}'" if pd.notna(val) else "NULL" for val in row]) + ')' for row in df.values])

        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES {values};"
        return sql_insert

class sqliteDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.uuid = str(uuid.uuid1())
    
    def __del__(self):
        self.close_connection()
        
    def close_connection(self):
        self.conn.close()

    def insert_data(self, table_name, df, if_exists='append', index=False):
        try:
            df['uuid'] = self.uuid
            df.to_sql(table_name, self.conn, if_exists=if_exists, index=index)
        except Exception as e:
            pass