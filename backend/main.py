from model import MotorData, MotorResponse, PredictionBody, Item
from fastapi import FastAPI, Depends
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import pandas as pd
from tensorflow.keras.models import load_model
from predict import failure
from openai import openai_create_thread
import csv

app = FastAPI()
table_name = "simdata"
csv_file_path = './pressure.csv'

loaded_model = load_model('my_model.h5')

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='db-mysql-nyc3-58187-do-user-8755953-0.c.db.ondigitalocean.com',
            database='defaultdb',
            user='doadmin',
            password='AVNS_-Dci05t-7EH-AUALdb9',
            port=25060,
            ssl_ca='./ca-certificate.crt',
            ssl_verify_cert=True
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
    
def process_response(response):
    response = response[0]
    res = {}
    keys = ["volt", "rotate", "pressure", "vibration", "timestamp"]
    for i in range (len(response)):
        val = response[i]
        res[keys[i]] = val

    res['timestamp'] = str(res['timestamp'])

    return MotorResponse (
        volt=res["volt"],
        rotate=res["rotate"],
        pressure=res["pressure"],
        vibration=res["vibration"],
        timestamp=res["timestamp"],
    )


@app.get("/")
def home():
    return {"message": "The server is up and running"}


@app.post('/data/send')
def send_data(data: MotorData, db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    
    if db_connection.is_connected():
        cursor = db_connection.cursor()

        # SQL query to insert values into all columns
        sql_query = f"INSERT INTO {table_name} (volt, rotate, pressure, vibration, timestamp) " \
                    f"VALUES ({data.volt}, {data.rotate}, {data.pressure}, {data.vibration}, '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"

        # Execute the query with the values
        cursor.execute(sql_query)
        # Commit the transaction
        db_connection.commit()

        cursor.close()

        db_connection.close()

        return {"message" : "Query Successful"}

    else:
        return {"error" : "Database connection not established"}

@app.get('/data/get') 
def receive_data(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)) -> MotorResponse:

    if db_connection.is_connected():
        cursor = db_connection.cursor()

        query = f"SELECT * FROM {table_name} WHERE timestamp = (SELECT MAX(timestamp) FROM {table_name})"

        cursor.execute(query)

        result = cursor.fetchall()

        db_connection.close()
        cursor.close()

        return process_response(result)

    else:
        return {"error" : "Database connection not established"}


def construct_between(result, col):
    res = [{"timestamp": str(val[0]),col : val[1]} for val in result]
    return json.dumps(res)



@app.get('/data/get_between')
def get_between(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection), start: str = '', end : str = '', col : str = ''):

    if db_connection.is_connected():
        cursor = db_connection.cursor()

        if start != end:
            query = f"SELECT timestamp,{col} FROM {table_name}\n WHERE timestamp BETWEEN '{start} 00:00:00' AND '{end} 00:00:00'"
        else:
            query = f"SELECT timestamp,{col} FROM {table_name}\n WHERE timestamp BETWEEN '{start} 00:00:00' AND '{end} 23:59:59'"

        cursor.execute(query)

        result = cursor.fetchall()

        db_connection.close()
        cursor.close()

        return construct_between(result,col)
    
    else:
        return {"error" : "Database connection not established"}
    


