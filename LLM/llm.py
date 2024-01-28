import openai
import logging
import time
import requests
from fastapi import FastAPI, HTTPException
from keras.models import load_model
from model import MotorData, MotorResponse, PredictionBody, Item
from fastapi import FastAPI, Depends
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import pandas as pd
from pydantic import BaseModel
import datetime
from predict import failure

table_name = "simdata"
loaded_model = load_model('my_model.h5')

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
except Error as e:
    print("Error while connecting to MySQL", e)

app = FastAPI()

client = openai.OpenAI(api_key="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")
thread_id = "thread_OsH5bb0irs26EXgkljbCMU3f"

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_between",
            "description": "Fetch data from a specified column between two dates from the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date for the data retrieval in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "format": "date",
                        "description": "End date for the data retrieval in YYYY-MM-DD format"
                    },
                    "column_name": {
                        "type": "string",
                        "description": "Name of the column to retrieve data from"
                    }
                },
                "required": ["start_date", "end_date", "column_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "predict_failure",
            "description": "Send data to the model for failure prediction",
            "parameters": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "format": "date",
                        "description": "Optional date for the prediction in YYYY-MM-DD format. Defaults to 00:00:00 if time is not specified.",
                        "nullable": True
                    }
                }
            },
            "responses": {
                "type": "object",
                "properties": {
                    "failure": {
                        "type": "number",
                        "description": "Prediction result"
                    },
                    "error": {
                        "type": "string",
                        "description": "Error message if database connection is not established"
                    }
                }
            }
        }
    },
    {"type": "code_interpreter"}
]

file_1 = client.files.create(
    file=open("motor-documentation.pdf", "rb"),
    purpose='assistants'
)

