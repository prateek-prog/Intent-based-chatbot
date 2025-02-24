import json
import streamlit as st
import os
import csv
import datetime
from p import chatbot
#import random

# Load SpaCy model
#import spacy

#nlp = spacy.load("en_core_web_sm")


# Function to parse and validate data
def parse_greenskills_data(greenskills):
    validated_data = []
    for country_data in greenskills:
        if isinstance(country_data, str):
            # Convert string to dictionary if needed
            country_data = json.loads(country_data)
        validated_data.append(country_data)
    return validated_data


# Function to find the file dynamically
def find_file(file_name, search_dir=os.getcwd()):
    for root, dirs, files in os.walk(search_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None





# Streamlit application
def main():
    st.title("Intent-based Chatbot using NLP and SpaCy")
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Create chat log file if not exists
    log_file = 'chat_log.csv'
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

    # Locate the JSON file dynamically
    json_file_path = find_file("greenskills.json")

    if json_file_path:
        try:
            with open(json_file_path, 'r') as f:
                greenskills = json.load(f)
                greenskills = parse_greenskills_data(greenskills)
        except Exception as e:
            st.error(f"An error occurred while loading 'greenskill.json': {str(e)}")
            return
    else:
        st.error("The file 'greenskill.json' was not found. Please ensure it is in the project directory.")
        return

    if choice == "Home":
        st.write("Welcome to the chatbot. Type a message below to start the conversation.")
        user_input = st.text_input("You:", key="user_input")
        if user_input:
            response = chatbot(user_input, greenskills)
            st.text(f"Chatbot: {response}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append conversation to log
            with open(log_file, 'a', newline='', encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response, timestamp])

    elif choice == "Conversation History":
        st.header("Conversation History")
        try:
            with open(log_file, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    st.text(f"User: {row[0]}")
                    st.text(f"Chatbot: {row[1]}")
                    st.text(f"Timestamp: {row[2]}")
                    st.markdown("---")
        except FileNotFoundError:
            st.write("No conversation history found.")

    elif choice == "About":
        st.header("About the Chatbot")
        st.write("""
            This chatbot uses SpaCy for Natural Language Processing (NLP). 
            It can recognize entities and respond based on predefined intents.
        """)
        st.subheader("Features:")
        st.write("""
            - Query country-specific statistics.
            - Perform Named Entity Recognition (NER) using SpaCy.
            - View previous conversations.
            - Easily extensible for new intents.
        """)


if __name__ == "__main__":
    main()