# @app.post('/data/predict')
def send_data(timestamp: datetime | None = None, db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    
    # Week timespan
    if db_connection.is_connected():
        cursor = db_connection.cursor()

        query = f"SELECT timestamp, pressure FROM {table_name}"

        cursor.execute(query)

        result = cursor.fetchall()

        dataframe = pd.DataFrame(result)
        dataframe.columns = ["datetime", "pressure"]

        if timestamp:
            dataframe = dataframe[dataframe['datetime']<=timestamp]
        
        res = failure(loaded_model, dataframe)

        db_connection.close()
        cursor.close()

        return {"failure" : res}

    else:
        return {"error" : "Database connection not established"}


def predict_financial(body: PredictionBody):
    
    if db_connection.is_connected():
        cursor = db_connection.cursor()

        query = f"SELECT timestamp, pressure FROM {table_name}"

        cursor.execute(query)

        result = cursor.fetchall()

        dataframe = pd.DataFrame(result)
        dataframe.columns = ["datetime", "pressure"]
        
        res = failure(loaded_model, dataframe)

        db_connection.close()
        cursor.close()
        
        if res:
            return f"There is a likelihood that the device will experience failure. If the device fails, you will expect \
              a downtime cost of about ${body.downtime * body.downtime_per_hour_cost} and it is expected to cost ${body.repair_cost}"

        else:
            return f"There is a low likelihood that the device will fail. The expected cost to repair the device is ${body.repair_cost}"

    else:
        return {"error" : "Database connection not established"}


def add_financials(body: PredictionBody):

    if db_connection.is_connected():
        cursor = db_connection.cursor()

        query = f"INSERT INTO finances (repair_cost, downtime, downtime_per_hour_cost) VALUES ({body.repair_cost}, {body.downtime}, {body.downtime_per_hour_cost})"

        cursor.execute(query)
        db_connection.close()
        cursor.close()

    else:
        return {"error" : "Database connection not established"}
    
def machine_financials(machine_id: str):
    if db_connection.is_connected():
        cursor = db_connection.cursor()

        query = f"SELECT timestamp, pressure FROM {table_name}"

        cursor.execute(query)

        result = cursor.fetchall()

        dataframe = pd.DataFrame(result)
        dataframe.columns = ["datetime", "pressure"]

        financial_query = f"SELECT repair_cost, downtime, downtime_per_hour_cost from finances WHERE machine_id = {machine_id};"

        cursor.execute(financial_query)

        financial_query_result = cursor.fetchall()
        
        res = failure(loaded_model, dataframe)

        financial_query_result = financial_query_result[0]

        db_connection.close()
        cursor.close()
        
        if res:
            return f"There is a likelihood that the device will experience failure. If the device fails, you will expect \
              a downtime cost of about ${financial_query_result[1] * financial_query_result[2]} and it is expected to cost ${financial_query_result[0]}"

        else:
            return f"There is a low likelihood that the device will fail. The expected cost to repair the device is ${financial_query_result[0]}"

    else:
        return {"error" : "Database connection not established"}




def insert_thread_data(name: str, thread_id: str, db_connection):
    try:
        cursor = db_connection.cursor()
        query = "INSERT INTO threads (thread_name, thread_id) VALUES (%s, %s)"
        cursor.execute(query, (name, thread_id))
        db_connection.commit()
        cursor.close()
    except Error as e:
        print("Error while inserting into MySQL", e)

@app.post("/thread/createThread")  # Changed from @app.get
def create_thread(thread: Item, db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    if not db_connection.is_connected():
        return {"error": "Failed to connect to the database"}

    name = thread.threadName
    thread_id = openai_create_thread()

    insert_thread_data(name, thread_id, db_connection)
    db_connection.close()

    return {"message": "Thread created", "thread_name": name, "thread_id": thread_id}


@app.get('/add_machine_data')
def add_machine_data(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):

    if db_connection.is_connected():
        cursor = db_connection.cursor()

        remove = f"DELETE FROM {table_name}"

        cursor.execute(remove)
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                print(row)
                timestamp = row["datetime"]
                pressure = row["pressure"]
                rotate = row["rotate"]
                vibration = row["vibration"]
                volt = row["volt"]

                # Insert data into the 'threads' table
                query = f"INSERT INTO {table_name} (volt, rotate, pressure, vibration, timestamp) VALUES ({volt}, {rotate}, {pressure}, {vibration}, '{timestamp}')"
                cursor.execute(query)

        # Commit the changes and close the cursor
        db_connection.commit()
        cursor.close()
        db_connection.close()




# @app.post('/table/drop')
# def drop_table(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()

#         query = ''' CREATE TABLE simdata(
#         volt FLOAT,
#         rotate FLOAT,
#         pressure FLOAT,
#         vibration FLOAT,
#         timestamp DATETIME,
#         PRIMARY KEY(timestamp)
#         )
#         '''

#         cursor.execute(query)

#         db_connection.close()
#         cursor.close()

#         return {"message" : "successful"}
        