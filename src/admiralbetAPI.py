import requests
import csv
from datetime import datetime, timedelta

# Function to separate home and away team names
def extract_team_names(match_name):
    if " - " in match_name:
        team_names = match_name.split(" - ")
        return team_names[0], team_names[1]
    else:
        return match_name, "N/A"

# Function to extract odds based on outcome name
def extract_odds(bet_outcomes):
    odds_1 = bet_outcomes[0].get("odd") if len(bet_outcomes) > 0 else None
    odds_x = bet_outcomes[1].get("odd") if len(bet_outcomes) > 1 else None
    odds_2 = bet_outcomes[2].get("odd") if len(bet_outcomes) > 2 else None
    return odds_1, odds_x, odds_2

# Function to add 2 hours to datetime string
def add_2_hours(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    datetime_obj += timedelta(hours=2)
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

# URL of the API
base_url = 'https://sport-webapi.admiralbet.rs/api/offer/getEventsStartingSoonFilterSelections/?sportId=1&isLive=false&dateFrom=2024-06-09T14:48:22.799&dateTo=2029-06-09T14:47:52.000&eventMappingTypes=&pageId=3'

# Initialize skipN
skipN = 0

# Initialize data list
extracted_data = []

# Loop until we have 150 matches or no more data is returned
while len(extracted_data) < 150:
    # Fetch the data from the API with updated skipN
    api_url = f"{base_url}&topN=25&skipN={skipN}"
    response = requests.get(api_url)
    data = response.json()

    # If no data is returned, break the loop
    if not data:
        break

    # Extract the required data
    for match in data:
        if "bets" in match and len(match["bets"]) > 0:
            home_name, away_name = extract_team_names(match["name"])
            odds_1, odds_x, odds_2 = extract_odds(match["bets"][0].get("betOutcomes", []))
            match_info = {
                "home": home_name,
                "away": away_name,
                "dateTime": add_2_hours(match["dateTime"]),
                "odds_1": odds_1,
                "odds_x": odds_x,
                "odds_2": odds_2
            }
            extracted_data.append(match_info)

    # Increment skipN by 25 for the next iteration
    skipN += 25

# Define the CSV file headers
headers = ["home", "away", "dateTime", "odds_1", "odds_x", "odds_2"]

# Save the data to a CSV file
with open('admiralbet.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for row in extracted_data:
        writer.writerow(row)

# Print the extracted data
print("Data has been saved to admiralbet.csv")
