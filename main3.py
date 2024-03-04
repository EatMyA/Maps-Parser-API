import pandas as pd
import requests
import time

api_key = "AIzaSyB5UQYA7LKIS4m5PeH4hePLZHERRPWJons"

# Reading names from a CSV file
# Replace 'your_file.csv' with your actual file path
# Replace 'column_name' with the actual column name that contains the names
df = pd.read_csv('Sheet22.csv')
name_list = df['name'].tolist()

def make_request(url):
    response = requests.get(url)
    return response.json()

def get_place_details(place_id, api_key):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    details_response = requests.get(details_url)
    details_data = details_response.json()
    return details_data["result"]

data_list = []

for name in name_list:
    search_query = name
    city_coordinates = "51.5074,-0.1278"  # London coordinates
    radius = 40000  # Search radius in meters
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&location={city_coordinates}&radius={radius}&key={api_key}"

    data = make_request(url)

    while True:
        results = data.get("results", [])
        for result in results:
            place_id = result.get("place_id", "N/A")
            details_data = get_place_details(place_id, api_key)
            data_list.append({
                "Name": result.get("name", "N/A"),
                "Address": result.get("formatted_address", "N/A"),
                "Website": details_data.get("website", "N/A"),
                "Phone Number": details_data.get("formatted_phone_number", "N/A"),
                # Other fields can be added as required
            })

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        next_page_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={api_key}"
        time.sleep(3)  # Delay to respect Google's API requirements
        data = make_request(next_page_url)

df = pd.DataFrame(data_list)
df.to_csv("res22.csv", index=False)
print("Data successfully saved to CSV file.")
