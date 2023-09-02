
# Google Maps Geocoding Script

This script allows you to geocode addresses using the Google Maps API. By providing a list of addresses in a CSV file, you can retrieve detailed address components, such as street, city, state, country, and postal code.

## How the Script Works

The script works by reading addresses from column A of the `input.csv` file. Each address in column A is then used to query the Google Maps Geocoding API.

For each successful query, the script retrieves and formats the address into seven components: street, secondary street, county, state, country, postal code, and city. The API might not always provide all seven components for every address, so some fields may remain empty in the output.

The formatted address data is then inserted into the first available set of seven consecutive columns without populated data in the `output.csv` file. This ensures that existing data in the CSV isn't overwritten.

To control the number of rows processed from the `input.csv`, you can modify the `ROWS_TO_PROCESS` constant in the script. By default, this is set to 1000, but you can adjust it as per your needs.



The script reads addresses from the `input.csv` file and queries the Google Maps Geocoding API for each address. For each successful query, the script retrieves and formats the address into seven components: street, secondary street, county, state, country, postal code, and city.

The formatted address data is then inserted into the first available set of seven consecutive columns without populated data in the `output.csv` file. This ensures that existing data in the CSV isn't overwritten.

If you wish to limit the number of rows processed from the `input.csv`, you can modify the `ROWS_TO_PROCESS` constant in the script.

## Prerequisites

- Ensure you have Python installed on your machine.
- You'll need the `requests` library. Install it using pip:

  ```
  pip install requests
  ```

## Obtaining a Google Maps API Key

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project drop-down and select or create the project for which you want to add an API key.
3. Navigate to the "Credentials" tab.
4. Click on "Create Credentials" and select "API key". Your new API key will appear. Copy this key.
5. Ensure that the Geocoding API is enabled on your project. You can enable it from the "Library" section in the Google Cloud Console.

## Usage

1. Clone this repository to your local machine.
2. Update the `GOOGLE_API_KEY` constant in the `google_maps_geocoding_api.py` script with the Google Maps API key you obtained.
3. Populate the `input.csv` file with the addresses you wish to geocode. Use the provided `sample_input.csv` as a reference for the expected format.
4. Run the script:

  ```
  python google_maps_geocoding_api.py
  ```

5. Once the script completes, you'll find the geocoded data in the `output.csv` file.

## License

This project is open-source. Feel free to clone, modify, and distribute as per your needs.