file_2 = client.files.create(
    file=open("Bosch Motor.pdf", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    name="Albert 2.0",
    instructions="""You are Pam an agent specialized in assisting industrial engineers. His primary role is to diagnose issues in industrial systems and predict maintenance needs. He uses his expertise in industrial engineering to provide insightful, accurate, and practical solutions. 
The organization is currently using a Radial Piston Motor of type MRD. by Parker Hannifin. Use the documentations provided whenever possible to get more information. 
Call the required functions whenever required.""",
    tools=tools_list,
    model="gpt-4-1106-preview",
    file_ids=[file_1.id, file_2.id]
)


def process_response(response):
    response = response[0]
    res = {}
    keys = ["volt", "rotate", "pressure", "vibration", "timestamp"]
    for i in range(len(response)):
        val = response[i]
        res[keys[i]] = val

    res['timestamp'] = str(res['timestamp'])

    return MotorResponse(
        volt=res["volt"],
        rotate=res["rotate"],
        pressure=res["pressure"],
        vibration=res["vibration"],
        timestamp=res["timestamp"],
    )


def openai_create_thread():
    thread = client.beta.threads.create(messages=[{"role": "user", "content": "Hi"}])
    thread_id = thread.id
    return thread_id


@app.get("/")
def home():
    return {"message": "The server is up and running"}


# def send_data(data: MotorData, db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     try:
#         cursor = db_connection.cursor()
#
#         # SQL query to insert values into all columns
#         sql_query = f"INSERT INTO {table_name} (volt, rotate, pressure, vibration, timestamp) " \
#                     f"VALUES ({data.volt}, {data.rotate}, {data.pressure}, {data.vibration}, '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
#
#         # Execute the query with the values
#         cursor.execute(sql_query)
#         # Commit the transaction
#         return {"message": "Query Successful"}
#     except:
#         return {"error": "Database connection not established"}
#

# @app.get('/data/get')
# def receive_data(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)) -> MotorResponse:
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()
#
#         query = f"SELECT * FROM {table_name} WHERE timestamp = (SELECT MAX(timestamp) FROM {table_name})"
#
#         cursor.execute(query)
#
#         result = cursor.fetchall()
#
#         db_connection.close()
#         cursor.close()
#
#         return process_response(result)
#
#     else:
#         return {"error": "Database connection not established"}


def construct_between(result, col):
    res = [{"timestamp": str(val[0]), col: val[1]} for val in result]
    return json.dumps(res)


def get_between(start: str = '', end: str = '', col: str = ''):
    try:
        cursor = connection.cursor()

        if start != end:
            query = f"SELECT timestamp,{col} FROM {table_name}\n WHERE timestamp BETWEEN '{start} 00:00:00' AND '{end} 00:00:00'"
        else:
            query = f"SELECT timestamp,{col} FROM {table_name}\n WHERE timestamp BETWEEN '{start} 00:00:00' AND '{end} 23:59:59'"

        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()

        return construct_between(result, col)

    except:
        return {"error": "Database connection not established"}


# def send_data(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     # Week timespan
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()
#
#         query = f"SELECT timestamp, pressure FROM {table_name}"
#
#         cursor.execute(query)
#
#         result = cursor.fetchall()
#
#         dataframe = pd.DataFrame(result)
#         dataframe.columns = ["datetime", "pressure"]
#
#         res = failure(loaded_model, dataframe)
#         return {"failure": res}
#
#     else:
#         return {"error": "Database connection not established"}


# noinspection PyStatementEffect
# @app.post('/data/financial_prediction')
# def predict_financial(body: PredictionBody,
#                       db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()
#
#         query = f"SELECT timestamp, pressure FROM {table_name}"
#
#         cursor.execute(query)
#
#         result = cursor.fetchall()
#
#         dataframe = pd.DataFrame(result)
#         dataframe.columns = ["datetime", "pressure"]
#
#         res = failure(loaded_model, dataframe)
#
#         if res:
#             {"message": f"There is a likelihood that the device will experience failure. If the device fails, you will expect \
#               ${body.amount_of_downtime * body.per_hour_downtime_cost}"}
#
#         else:
#             {
#                 "message": f"There is a low likelihood that the device will fail. The expected cost to repair the device is ${body.motor_repair_cost}"}
#
#     else:
#         return {"error": "Database connection not established"}

def predict_failure(timestamp=None):
    cursor = connection.cursor()
    query = f"SELECT timestamp, pressure FROM {table_name}"

    cursor.execute(query)
    result = cursor.fetchall()

    dataframe = pd.DataFrame(result)
    dataframe.columns = ["datetime", "pressure"]

    if timestamp:
        dataframe = dataframe[dataframe['datetime'] <= timestamp]

    res = failure(loaded_model, dataframe)

    cursor.close()
    return {"failure": res}



def insert_thread_data(name: str, thread_id: str, db_connection):
    try:
        cursor = db_connection.cursor()
        query = "INSERT INTO threads (thread_name, thread_id) VALUES (%s, %s)"
        cursor.execute(query, (name, thread_id))
        db_connection.commit()
        cursor.close()
    except Error as e:
        print("Error while inserting into MySQL", e)


# @app.post("/thread/createThread")  # Changed from @app.get
# def create_thread(thread: Item, db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     if not db_connection.is_connected():
#         return {"error": "Failed to connect to the database"}
#
#     name = thread.threadName
#     thread_id = openai_create_thread()
#
#     insert_thread_data(name, thread_id, db_connection)
#     db_connection.close()
#
#     return {"message": "Thread created", "thread_name": name, "thread_id": thread_id}


# @app.post('/table/drop')
# def drop_table(db_connection: mysql.connector.MySQLConnection = Depends(get_db_connection)):
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()
#
#         # noinspection SqlNoDataSourceInspection
#         query = ''' CREATE TABLE simdata(
#         volt FLOAT,
#         rotate FLOAT,
#         pressure FLOAT,
#         vibration FLOAT,
#         timestamp DATETIME,
#         PRIMARY KEY(timestamp)
#         )
#         '''
#
#         cursor.execute(query)
#
#         db_connection.close()
#         cursor.close()
#
#         return {"message": "successful"}
#

def get_data_between_dates(start, end, col):
    """
    Sends a GET request to the server to retrieve data between specified start and end dates for a given column.

    :param start: The start date in 'YYYY-MM-DD' format.
    :param end: The end date in 'YYYY-MM-DD' format.
    :param col: The name of the column to retrieve data from.
    :return: The server's response as a JSON object if successful, else an error message.
    """
    # Endpoint URL
    url = 'http:/127.0.0.1:9567/data/get_between'

    # Parameters for the GET request
    url = f'{url}/?start={start}&end={end}&col={col}'  # Replace with your actual server URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming the server returns JSON data
    else:
        return f"Error: {response.status_code}, {response.text}"



def create_thread():
    thread = client.beta.threads.create(messages=[{"role": "user", "content": "Hi"}])
    thread_id = thread.id
    return thread_id


def create_message(thread_id, message):
    message_execute = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    return message_execute


def execute_message(thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id,
    )
    return run.id


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                return response

            elif run.status == 'requires_action':
                print("Calling Function")
                required_actions = run.required_action.submit_tool_outputs.model_dump()
                print(required_actions)
                tool_outputs = []
                import json
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])

                    if func_name == "get_between":
                        output = get_between(start=arguments['start_date'], end=arguments["end_date"],
                                             col=arguments["column_name"])
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    elif func_name == "predict_failure":
                        timestamp = arguments.get('timestamp', None)
                        output = predict_failure(timestamp=timestamp)
                        output =  json.dumps(output)
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    else:
                        raise ValueError(f"Unknown function: {func_name}")

                print("Submitting outputs back to the Assistant...")
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


@app.post("/sendMessage/{message}")
def predict(message):
    try:
        create_message(thread_id=thread_id, message=message)
        run_id = execute_message(thread_id)
        response_string = wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id)
        return {"message": response_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.route("/")
def home():
    return "Hello World"


# predict_failure()
#
# print(predict("Hi! Could you get me the pressure values from 27th Januray 2024 to 28th 2024 Januray"))
# print(create_thread())