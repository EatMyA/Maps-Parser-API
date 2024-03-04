import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import re

api_key = "AIzaSyB5UQYA7LKIS4m5PeH4hePLZHERRPWJons"
search_query = "renovation"
city_coordinates = "51.5074,-0.1278"  # London coordinates
radius = 40000  # Search radius in meters (e.g., 20 km)

def make_request(url):
  response = requests.get(url)
  return response.json()

def get_place_details(place_id, api_key):
  details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
  details_response = requests.get(details_url)
  details_data = details_response.json()
  return details_data["result"]

# List to store data
data_list = []

# Initial URL for the text search request
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&location={city_coordinates}&radius={radius}&key={api_key}"

# Process the first request
data = make_request(url)

# Loop through each page of results
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
          # "Email": "N/A",
          # "Opening Hours": details_data.get("opening_hours", {}).get("weekday_text", "N/A"),
          # "Review Count": details_data.get("user_ratings_total", "N/A"),
          # "Rating": result.get("rating", "N/A"),
          # "Types": details_data.get("types", []),
          # "Photos Links": details_data.get("photos", []),
          # "Logo Link": details_data.get("icon", "N/A"),
          # "Google Places API Link": f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
      })

  # Check for next page token
  next_page_token = data.get("next_page_token")
  if not next_page_token:
      print("Last page.")
      break

  # Prepare the URL for the next page
  next_page_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={api_key}"

  # Google API requires a short delay before requesting the next page
  time.sleep(10)

  # Request the next page
  data = make_request(next_page_url)

# Create a DataFrame from the data list
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
df.to_csv("renovations2.csv", index=False)
print("Data successfully saved to CSV file.")
