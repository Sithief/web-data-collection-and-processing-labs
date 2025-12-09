import requests
import json

# 1. Define the target user and the endpoint
username = "torvalds"  # You can change this to any valid GitHub username
url = f"https://api.github.com/users/{username}/repos"

# 2. Make the GET request
response = requests.get(url)

# 3. Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # 4. Save the data to a file
    filename = f"{username}_repos.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Success! Found {len(data)} repositories.")
    print(f"Data saved to {filename}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)