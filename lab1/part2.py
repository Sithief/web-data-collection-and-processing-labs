import requests
import json

# 1. Configuration
# Replace 'YOUR_API_KEY_HERE' with the key you got from the website
API_KEY = "YOUR_API_KEY_HERE"
CITY = "Novosibirsk"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# 2. Prepare the parameters (Authorization + Query)
params = {
    "key": API_KEY,
    "q": CITY,
    "aqi": "no"  # Air Quality Index (optional)
}

# 3. Make the authorized request
response = requests.get(BASE_URL, params=params)

# 4. Process and Save
if response.status_code == 200:
    data = response.json()

    # Save to file
    filename = "weatherapi_data.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Success! Current temperature in {CITY} is {data['current']['temp_c']}°C")
    print(f"Data saved to {filename}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)