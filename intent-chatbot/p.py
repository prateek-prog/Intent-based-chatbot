import spacy
import random
nlp = spacy.load("en_core_web_sm")
def chatbot  (input_text, greenskills):

# Process input with SpaCy
    doc = nlp(input_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    year=[(ent.text, ent.label_) for ent in doc.ents]
    # Extract intents or keywords based on entities
    input_text = input_text.casefold()
    entity_response = f"Identified Entities: {entities}" if entities else "No entities identified."
    year_response=  f"Identified Entities: {year}" if entities else "No entities identified."
    
    # Check for country name in the input
    for country_data in greenskills:
        if country_data["Entity"].casefold() in input_text:
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
            if country_data["Entity"].casefold() == entity_response.casefold() and country_data["Year"] == year_response:
                filtered_data.append(country_data)
        elif entity_response:
            if country_data["Entity"].casefold() == entity_response.casefold():
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

            elif "Renewable energy share in total final energy consumption" in input_text:
                renewable_energy_share = country_data.get("Renewable energy share in the total final energy consumption (%)", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Renewable energy share is {renewable_energy_share}%.")

            elif "co2 emissions" in input_text:
                co2_emissions = country_data.get("Value_co2_emissions_kt_by_country", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): CO2 emissions are {co2_emissions} kt.")
                #responses.append(f"{country_data['Entity']} ({country_data['Year']}): CO2 emissions are {country_data.get('Value_co2_emissions_kt_by_country', 'Data not available')} kt.")
            elif "gdp growth" in input_text:
                gdp_growth = country_data.get("gdp_growth", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): GDP growth rate is {gdp_growth}.")

            elif "latitude and longitude" in input_text:
                latitude = country_data.get("Latitude", "Data not available")
                longitude = country_data.get("Longitude", "Data not available")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Latitude is {latitude}, Longitude is {longitude}.")

            elif "clean fuels for cooking" in input_text:
                fuels = country_data.get("Access to clean fuels for cooking","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Access to clean fuels for cooking is {fuels}.")

            elif "nuclear electicity" in input_text:
                nuclear_electricity =country_data.get("Electricity from nuclear(TWh)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Electricity from nuclear (TWh) is {nuclear_electricity}TWh.")
                
            elif "fossil fuels" in input_text:
                 fossil_fuel_electricity = country_data.get("Electricity from fossil fuels (TWh)","Data not avaliable")
                 responses.append(f"{country_data['Entity']} ({country_data['Year']}): Electricity from fossil fuels (TWh) is {fossil_fuel_electricity}TWh.")
            elif "financial flow for developing countries" in input_text:
                financial_developement = country_data.get("Financial flows to developing countries (US $)","Data not avaliable")  
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Financial flows to developing countries (US $) is {financial_developement}TWh.")
            elif "low carbon electricity" in input_text:
                low_carbon_electricity = country_data.get("Low-carbon electricity (% of total electricity)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Low-carbon electricity is {low_carbon_electricity}%.") 
            elif "land area" in input_text:
               land_area = country_data.get("Land Area(Km2)","Data not avaliable")
               responses.append(f"{country_data['Entity']} ({country_data['Year']}): Land Area is {land_area} KM2.")       
            elif "density area" in input_text:
                density_area= country_data.get("Density\\n(P/Km2)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Density of Area is {density_area} P/KM2.")
            elif "Primary energy consumption per capita" in input_text:
                energy_consumption= country_data.get("Primary energy consumption per capita (kWh/person)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Density of Area is {energy_consumption} KWh/person.")
            elif "energy intensity level of primary energy" in input_text:
                energy_intensity_level=country_data.get("Energy intensity level of primary energy (MJ/$2017 PPP GDP)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Energy intensity level of primary energy is {energy_intensity_level} MJ/$2017 PPP GDP.")
            elif "renewables" in input_text:
                renewable_energy_share1= country_data.get("Renewables (% of equivalent primary energy)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Renewables of equivalent primary energy is {renewable_energy_share1} %.")
            elif "renewable electricity generating capacity per capita" in input_text:
                renewable_electricity= country_data.get("Renewable-electricity-generating-capacity-per-capita","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Renewables of equivalent primary energy is {renewable_electricity} W/person.")
            elif "renewable electricity" in input_text:
                renewable_electricity_use= country_data.get("Electricity from renewables (TWh)","Data not avaliable")
                responses.append(f"{country_data['Entity']} ({country_data['Year']}): Renewable electricity is {renewable_electricity_use} TWh.")
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


