import spacy
import json
import streamlit as st
import os
import csv
import datetime
import random

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to parse and validate data
def parse_greenskills_data(greenskills):
    validated_data = []
    for country_data in greenskills:
        if isinstance(country_data, str):  # Convert string to dictionary if needed
            country_data = json.loads(country_data)
        validated_data.append(country_data)
    return validated_data

# Chatbot logic with SpaCy integration
def chatbot(input_text, greenskills):
    # Process input with SpaCy
    doc = nlp(input_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    year=[(ent.text, ent.label_) for ent in doc.ents]
    # Extract intents or keywords based on entities
    input_text = input_text.lower()
    entity_response = f"Identified Entities: {entities}" if entities else "No entities identified."
    year_response=  f"Identified Entities: {year}" if entities else "No entities identified."
    
    # Check for country name in the input
    for country_data in greenskills:
        if country_data["Entity"].lower() in input_text:
            entity_response = country_data["Entity"]
            break

    # Extract year if mentioned
    for word in input_text.split():
        if word.isdigit() and len(word) == 4:  # Check if it's a 4-digit year
            year_response = int(word)
            break

    # Filter data based on the specific entity and year
    filtered_data = []
    for country_data in greenskills:
        if entity_response and year_response:
            if country_data["Entity"].lower() == entity_response.lower() and country_data["Year"] == year_response:
                filtered_data.append(country_data)
        elif entity_response:
            if country_data["Entity"].lower() == entity_response.lower():
                filtered_data.append(country_data)
        elif year_response:
            if country_data["Year"] == year_response:
                filtered_data.append(country_data)


    # Generate response based on the filtered data
    if filtered_data:
        responses = []
        for country_data in filtered_data:
            if "electricity access" in input_text:
                access_to_electricity = country_data.get("Access to electricity (% of population)", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Access to electricity is {access_to_electricity}%.")

            elif "renewable energy" in input_text:
                renewable_energy_share = country_data.get("Renewable energy share in the total final energy consumption (%)", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Renewable energy share is {renewable_energy_share}%.")

            elif "co2 emissions" in input_text:
                co2_emissions = country_data.get("Value_co2_emissions_kt_by_country", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): CO2 emissions are {co2_emissions} kt.")

            elif "gdp growth" in input_text:
                gdp_growth = country_data.get("gdp_growth", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): GDP growth rate is {gdp_growth}.")

            elif "latitude and longitude" in input_text:
                latitude = country_data.get("Latitude", "Data not available")
                longitude = country_data.get("Longitude", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Latitude is {latitude}, Longitude is {longitude}.")
            elif "clean fuels for cooking" in input_text:
                fuels = country_data.get("Access to clean fuels for cooking","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Access to clean fuels for cooking is{fuels}.")
            elif "Electricity from nuclear" in input_text:
                nuclear_access_to_electricity =country_data.get("Electricity from nuclear(TWh)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Electricity from nuclearis{nuclear_access_to_electricity}TWh.")
          
        # Return all filtered responses
       # return entity_response + "\n" + "\n".join(responses)
        return "\n"+ "\n".join(responses)
    else:
        # If no matching data found
        if entity_response and year_response:
            return f"No data found for {entity_response} in the year {year_response}."
        elif entity_response:
            return f"No data found for {entity_response}."
        elif year_response:
            return f"No data found for the year {year_response}."
        else:
            return random.choice(["I'm sorry, I didn't understand that.", "Can you please rephrase your question?"])


print("hello")
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

    # Load greenskills data once
    try:
        with open('greenskill.json', 'r') as f:
            greenskills = json.load(f)
        greenskills = parse_greenskills_data(greenskills)
    except FileNotFoundError:
        st.error("The file 'greenskills.json' was not found.")
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