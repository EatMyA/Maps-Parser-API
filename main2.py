import requests
import pandas as pd
import os

api_key = ""
cse_id = "572fba3e438164b37"
search_query = "renovation london"
start_index = 1
max_results = 800  # Change as needed, up to the limit of your API plan

def google_search(query, api_key, cse_id, start):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cse_id}&key={api_key}&start={start}"
    response = requests.get(url)
    return response.json()

# List to store data
data_list = []

while start_index <= max_results:
    results = google_search(search_query, api_key, cse_id, start_index)
    for item in results.get('items', []):
        data_list.append({
            "Title": item.get("title"),
            "Link": item.get("link"),
            "Snippet": item.get("snippet")
        })
    start_index += 10

# Create a DataFrame from the data list
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
df.to_csv("google_search_results2.csv", index=False)
print("Data successfully saved to CSV file.")
