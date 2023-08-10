import pandas as pd
import folium
import geocoder
import os

def get_coordinates(city, country):
    while True:
        g = geocoder.bing(f"{city}, {country}", key=os.getenv("GEO_BING_KEY").strip().rstrip())
        results = g.json
        if results:
            break

    try:
        return results['lat'], results['lng']
    except:
        lat, lng = results["raw"]["point"]["coordinates"]
        return lat, lng

# Load the csv data into pandas dataframe
df = pd.read_csv("database/supplier.csv")

# Group by city and count the number of suppliers in each city
city_counts = df.groupby(['country', 'city']).size().reset_index(name='supplier_count')

# Create a map centered around the world
m = folium.Map(location=[20,0], zoom_start=2, tiles='cartodbpositron')

# For each city in the dataframe, add a circle to the map
for index, row in city_counts.iterrows():
    coords = get_coordinates(row['city'], row['country'])
    if coords:
        folium.Circle(
            location=coords,
            radius=int(row['supplier_count']*10000),  # adjust multiplier as per your need
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"{row['city']}, {row['country']} ({row['supplier_count']} suppliers)"
        ).add_to(m)

# Save the map to an HTML file
os.makedirs('images', exist_ok=True)
m.save('images/supplier_on_map.html')
