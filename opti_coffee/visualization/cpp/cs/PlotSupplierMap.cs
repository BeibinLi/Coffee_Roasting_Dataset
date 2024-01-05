using System;
using System.IO;
using System.Data;
using Folium;
using Geocoder;

namespace CoffeeDistribution.Visualization
{
    public class PlotSupplierMap
    {
        public static (double, double) GetCoordinates(string city, string country)
        {
            Geocoder.Geocoder geocoder = new Geocoder.Geocoder("YOUR_BING_MAPS_API_KEY");
            var result = geocoder.Geocode(city + ", " + country).Result;
            return (result.Latitude, result.Longitude);
        }

        public static void PlotMap(DataTable cityCounts)
        {
            var map = new Map(location: new LatLng(20, 0), zoom: 2);
            map.SetTileLayer("cartodbpositron");

            foreach (DataRow row in cityCounts.Rows)
            {
                var coords = GetCoordinates(row.Field<string>("City"), row.Field<string>("Country"));
                var circle = new Circle(coords, row.Field<int>("SupplierCount") * 10000)
                {
                    Color = "blue",
                    FillColor = "blue",
                    FillOpacity = 0.6,
                    Popup = new Popup($"{row.Field<string>("City")}, {row.Field<string>("Country")} ({row.Field<int>("SupplierCount")} suppliers)")
                };
                map.AddLayer(circle);
            }

            Directory.CreateDirectory("images");
            map.Save("images/supplier_on_map.html");
        }
    }
}