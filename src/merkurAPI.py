import requests
import csv
from datetime import datetime, timezone, timedelta

# Function to convert kickOffTime to GMT+2
def convert_kickoff_time(timestamp):
    gmt_plus_2 = timezone(timedelta(hours=2))
    return datetime.fromtimestamp(timestamp / 1000, tz=gmt_plus_2).strftime('%Y-%m-%d %H:%M:%S')

# URL of the API
api_url = 'https://www.merkurxtip.rs/restapi/offer/sr/sport/S/mob?annex=0&desktopVersion=1.34.2.4'

#OLD https://www.merkurxtip.rs/restapi/offer/sr/sport/S/mob?annex=0&date=09.06.2024&desktopVersion=1.34.2.4&locale=sr

# Fetch the data from the API
response = requests.get(api_url)
data = response.json()

# Extract the required data
extracted_data = []

for match in data["esMatches"]:
    match_info = {
        "home": match["home"],
        "away": match["away"],
        "kickOffTime": convert_kickoff_time(match["kickOffTime"]),
        "leagueName": match["leagueName"],
        "odds_1": match["odds"]["1"] if "1" in match["odds"] else None,
        "odds_x": match["odds"]["2"] if "2" in match["odds"] else None,
        "odds_2": match["odds"]["3"] if "3" in match["odds"] else None  # Replace odds_3 with odds_2
    }
    extracted_data.append(match_info)

# Define the CSV file headers
headers = ["home", "away", "kickOffTime", "leagueName", "odds_1", "odds_x", "odds_2"]  # Update headers

# Save the data to a CSV file
with open('merkur.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for row in extracted_data:
        writer.writerow(row)

# Print the extracted data
print("Data has been saved to extracted_data.csv")
