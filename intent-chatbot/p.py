import spacy
import random
nlp = spacy.load("en_core_web_sm")
def chatbot  (input_text, greenskills):

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
    if entity_response and year_response:
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
    else:
        filtered_data = greenskills

    # Generate response based on the filtered data
    if filtered_data:
        responses = []
        for country_data in filtered_data:
            if "electricity access population" in input_text:
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
            elif "nuclear electicity" in input_text:
                nuclear_electricity =country_data.get("Electricity from nuclear(TWh)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Electricity from nuclear (TWh) is{nuclear_electricity}TWh.")
            elif "fossil fuels" in input_text:
                 fossil_fuel_electricity = country_data.get("Electricity from fossil fuels (TWh)","Data not avaliable")
                 responses.append(f"{country_data['Entity']} ({country_data['Year']}): Electricity from fossil fuels (TWh) is{fossil_fuel_electricity}TWh.")
            elif "financial flow for developing countries" in input_text:
                financial_developement = country_data.get("Financial flows to developing countries (US $)","Data not avaliable")  
                responses.append(f"{country_data['Entity']} ({country_data['Year']}):Financial flows to developing countries (US $) is{financial_developement}TWh.")
            elif "Low carbon electricity" in input_text:
                low_carbon_electricity = country_data.get("Low-carbon electricity (% electricity)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}):Low-carbon electricity is{low_carbon_electricity}%.") 
            elif "Land Area" in input_text:
               #land_area = country_data.get("Land Area(KM2)","Data not avaliable")
               #responses.append(f"{country_data['Entity']}):Land Area is{land_area}KM2.")       
                land_area = country_data.get("Land Area(KM2)")
                if land_area:
                  responses.append(f"{country_data.get['Entity']}: Land Area is {land_area} KM².")
                else:
                  responses.append(f"No data found for {country_data.get('Entity', 'this country')}.")
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


