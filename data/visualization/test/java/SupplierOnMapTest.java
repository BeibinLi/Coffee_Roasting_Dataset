import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SupplierOnMapTest {

    @Test
    void testGetCoordinates() {
        // Test the getCoordinates function with a sample city and country
        String city = "Seattle";
        String country = "USA";
        Coordinate coords = SupplierOnMap.getCoordinates(city, country);

        // Check that the latitude and longitude are within reasonable bounds
        assertTrue(coords.getLat() > 47 && coords.getLat() < 48);
        assertTrue(coords.getLon() > -123 && coords.getLon() < -122);
    }
}