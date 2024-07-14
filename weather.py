import requests
import pandas as pd
from datetime import datetime, timedelta

# Your OpenWeatherMap API key
api_key = 'b268cab05964893b6d8bd77e692c0636'

# List of districts in Tamil Nadu (this is a sample list; add all districts)
districts = ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
    "Tirunelveli", "Tiruppur", "Ranipet", "Vellore", "Thoothukudi",
    "Tiruvallur", "Thanjavur", "Dindigul", "Erode", "Cuddalore",
    "Kancheepuram", "Kanyakumari", "Karur", "Krishnagiri", "Nagapattinam",
    "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram",
    "Sivaganga", "Tenkasi", "Theni", "Thiruvannamalai", "Tiruvarur",
    "Villupuram"]

# Function to fetch weather data for a given district and date
def fetch_weather_data(district, date, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': district + ',IN',  # District, Country code
        'date': date,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Function to fetch data for all districts and dates
def fetch_all_data(districts, start_date, end_date, api_key):
    date_range = pd.date_range(start=start_date, end=end_date)
    all_data = []

    for district in districts:
        for date in date_range:
            formatted_date = date.strftime('%Y-%m-%d')
            data = fetch_weather_data(district, formatted_date, api_key)
            if data.get('cod') == 200:
                weather_data = {
                    'District': district,
                    'Date': formatted_date,
                    'Temperature (°C)': data['main']['temp'],
                    'Humidity (%)': data['main']['humidity'],
                    'Weather': data['weather'][0]['description'],
                    'Wind Speed (m/s)': data['wind']['speed']
                }
                all_data.append(weather_data)
            else:
                print(f"Failed to fetch data for {district} on {formatted_date}")

    return pd.DataFrame(all_data)

# Main script execution
if __name__ == "__main__":
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    weather_df = fetch_all_data(districts, start_date, end_date, api_key)
    print(weather_df)