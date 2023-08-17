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

public class CPPSupplierMap {

    public static void main(String[] args) {
        List<String[]> cityCounts = readCityCounts("city_counts.txt");
        plotMap(cityCounts);
    }

    private static List<String[]> readCityCounts(String filePath) {
        List<String[]> cityCounts = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                cityCounts.add(line.split(","));
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

    private static void plotMap(List<String[]> cityCounts) {
        JMapViewer map = new JMapViewer();
        map.setZoom(2);
        map.setDisplayPosition(new Coordinate(20, 0), 2);

        for (String[] entry : cityCounts) {
            String country = entry[0].trim();
            String city = entry[1].trim();
            int count = Integer.parseInt(entry[2].trim());

            Coordinate coords = getCoordinates(city, country);
            MapMarker marker = new MapMarkerCircle(coords, count * 10000); // adjust multiplier as per your need
            map.addMapMarker(marker);
        }

        JFrame frame = new JFrame("CPP Supplier Locations");
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(map);
        frame.setVisible(true);
    }
}