import streamlit as st
import sqlite3
import plotly.graph_objects as go

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()

# Create the mental_health table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mental_health (
        id INTEGER PRIMARY KEY,
        date DATE,
        feelings TEXT,
        serenity INTEGER,
        sleep INTEGER,
        productivity INTEGER,
        enjoyment INTEGER
    )
''')

# Function to insert data into the database
def insert_mental_health_data(date, feelings, serenity, sleep, productivity, enjoyment):
    cursor.execute('''
        INSERT INTO mental_health (date, feelings, serenity, sleep, productivity, enjoyment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, feelings, serenity, sleep, productivity, enjoyment))
    conn.commit()

# Streamlit UI
st.title("Mental Health Tracker and Score Meter")

# Input fields for mental health details
date = st.date_input("Date", value=None, key='date_input')
feelings = st.slider("Feelings(1-10)", 1, 10, 5)
serenity = st.slider("Serenity (1-10)", 1, 10, 5)
sleep = st.slider("Sleep quality (1-10)", 1, 10, 5)
productivity = st.slider("Productivity (1-10)", 1, 10, 5)
enjoyment = st.slider("Enjoyment (1-10)", 1, 10, 5)

# Button to submit the data
if st.button("Submit"):
    if feelings:
        insert_mental_health_data(date, feelings, serenity, sleep, productivity, enjoyment)
        st.success("Data submitted successfully!")

# Function to calculate the mental health score
def calculate_mental_health_score():
    cursor.execute("SELECT serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    mental_health_score = sum(data[-1]) / 4  # Simple average score

    return mental_health_score

# Calculate the mental health score
mental_health_score = calculate_mental_health_score()

if mental_health_score is not None:
    st.write("Current Mental Health Score:", mental_health_score)

    # Create a gauge chart using Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mental_health_score,
        title="Mental Health Score",
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 10]},
               'bar': {'color': "lightblue"},
               'steps': [
                   {'range': [0, 3], 'color': "red"},
                   {'range': [3, 7], 'color': "yellow"},
                   {'range': [7, 10], 'color': "green"}]
               }
    ))

    st.plotly_chart(fig)
else:
    st.warning("No data available. Please enter data first.")

# Close the database connection when the app is done
conn.close()

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()

# Streamlit UI
st.title("Mental Health Data Visualization")

# Function to retrieve data from the database
def retrieve_mental_health_data():
    cursor.execute("SELECT date, serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    df = pd.DataFrame(data, columns=['Date', 'Serenity', 'Sleep', 'Productivity', 'Enjoyment'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Function to delete all data from the database
def delete_all_data():
    cursor.execute("DELETE FROM mental_health")
    conn.commit()
    st.success("All data deleted successfully!")

# Retrieve and display the mental health data
mental_health_data = retrieve_mental_health_data()

if mental_health_data is not None:
    st.write("Mental Health Data:")
    st.dataframe(mental_health_data)

    # Create a line chart for all attributes
    fig1 = px.line(mental_health_data, x='Date', y=['Serenity', 'Sleep', 'Productivity', 'Enjoyment'],
                   title="Mental Health Attributes Over Time")
    st.write("Line Plot for Mental Health Attributes:")
    st.plotly_chart(fig1)

    # Function to calculate the mental health score
    def calculate_mental_health_score(data):
        data['Mental Health Score'] = data[['Serenity', 'Sleep', 'Productivity', 'Enjoyment']].mean(axis=1)
        return data

    mental_health_data = calculate_mental_health_score(mental_health_data)

    # Create a line chart for the mental health score
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=mental_health_data['Date'], y=mental_health_data['Mental Health Score'],
                             mode='lines+markers', name='Mental Health Score', line=dict(color='blue')))
    fig2.update_layout(title="Mental Health Score Over Time", xaxis_title="Date", yaxis_title="Mental Health Score")
    st.write("Line Plot for Mental Health Score:")
    st.plotly_chart(fig2)

else:
    st.warning("No data available. Please enter data first.")

# Button to delete all data
if st.button("Delete All Data"):
    delete_all_data()

# Close the database connection when the app is done
conn.close()

import streamlit as st
import sqlite3
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub, PromptTemplate, LLMChain

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()


import os
huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

# Streamlit UI
st.title("Mental Health Guidelines")

# Function to retrieve insights from the database
def retrieve_mental_health_data():
    cursor.execute("SELECT feelings, serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    feelings_list = [row[0] for row in data]
    serenity_list = [row[1] for row in data]
    sleep_list = [row[2] for row in data]
    productivity_list = [row[3] for row in data]
    enjoyment_list = [row[4] for row in data]

    return feelings_list, serenity_list, sleep_list, productivity_list, enjoyment_list

# Retrieve data from the database
feelings, serenity, sleep, productivity, enjoyment = retrieve_mental_health_data()

# User input
user_input = st.text_input("Ask a question or seek guidance")


# Provide suggestions and guidance
if user_input:
    context = f"Feelings: {', '.join(feelings)}\nSerenity: {serenity}\nSleep: {sleep}\nProductivity: {productivity}\nEnjoyment: {enjoyment}\n\nUser Question: {user_input}"
    repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token, 
                     repo_id=repo_id, 
                     model_kwargs={"temperature":0.6, "max_new_tokens":2000})
    template = """
You are an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.

{question}

"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    suggestion = llm_chain.run(user_input)

    st.write("Suggestion:")
    st.write(suggestion)

# Close the database connection when the app is done
conn.close()