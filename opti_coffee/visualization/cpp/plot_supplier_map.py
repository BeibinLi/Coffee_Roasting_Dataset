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

def plot_map(city_counts):
    m = folium.Map(location=[20,0], zoom_start=2, tiles='cartodbpositron')

    for index, row in city_counts.iterrows():
        coords = get_coordinates(row['city'], row['country'])
        if coords:
            folium.Circle(
                location=coords,
                radius=int(row['supplier_count']*10000),
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"{row['city']}, {row['country']} ({row['supplier_count']} suppliers)"
            ).add_to(m)

    os.makedirs('images', exist_ok=True)
    m.save('images/supplier_on_map.html')

if __name__ == "__main__":
    city_counts = pd.read_csv("city_counts.txt", header=None, names=["country", "city", "supplier_count"])
    plot_map(city_counts)