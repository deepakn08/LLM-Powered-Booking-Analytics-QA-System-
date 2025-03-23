from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import nest_asyncio

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load CSV file
df = pd.read_csv("processed_hotel_data.csv")

# Create SQLite connection (for MySQL/PostgreSQL, update connection string)
engine = create_engine("sqlite:///hotel_bookings.db")

# Store CSV data in SQL table
df.to_sql("hotel_bookings", con=engine, if_exists="replace", index=False)

# Give you api key
api_key = groq_api_key
llm = ChatGroq(model = 'llama3-70b-8192', api_key = api_key)

llm_sql = llm
llm_process = llm

# Function for generating the sql query
def generate_sql_query(user_query):
    messages = [
        SystemMessage(content="""You are an AI that creates an SQLLite query based on the user's query.
                                Name of the table is hotel_bookings \n
                                You must use only the following column names:
                                ['hotel', 'is_canceled', 'lead_time', 'arrival_date_week_number',
                                'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children',
                                'babies', 'meal', 'country', 'market_segment', 'distribution_channel',
                                'is_repeated_guest', 'previous_cancellations',
                                'previous_bookings_not_canceled', 'reserved_room_type',
                                'assigned_room_type', 'booking_changes', 'deposit_type', 'agent',
                                'company', 'days_in_waiting_list', 'customer_type', 'adr',
                                'required_car_parking_spaces', 'total_of_special_requests',
                                'reservation_status', 'arrival_date', 'checkout_date', 'night_stay',
                                'Total_revenue']\n
                                Just give the SQL query only nothing other.\n
                                From the final SQL query remove \n
                                For the revenue or price related thing alsways use booking that are not cancelled.
                             """),
        HumanMessage(content=user_query)  # Pass user query dynamically
    ]

    response = llm_sql(messages)
    return response.content

# Function for executing the query
def execute_sql_query(sql_query):
    conn = sqlite3.connect("hotel_bookings.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    conn.close()
    return data

# Function for converting the output into good presentable answer
def process_data_with_llm(data, user_query):
    messages = [
        SystemMessage(content="""You are an AI you will get the data which is the answer of the user query your task is create a good complete answer \n
                                by using the data and user query.\n
                                Don't give the extra answers just give the answer related to query.
                      """),
        HumanMessage(content=f"Here is the raw data: {data}. Based on the user query '{user_query}', provide a meaningful response.")
    ]
    response = llm_process(messages)
    return response.content

# Final Function for calling output
def query_hotel_data(user_query):
    sql_query = generate_sql_query(user_query)
    data = execute_sql_query(sql_query)
    final_output = process_data_with_llm(data, user_query)
    return final_output


# Building fastapi
nest_asyncio.apply()

app = FastAPI()

@app.post('/ask/', response_class=HTMLResponse)
def ask_question(ques: str):
    response = query_hotel_data(ques)
    return response

uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
