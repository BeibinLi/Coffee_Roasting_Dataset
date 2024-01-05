import org.json.JSONArray;
import org.json.JSONObject;
import kong.unirest.HttpResponse;
import kong.unirest.JsonNode;
import kong.unirest.Unirest;
import org.openstreetmap.gui.jmapviewer.*;
import org.openstreetmap.gui.jmapviewer.interfaces.MapMarker;

import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SupplierOnMap {

    public static void main(String[] args) {
        Map<String, Integer> cityCounts = getCityCounts("database/supplier.csv");
        plotMap(cityCounts);
    }

    private static Map<String, Integer> getCityCounts(String filePath) {
        Map<String, Integer> cityCounts = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean isFirstLine = true;
            while ((line = br.readLine()) != null) {
                if (isFirstLine) {
                    isFirstLine = false;
                    continue;
                }
                String[] values = line.split(",");
                String city = values[2].trim();
                String country = values[3].trim();
                String key = city + ", " + country;
                cityCounts.put(key, cityCounts.getOrDefault(key, 0) + 1);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return cityCounts;
    }

    private static Coordinate getCoordinates(String city, String country) {
        String apiKey = System.getenv("GEO_BING_KEY").trim();
        HttpResponse<JsonNode> response = Unirest.get("http://dev.virtualearth.net/REST/v1/Locations")
                .queryString("q", city + ", " + country)
                .queryString("key", apiKey)
                .asJson();

        JSONObject location = response.getBody().getObject()
                .getJSONArray("resourceSets")
                .getJSONObject(0)
                .getJSONArray("resources")
                .getJSONObject(0)
                .getJSONObject("point")
                .getJSONArray("coordinates");

        return new Coordinate(location.getDouble(0), location.getDouble(1));
    }

    private static void plotMap(Map<String, Integer> cityCounts) {
        JMapViewer map = new JMapViewer();
        map.setZoom(2);
        map.setDisplayPosition(new Coordinate(20, 0), 2);

        for (Map.Entry<String, Integer> entry : cityCounts.entrySet()) {
            String[] parts = entry.getKey().split(", ");
            String city = parts[0];
            String country = parts[1];
            int count = entry.getValue();

            Coordinate coords = getCoordinates(city, country);
            MapMarker marker = new MapMarkerCircle(coords, count * 10000); // adjust multiplier as per your need
            map.addMapMarker(marker);
        }

        JFrame frame = new JFrame("Supplier Locations");
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(map);
        frame.setVisible(true);
    }
}