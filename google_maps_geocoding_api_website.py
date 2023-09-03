from urllib.parse import quote


import csv
import requests
import json

# Constants
def get_place_details(place_id):
    # Construct URL for the Google Maps Place Details API
    fields = "formatted_phone_number,website,name,permanently_closed,opening_hours,types"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={GOOGLE_API_KEY}"
    
    # Make the request
    response = requests.get(url)
    data = response.json()

    # Extract phone number, website, and additional fields
    phone_number = data.get('result', {}).get('formatted_phone_number', "")
    website = data.get('result', {}).get('website', "")
    short_name = data.get('result', {}).get('name', "")
    permanently_closed = "Yes" if data.get('result', {}).get('permanently_closed') else "No"
    opening_hours = "; ".join(data.get('result', {}).get('opening_hours', {}).get('weekday_text', []))
    types = "; ".join(data.get('result', {}).get('types', []))

    return phone_number, website, short_name, opening_hours

GOOGLE_API_KEY = "GOOGLE_MAPS_API_KEY"
input_file_path = "input.csv"
output_file_path = "output.csv"
ROWS_TO_PROCESS = 100





def get_address_details(address):
    # Construct URL for the Google Maps Geocoding API
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    
    # Make the request
    response = requests.get(url)
    data = response.json()

    # Initialize address details
    country = state = county = postal_code = city = street = street2 = None

    # Extract relevant details
    if data['status'] == "OK":
        components = data['results'][0]['address_components']
        place_id = data['results'][0].get('place_id', None)
        phone_number, website, short_name, opening_hours = get_place_details(place_id) if place_id else (None, None, None, None, None, None)

        for component in components:
            types = component['types']
            if 'country' in types:
                country = component['long_name']
            if 'administrative_area_level_1' in types:
                state = component['long_name']
            if 'administrative_area_level_2' in types:
                county = component['long_name']
            if 'postal_code' in types:
                postal_code = component['long_name']
            if 'locality' in types:
                city = component['long_name']
            if 'route' in types:
                street = component['long_name']
            if 'street_number' in types:
                street_number = component['long_name']
                street = f"{street_number} {street}" if street else street_number
            if 'subpremise' in types:
                street2 = component['long_name']

        return street, street2, county, state, country, postal_code, city, phone_number, website, opening_hours
    else:
        print(f"Error for address '{address}': {data['status']}")  # Feedback for errors
        return None, None, None, None, None, None, None


# Open the input and output CSV files
with open(input_file_path, "r") as infile, open(output_file_path, "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header to the output file
    header = next(reader)
    writer.writerow(header + ['Street-api', 'Street-api2', 'County-api', 'State-api', 'Country-api', 'Postal Code-api', 'City-api', 'phone-api', 'website-api', 'opening-hours-api'])  # Add new column headers

    # Process each row, limited to 100
    for row_num, row in enumerate(reader, start=1):
        if row_num > ROWS_TO_PROCESS:
            break

        # Using column A as the lookup address
        lookup_address = row[0]
        
        # Skip blank addresses
        if not lookup_address.strip():
            writer.writerow(row + [None] * 7)  # Populate with 7 blank values for consistency
            continue

        print(f"Processing address: {lookup_address}")  # Feedback for address being processed
        address_details = get_address_details(lookup_address)

        # Add the address details to the end of the row
        row += address_details[:10]

        writer.writerow(row)
